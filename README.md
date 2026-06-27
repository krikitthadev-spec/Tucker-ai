# Tucker AI - Tablet AI Agent

An AI agent that can control your tablet, open apps, perform research, and execute tasks autonomously.

## 🎯 What Tucker Does

- **Controls your tablet** via ADB (Android Debug Bridge)
- **Understands natural language** commands using AI
- **Performs research** by opening browsers and searching
- **Automates app interactions** - opening apps, navigating, tapping
- **Learns from screen content** using computer vision
- **Executes multi-step tasks** intelligently

## 📋 Requirements

### Hardware
- Android tablet with USB debugging enabled (or WiFi ADB)
- Computer/Termux environment running Tucker
- USB cable (for initial setup)

### Software
- Python 3.8+
- ADB (Android Debug Bridge)
- Git

## 🚀 Installation

### Step 1: Enable USB Debugging on Your Tablet

1. Open **Settings** on your tablet
2. Go to **About Tablet**
3. Tap **Build Number** 7 times (until it says "You are a developer")
4. Go back to Settings → **Developer Options**
5. Enable **USB Debugging**
6. (Optional) Enable **TCP/IP Debugging** for wireless connection

### Step 2: Install in Termux

```bash
# Update Termux packages
pkg update && pkg upgrade

# Install required packages
pkg install python git adb

# Clone this repository
git clone https://github.com/krikitthadev-spec/Tucker-ai.git
cd Tucker-ai

# Install Python dependencies
pip install -r requirements.txt
```

### Step 3: Connect Your Tablet

**Using USB Cable:**
```bash
adb devices
```
You should see your tablet listed.

**Using WiFi (after USB initial setup):**
```bash
# On your tablet (from adb shell):
adb shell setprop service.adb.tcp.port 5555
adb shell stop adbd
adb shell start adbd

# On your computer/Termux:
adb connect <TABLET_IP_ADDRESS>:5555
```

### Step 4: Get an API Key (Optional but Recommended)

For the AI to work better, get a free API key:
- **OpenAI**: https://platform.openai.com/api-keys (free $5 credits)
- **Anthropic Claude**: https://console.anthropic.com/
- **Hugging Face**: https://huggingface.co/ (free local models)

Create a `.env` file:
```bash
cp .env.example .env
# Edit .env and add your API key
```

## 📚 Project Structure

```
Tucker-ai/
├── README.md                 # This file
├── requirements.txt          # Python dependencies
├── .env.example             # Example environment variables
├── main.py                  # Main entry point
├── config.py                # Configuration settings
├── 
├── agents/
│   ├── __init__.py
│   ├── ai_brain.py         # LLM interface (the AI logic)
│   ├── tablet_controller.py # ADB commands (controls tablet)
│   └── vision.py            # Screen analysis
│
├── tools/
│   ├── __init__.py
│   ├── app_launcher.py     # Open apps
│   ├── web_search.py       # Search the web
│   ├── screen_capture.py   # Take screenshots
│   └── ui_automation.py    # Tap, swipe, type
│
└── examples/
    ├── simple_example.py    # Basic usage
    ├── research_example.py  # Research task
    └── app_control_example.py # App control
```

## 🎓 How It Works (Simple Version)

```
1. You give Tucker a command (voice or text)
   Example: "Search for Python tutorials"

2. Tucker's AI Brain reads your command
   "I need to open a browser and search"

3. Tucker controls your tablet
   - Opens Chrome
   - Taps the search bar
   - Types "Python tutorials"
   - Presses Enter

4. Tucker reads the results
   - Takes a screenshot
   - Analyzes what's on screen
   - Reports back to you
   "I found 10 Python tutorials. Would you like me to open one?"
```

## 💻 Quick Start Examples

### Basic Setup Test
```bash
python examples/simple_example.py
```

### Open an App
```bash
python -c "
from tools.app_launcher import AppLauncher
launcher = AppLauncher()
launcher.open_app('com.android.chrome')  # Opens Chrome
"
```

### Take a Screenshot
```bash
python -c "
from tools.screen_capture import ScreenCapture
capture = ScreenCapture()
capture.take_screenshot('screenshot.png')
"
```

### Use the AI Brain
```bash
python -c "
from agents.ai_brain import AIBrain
brain = AIBrain()
result = brain.process_command('Open YouTube')
print(result)
"
```

## 🛠️ Troubleshooting

### ADB Not Found
```bash
# Install ADB
pkg install adb

# Or add to PATH
export PATH=$PATH:/path/to/adb
```

### Tablet Not Detected
```bash
# Check connection
adb devices

# Restart ADB
adb kill-server
adb start-server
```

### Python Module Errors
```bash
# Reinstall dependencies
pip install -r requirements.txt --upgrade
```

### Permission Denied
Make sure USB Debugging is enabled on your tablet and you've authorized the connection.

## 🔐 Security Notes

- **Never** commit your `.env` file with API keys
- Keep your API keys private
- Be careful with tablet automation - it can trigger unintended actions
- Always test with simple commands first

## 📖 Learning Resources

- [ADB Documentation](https://developer.android.com/studio/command-line/adb)
- [OpenAI API Guide](https://platform.openai.com/docs)
- [Python Automation](https://docs.python.org/3/library/subprocess.html)

## 🤝 Contributing

Found a bug or have ideas? Create an issue or submit a pull request!

## 📝 License

MIT License - feel free to use and modify

## 🆘 Need Help?

1. Check the `examples/` folder for working code
2. Read through the comments in each Python file
3. Test each component separately first
4. Join Python communities (Reddit, Discord, GitHub)

---

**Remember**: Start simple! Get ADB working first, then add AI features gradually.

Happy coding! 🚀