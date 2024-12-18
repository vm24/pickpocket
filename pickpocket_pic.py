import asyncio
import psutil
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
from telethon.tl.types import User
import cv2  # OpenCV for webcam access
import threading
import logging
import sys
import os
import keyboard  # For tracking keyboard input
import mouse  # For tracking mouse input
import time  # For sleep and time-related function

# ------------------- Configuration -------------------

# Telegram API credentials (replace with your own)
api_id = ''        # Replace with your api_id
api_hash = ''    # Replace with your api_hash

# Your phone number with country code (e.g., +123456789)
phone_number = ''

# The username of the target to send messages to (format: username)
target_username = 'username'

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

# Function to send a message and image via Telegram
async def send_message_and_image(message):
    global target_entity
    if not target_entity:
        logging.warning("Target user not found.")
        return
    
    try:
        image_path = capture_webcam_image()
        if image_path:
            await client.send_file(target_entity, image_path, caption=message)
            logging.info(f"Sent message and image: {message}")
    except Exception as e:
        logging.error(f"Failed to send message and image: {e}")
    finally:
        if image_path and os.path.exists(image_path):
            try:
                os.remove(image_path)
                logging.info(f"Deleted image file: {image_path}")
            except Exception as e:
                logging.error(f"Failed to delete image file: {e}")

# Function to capture a webcam image and save it to disk
def capture_webcam_image(filename="event.jpg"):
    try:
        cap = cv2.VideoCapture(0)  # Open default camera
        if not cap.isOpened():
            logging.error("Cannot access the webcam.")
            return None
        ret, frame = cap.read()
        if ret:
            cv2.imwrite(filename, frame)
            logging.info(f"Captured image saved as {filename}")
            cap.release()
            return filename
        else:
            logging.error("Failed to capture image from webcam.")
            cap.release()
            return None
    except Exception as e:
        logging.error(f"Error capturing webcam image: {e}")
        return None

# Function to authenticate and get the target entity
async def setup_telegram(loop):
    global target_entity
    await client.start(phone=phone_number)
    
    try:
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
    except Exception as e:
        logging.error(f"Could not get target entity: {e}")
        sys.exit(1)

# Charger status monitoring
class ChargerMonitor(threading.Thread):
    def __init__(self, loop, check_interval=5):
        super().__init__()
        self.loop = loop
        self.check_interval = check_interval
        self.running = True
        battery = psutil.sensors_battery()
        if battery is None:
            logging.error("Unable to retrieve battery information.")
            sys.exit(1)
        self.last_status = battery.power_plugged

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
                    asyncio.run_coroutine_threadsafe(send_message_and_image(status_str), self.loop)
                    self.last_status = current_status
            except Exception as e:
                logging.error(f"Error in ChargerMonitor: {e}")
            time.sleep(self.check_interval)

    def stop(self):
        self.running = False

# Input monitoring for keyboard and mouse
class InputMonitor(threading.Thread):
    def __init__(self, loop, event_cooldown=5):
        super().__init__()
        self.loop = loop
        self.event_cooldown = event_cooldown  # seconds
        self.last_event_time = 0
        self.running = True

    def run(self):
        logging.info("Starting input monitoring...")
        try:
            # Register event handlers for mouse events
            mouse.hook(self.on_mouse_event)  # Capture all mouse events using hook
            
            # Register event handler for keyboard input
            keyboard.on_press(self.on_key_event)
            
            # Keep the thread alive
            while self.running:
                time.sleep(1)
        except Exception as e:
            logging.error(f"Error in InputMonitor: {e}")

    def on_key_event(self, event):
        try:
            current_time = time.time()
            if current_time - self.last_event_time > self.event_cooldown:
                message = f"Key '{event.name}' pressed."
                logging.info(message)
                asyncio.run_coroutine_threadsafe(send_message_and_image(message), self.loop)
                self.last_event_time = current_time
        except Exception as e:
            logging.error(f"Error in on_key_event: {e}")

    def on_mouse_event(self, event):
        try:
            current_time = time.time()
            
            # Ensure we don’t process too many events in a short time
            if current_time - self.last_event_time > self.event_cooldown:
                message = f"Mouse event: {event}"
                if isinstance(event, mouse.ButtonEvent):
                    action = "pressed" if event.event_type == "down" else "released"
                    message = f"Mouse button '{event.button}' {action} at ({event.x}, {event.y})."
                elif isinstance(event, mouse.MoveEvent):
                    message = f"Mouse moved to ({event.x}, {event.y})."
                elif isinstance(event, mouse.ScrollEvent):
                    message = f"Mouse scrolled at ({event.x}, {event.y}) with delta ({event.delta_x}, {event.delta_y})."
                
                logging.info(message)
                asyncio.run_coroutine_threadsafe(send_message_and_image(message), self.loop)
                self.last_event_time = current_time
        except Exception as e:
            logging.error(f"Error in on_mouse_event: {e}")

    def stop(self):
        self.running = False
        # Unhook all keyboard and mouse listeners
        keyboard.unhook_all()
        mouse.unhook_all()

# Main asynchronous function
async def main():
    loop = asyncio.get_running_loop()
    await setup_telegram(loop)

    # Start charger monitoring in a separate thread
    charger_monitor = ChargerMonitor(loop, check_interval=5)
    charger_monitor.start()

    # Start input monitoring
    input_monitor = InputMonitor(loop, event_cooldown=1)  # Shorter cooldown for quicker responses
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
