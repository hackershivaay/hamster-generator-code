# Hamster Kombat Promo Code Generator

![image](https://github.com/user-attachments/assets/2c32eccc-7173-42b6-967d-8489756edcc5)


A script for generating promo codes using the GamePromo API. This tool supports multiple games and proxies, and it displays progress in a visually appealing manner.

[TELEGRAM CHANNEL](https://t.me/Deeplchain) | [TWITTER](https://x.com/itsjaw_real)

### Send me a thankyou 💪 
```
0x705C71fc031B378586695c8f888231e9d24381b4 - EVM
TDTtTc4hSnK9ii1VDudZij8FVK2ZtwChja - TRON
UQBy7ICXV6qFGeFTRWSpnMtoH6agYF3PRa5nufcTr3GVOPri - TON
```

## Summary ( Latest Update on 09 - 07 - 2024 )

- Give a Small Update
- Add New Game Promo ID
- Fix Random Game Selection

***if `"random_selection": false`, will choose game from `"selected_games": ["2","6"]`, you can add more selections by adding more number. example : `"selected_games": ["2","6","3"]`***

## Features

- Generate promo codes for various games.
- Support for proxy usage.
- Display progress percentage during the process.
- Configurable settings via `configs.json`.
- Output results to `promo.txt`.

## Table of Contents

- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [How It Works](#how-it-works)
- [License](#license)

## Installation

To get started, clone this repository and install the required dependencies:

1. **Clone the repository:**

   ```bash
   git clone https://github.com/jawikas/hamster-generator-code.git
   cd hamster-generator-code
Create a virtual environment (optional but recommended):

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```
Install the dependencies:

```bash
pip install -r requirements.txt
```

## Configuration
Create configs.json:

This file should be located in the root directory of the project. Here is a sample configuration:

```json
{
    "key_count": 8,
    "countdown_delay": 11,
    "use_proxies": false,
    "random_selection": false,
    "selected_games": ["8"],
    "games": {
        "1": {
            "name": "Chain Cube 2048",
            "appToken": "d1690a07-3780-4068-810f-9b5bbf2931b2",
            "promoId": "b4170868-cef0-424f-8eb9-be0622e8e8e3",
            "event_delay": 21
        },
        "2": {
            "name": "My Clone Army",
            "appToken": "74ee0b5b-775e-4bee-974f-63e7f4d5bacb",
            "promoId": "fe693b26-b342-4159-8808-15e3ff7f8767",
            "event_delay": 21
        },
        "3": {
            "name": "Train Miner",
            "appToken": "82647f43-3f87-402d-88dd-09a90025313f",
            "promoId": "c4480ac7-e178-4973-8061-9ed5b2e17954",
            "event_delay": 21
        },
        "4": {
            "name": "MergeAway",
            "appToken": "8d1cc2ad-e097-4b86-90ef-7a27e19fb833",
            "promoId": "dc128d28-c45b-411c-98ff-ac7726fbaea4",
            "event_delay": 21
        },
        "5": {
            "name": "Twerk Race 3D",
            "appToken": "61308365-9d16-4040-8bb0-2f4a4c69074c",
            "promoId": "61308365-9d16-4040-8bb0-2f4a4c69074c",
            "event_delay": 21
        },
        "6": {
            "name": "POLY",
            "appToken": "2aaf5aee-2cbc-47ec-8a3f-0962cc14bc71",
            "promoId": "2aaf5aee-2cbc-47ec-8a3f-0962cc14bc71",
            "event_delay": 31
        },
        "7": {
            "name": "TRIM",
            "appToken": "ef319a80-949a-492e-8ee0-424fb5fc20a6",
            "promoId": "ef319a80-949a-492e-8ee0-424fb5fc20a6",
            "event_delay": 31
        },
        "8": {
            "name": "Zoopolis",
            "appToken": "b2436c89-e0aa-4aed-8046-9b0515e1c46b",
            "promoId": "b2436c89-e0aa-4aed-8046-9b0515e1c46b",
            "event_delay": 21
        },
        "9": {
            "name": "Fluff Crusade",
            "appToken": "112887b0-a8af-4eb2-ac63-d82df78283d9",
            "promoId": "112887b0-a8af-4eb2-ac63-d82df78283d9",
            "event_delay": 31
        },
        "10": {
            "name": "Tile Trio",
            "appToken": "e68b39d2-4880-4a31-b3aa-0393e7df10c7",
            "promoId": "e68b39d2-4880-4a31-b3aa-0393e7df10c7",
            "event_delay": 31
        },
        "11": {
            "name": "Stone Age",
            "appToken": "04ebd6de-69b7-43d1-9c4b-04a6ca3305af",
            "promoId": "04ebd6de-69b7-43d1-9c4b-04a6ca3305af",
            "event_delay": 31
        }
    }
}

```
Create proxies.txt (if using proxies):

List your proxies in the following format:

```ruby
username:password@host:port
```
## Usage
To run the promo code generator:

```bash
python main.py
```
The script will generate promo codes based on the configuration in configs.json and save them to promo.txt.

Progress Display
The script displays a progress bar to show the percentage completion of the promo code generation process.

## How It Works
1. Configuration Loading:

   - The script loads configurations from configs.json.

2. Proxy Handling:

   - If proxies are enabled, the script will use proxies from proxies.txt.

3. Promo Code Generation:

   - The script logs in using the GamePromo API.
   - Emulates progress and generates promo codes based on the configured game and count.

4. Progress Tracking:

   - The progress is displayed in the console with a progress bar.


## License
This project is licensed under the MIT License - see the LICENSE file for details.

Contact
For any questions or issues, please open an issue on GitHub or contact me at [ https://t.me/itsjaw_real ]..
