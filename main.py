import asyncio
import aiohttp
import requests
import uuid
import os
import sys
import time
import random
import json
import logging
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base
from colorama import init, Fore, Style

# Инициализация colorama
init(autoreset=True)

# Конфигурация для базы данных
DATABASE_URL = os.getenv('DATABASE_URL')
Base = declarative_base()
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

class Record(Base):
    __tablename__ = 'records'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=True)
    content = Column(String(255))
    date_sent = Column(String(10), nullable=True)

Base.metadata.create_all(engine)

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Цвета для вывода
mrh = Fore.LIGHTRED_EX
pth = Fore.LIGHTWHITE_EX
hju = Fore.LIGHTGREEN_EX
reset = Style.RESET_ALL

EVENTS_DELAY = 20000 / 1000

def load_config():
    try:
        with open('config.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        logging.error("Config file not found.")
        sys.exit(1)

config = load_config()
games = config['games']

def load_proxies():
    proxies = []
    if config.get('use_proxies'):
        try:
            with open('proxies.txt', 'r') as file:
                for line in file:
                    proxies.append(parse_proxy(line.strip()))
        except FileNotFoundError:
            print("proxies.txt not found")
    return proxies

def parse_proxy(proxy_string):
    try:
        proxy_parts = proxy_string.split('@')
        auth = proxy_parts[0].split(':')
        host_port = proxy_parts[1].split(':')
        return {
            'http': f"http://{auth[0]}:{auth[1]}@{host_port[0]}:{host_port[1]}",
            'https': f"http://{auth[0]}:{auth[1]}@{host_port[0]}:{host_port[1]}"
        }
    except (IndexError, ValueError):
        logging.error(f"Invalid proxy format: {proxy_string}")
        return None

def get_proxy(proxies):
        return random.choice(proxies) if proxies else None

def _banner():
    banner = r"""
 ██╗████████╗███████╗     ██╗ █████╗ ██╗    ██╗
 ██║╚══██╔══╝██╔════╝     ██║██╔══██╗██║    ██║
 ██║   ██║   ███████╗     ██║███████║██║ █╗ ██║
 ██║   ██║   ╚════██║██   ██║██╔══██║██║███╗██║
 ██║   ██║   ███████║╚█████╔╝██║  ██║╚███╔███╔╝
 ╚═╝   ╚═╝   ╚══════╝ ╚════╝ ╚═╝  ╚═╝ ╚══╝╚══╝  """
    print(Fore.GREEN + Style.BRIGHT + banner + Style.RESET_ALL)
    print(hju + f" Hamster Promo Code Generator")
    print(mrh + f" NOT FOR SALE = Free to use")
    print(mrh + f" before start please '{hju}git pull{mrh}' to update bot\n")

def _clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def log_line():
    print(pth + "~" * 60)

def countdown_timer(seconds):
    while seconds:
        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)
        h = str(h).zfill(2)
        m = str(m).zfill(2)
        s = str(s).zfill(2)
        print(f"{pth}please wait until {h}:{m}:{s} ", flush=True, end="\r")
        seconds -= 1
        time.sleep(1)
    print(f"{pth}please wait until {h}:{m}:{s} ", flush=True, end="\r")

def generate_client_id():
    timestamp = int(time.time() * 1000)
    random_numbers = ''.join([str(random.randint(0, 9)) for _ in range(19)])
    return f"{timestamp}-{random_numbers}"

def generate_uuid():
    return str(uuid.uuid4())

async def login(client_id, app_token, proxies=None):
    proxy = get_proxy(proxies)
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post('https://api.gamepromo.io/promo/login-client',
                                    json={
                                        'appToken': app_token,
                                        'clientId': client_id,
                                        'clientOrigin': 'deviceid'
                                    },
                                    proxy=proxy) as response:
                response.raise_for_status()
                data = await response.json()
                return data.get('clientToken')
        except aiohttp.ClientError as e:
            logging.error(f"(Login failed: {e}")
            return None

async def emulate_progress(client_token, promo_id, proxies=None):
    response = requests.post('https://api.gamepromo.io/promo/register-event', headers={
        'Authorization': f'Bearer {client_token}',
        'Content-Type': 'application/json'
    }, json={
        'promoId': promo_id,
        'eventId': generate_uuid(),
        'eventOrigin': 'undefined'
    }, proxies=proxies)

    if response.status_code != 200:
        return False

    data = response.json()
    return data['hasCode']

async def generate_key(client_token, promo_id, proxies=None):
    response = requests.post('https://api.gamepromo.io/promo/create-code', headers={
        'Authorization': f'Bearer {client_token}',
        'Content-Type': 'application/json'
    }, json={
        'promoId': promo_id
    }, proxies=proxies)

    if response.status_code != 200:
        raise Exception('Failed to generate key')

    data = response.json()
    return data['promoCode']

def delay_random():
    return random.random() / 3 + 1

def insert_tokens_to_db(tokens):
    unique_tokens = {token for token in tokens if token}

    with Session() as session:
        new_records = [Record(content=token) for token in unique_tokens if session.query(Record).filter_by(content=token).count() == 0]
        session.bulk_save_objects(new_records)
        session.commit()
    logging.info(f"Inserted {len(new_records)} unique tokens into the database.")

def save_tokens_to_file(tokens, file_path='promo.txt'):
    with open(file_path, 'a') as file:
        for token in tokens:
            file.write(f"{token}\n")

async def generate_key_process(game, key_count, proxies):
    client_id = generate_client_id()
    client_token = None
    try:
        client_token = await login(client_id, game['appToken'], proxies)
    except Exception as error:
        print(mrh + f"Failed to login: {error}")
        return None

    for i in range(11):
        await asyncio.sleep(EVENTS_DELAY * delay_random())
        has_code = await emulate_progress(client_token, game['promoId'], proxies)
        if has_code:
            break

    try:
        key = await generate_key(client_token, game['promoId'], proxies)
        return key
    except Exception as error:
        print(f"Failed to generate key: {error}")
        return None

async def main():
    _clear()
    _banner()
    log_line()
    game_choice = random.randint(1, 6)
    key_count = config.get('key_count', 1)
    game = games[str(game_choice)]
    proxies = load_proxies()

    while True:
        proxy = get_proxy(proxies)
        keys = await asyncio.gather(*[generate_key_process(game, key_count, proxy) for _ in range(key_count)])
        keys = list(filter(None, keys))

        if keys:
            if config.get('save_to_db', False):
                insert_tokens_to_db(keys)
            else:
                save_tokens_to_file(keys)

        print(hju + f"Generated {pth}{len(keys)} promo code's. {hju}Sleeping for a bit before generating more...      ")
        game_choice = random.randint(1, 6)
        game = games[str(game_choice)]
        countdown_timer(600)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print(mrh + f"\rSuccessfully logged out of the bot\n")
        sys.exit()
