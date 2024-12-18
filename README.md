# 🕵️‍♂️ PickPocket

**PickPocket-IT** is a Python script designed to report events like **Mouse Movements**, **Key Presses**, and **Charger Plug/Unplug** actions to a target **Telegram user**. Perfect for monitoring activity in public places, study halls, or personal environments where your belongings are left unattended.

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
