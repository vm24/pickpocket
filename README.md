🖱️ Mouse, Keyboard, and Charger Activity Reporter
Overview
This Python script serves as a security and activity tracker for your computer. It continuously monitors your system for mouse movements, key presses, and charger plug/unplug events, and reports them to a specified Telegram user. Perfect for situations where you leave your device unattended in public spaces, study halls, or shared environments. Stay aware of any activity happening on your device in real-time!

🚀 Features
Real-Time Mouse Movement Tracking
Detects and logs every movement of your mouse, keeping you informed of any activity.

Key Press Detection
Monitors and reports all key presses made while the script is running. Never miss a keystroke.

Charger Plug/Unplug Monitoring
Sends a notification whenever your charger is plugged in or unplugged, helping you keep track of your device's power status.

Instant Telegram Notifications
Get real-time alerts directly to your Telegram account. Always stay in control, no matter where you are.

Perfect for Public Places & Shared Environments
Whether you’re in a café, library, or study hall, you’ll know if anyone is interacting with your device while you're away.

🛠️ Installation
Clone the repository:

bash
Copy code
git clone https://github.com/yourusername/Activity-Reporter.git
Navigate to the project directory:

bash
Copy code
cd Activity-Reporter
Install dependencies: The following Python libraries are required to run the script:

bash
Copy code
pip install pynput psutil telethon
Set up Telegram Bot:

Create a new bot using BotFather.
Get your bot token from BotFather.
Retrieve your Telegram User ID by messaging @userinfobot on Telegram.
Replace YOUR_BOT_TOKEN and TARGET_USER_ID in the script with your actual bot token and user ID.
⚡ Usage
Run the Script:

Open a terminal/command prompt and execute the script:

bash
Copy code
python pickpocket.py
Monitoring Starts:
The script will continuously monitor the mouse, keyboard, and charger activity, sending updates to your Telegram account. To stop the monitoring, press Ctrl+C.

Telegram Notifications:
Whenever a mouse movement, key press, or charger event occurs, you'll receive an instant notification on your Telegram account.

⚙️ Configuration
Telegram Notifications:
All messages (mouse movements, key presses, charger events) will be sent to your Telegram. You can easily customize the message format by editing the send_message() function in the script.

Polling Interval:
The script uses asyncio to handle multiple tasks. You can adjust the frequency or the data captured by modifying the polling functions within the script.

🧑‍💻 Code Walkthrough
Mouse and Keyboard Listener:
Uses the pynput library to capture real-time mouse movements and key presses. Each event triggers a notification.

Charger Monitoring:
Uses the psutil library to detect when the charger is plugged in or unplugged, and sends a message accordingly.

Telegram Integration:
Utilizes the telethon library to send messages to your Telegram account. The bot runs asynchronously, sending updates whenever an event occurs.

📸 Webcam Snapshot (Optional)
If you'd like the script to send webcam snapshots with each event, you can easily integrate a webcam capture function into the existing workflow. We can modify the script to capture and send images from your webcam using libraries like opencv-python.

🔧 Troubleshooting
Missing Dependencies:
If you encounter issues with missing libraries, try running:

bash
Copy code
pip install -r requirements.txt
(Make sure all necessary dependencies are listed in the requirements.txt file.)

Telegram Bot Not Responding:
Ensure that the bot token and user ID are correctly set in the script. If issues persist, check if Telegram API services are up and running.

Event Listener Issues:
If you experience issues with the event listeners (e.g., key presses or mouse movements not being detected), make sure you have the necessary permissions to run the script and access your hardware resources.

📚 License
This project is licensed under the MIT License - see the LICENSE file for details.

📞 Contact
If you have any questions or feedback, feel free to reach out via GitHub Issues or email.

📝 Notes
Privacy:
Be mindful of privacy when using this script. Only monitor activities on your own personal devices, and ensure you have permission to monitor the environment where the script is deployed.
