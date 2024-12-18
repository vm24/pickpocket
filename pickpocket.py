import asyncio
import psutil
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
from telethon.tl.types import User
from pynput import mouse, keyboard
import threading
import time
import sys
import logging
# ------------------- Configuration -------------------

# Telegram API credentials (replace with your own)
api_id = ''        # Replace with your api_id
api_hash = ''    # Replace with your api_hash

# Your phone number with country code (e.g., +123456789)
phone_number = ''

# The username of the target to send messages to (format: username)
target_username = ''

# ------------------------------------------------------

# Configure logging
logging.basicConfig(
    filename='pickpocket.log',
    level=logging.INFO,
    format='%(asctime)s:%(levelname)s:%(message)s'
)

# Initialize the Telegram client
client = TelegramClient('session_name', api_id, api_hash)

# Global variable to store target entity
target_entity = None

# Function to send a message via Telegram
async def send_message(message):
    global target_entity
    if not target_entity:
        logging.warning("Target user not found.")
        return
    try:
        await client.send_message(target_entity, message)
        logging.info(f"Sent message: {message}")
    except Exception as e:
        logging.error(f"Failed to send message: {e}")

# Function to authenticate and get the target entity
async def setup_telegram(loop):
    global target_entity
    await client.start(phone=phone_number)
    
    try:
        # Attempt to get the target entity directly
        target_entity = await client.get_entity(target_username)
        logging.info(f"Successfully found target user: {target_username}")
    except ValueError:
        logging.warning(f"Direct retrieval failed. Searching through dialogs for {target_username}...")
        dialogs = await client.get_dialogs(limit=100)
        for dialog in dialogs:
            entity = dialog.entity
            if isinstance(entity, User) and entity.username == target_username:
                target_entity = entity
                logging.info(f"Found target user in dialogs: {target_username}")
                break
        else:
            logging.error(f"User '{target_username}' not found in your contacts or dialogs.")
            sys.exit(1)

# Charger status monitoring
class ChargerMonitor(threading.Thread):
    def __init__(self, loop, check_interval=5):
        super().__init__()
        self.loop = loop
        self.check_interval = check_interval
        battery = psutil.sensors_battery()
        if battery is None:
            logging.error("Unable to retrieve battery information.")
            sys.exit(1)
        self.last_status = battery.power_plugged
        self.running = True

    def run(self):
        while self.running:
            try:
                battery = psutil.sensors_battery()
                if battery is None:
                    logging.error("Unable to retrieve battery information.")
                    time.sleep(self.check_interval)
                    continue
                current_status = battery.power_plugged
                if current_status != self.last_status:
                    status_str = "Charger Plugged In" if current_status else "Charger Unplugged"
                    logging.info(f"Charger status changed: {status_str}")
                    asyncio.run_coroutine_threadsafe(send_message(status_str), self.loop)
                    self.last_status = current_status
            except Exception as e:
                logging.error(f"Error in ChargerMonitor: {e}")
            time.sleep(self.check_interval)

    def stop(self):
        self.running = False

# User input monitoring
class InputMonitor:
    def __init__(self, loop):
        self.loop = loop
        self.mouse_listener = mouse.Listener(on_move=self.on_move, on_click=self.on_click, on_scroll=self.on_scroll)
        self.keyboard_listener = keyboard.Listener(on_press=self.on_press)
        self.last_event_time = 0
        self.event_cooldown = 5  # seconds to wait before sending another input event

    def on_move(self, x, y):
        try:
            self.handle_event("Mouse moved.")
        except Exception as e:
            logging.error(f"Error in on_move: {e}")

    def on_click(self, x, y, button, pressed):
        try:
            action = "pressed" if pressed else "released"
            self.handle_event(f"Mouse {button} {action} at ({x}, {y}).")
        except Exception as e:
            logging.error(f"Error in on_click: {e}")

    def on_scroll(self, x, y, dx, dy):
        try:
            self.handle_event(f"Mouse scrolled at ({x}, {y}) with delta ({dx}, {dy}).")
        except Exception as e:
            logging.error(f"Error in on_scroll: {e}")

    def on_press(self, key):
        try:
            self.handle_event(f"Key {key} pressed.")
        except Exception as e:
            logging.error(f"Error in on_press: {e}")

    def handle_event(self, message):
        current_time = time.time()
        if current_time - self.last_event_time > self.event_cooldown:
            logging.info(f"Handling event: {message}")
            asyncio.run_coroutine_threadsafe(send_message(message), self.loop)
            self.last_event_time = current_time

    def start(self):
        self.mouse_listener.start()
        self.keyboard_listener.start()

    def stop(self):
        self.mouse_listener.stop()
        self.keyboard_listener.stop()

# Main asynchronous function
async def main():
    loop = asyncio.get_running_loop()
    await setup_telegram(loop)

    # Start charger monitoring in a separate thread
    charger_monitor = ChargerMonitor(loop, check_interval=5)
    charger_monitor.start()

    # Start input monitoring
    input_monitor = InputMonitor(loop)
    input_monitor.start()

    logging.info("Monitoring started. Press Ctrl+C to stop.")
    print("Monitoring started. Press Ctrl+C to stop.")

    try:
        await client.run_until_disconnected()
    except KeyboardInterrupt:
        logging.info("Stopping monitoring...")
        print("Stopping monitoring...")
    finally:
        charger_monitor.stop()
        input_monitor.stop()

# Entry point
if __name__ == '__main__':
    try:
        asyncio.run(main())
    except Exception as e:
        logging.critical(f"Unhandled exception: {e}")