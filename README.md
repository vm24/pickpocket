# PickPocket-IT

**PickPocket-IT** is a Python script for reporting **Mouse Movement**, **Key Pressed**, and **Plug/Unplug Charger** events to a target **Telegram** user. It's perfect for use in public places, study halls, or any environment where you need to monitor activity discreetly.

## Features:
- Track mouse movements.
- Capture key presses.
- Detect charger plug/unplug events.
- Send notifications to a Telegram user.

## Requirements:
- **Python 3.12+**
- **Telethon**: For interacting with Telegram.
- **Pynput**: For monitoring keyboard and mouse events.
- **Psutil**: For detecting system status, like charger events.

You can install all dependencies using pip:
```bash
pip install psutil telethon pynput
