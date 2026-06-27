# Tucker AI - Tablet AI Agent (Termux Only)

An AI agent that runs completely on your Android tablet using Termux. Controls apps, performs research, and executes tasks without needing a computer.

## 🎯 What Tucker Does

- **Controls your tablet apps** using Accessibility Services
- **Understands natural language** commands using AI
- **Performs research** by opening browsers and searching
- **Automates app interactions** - opening apps, navigating, tapping
- **Learns from screen content** using computer vision
- **Executes multi-step tasks** intelligently
- **Works entirely on your tablet** (optional: add AI for smarter decisions)

## 📋 Requirements

### Hardware
- Android tablet (API 24+)
- ~500MB free storage
- Internet connection (optional, for AI API)

### Software
- Termux app (from F-Droid or Play Store)
- Python 3.8+
- Git

## 🚀 Installation (Tablet Only)

### Step 1: Install Termux

1. Download **Termux** from:
   - F-Droid: https://f-droid.org/en/packages/com.termux/
   - Play Store: https://play.google.com/store/apps/details?id=com.termux

2. Open Termux app

### Step 2: Enable Accessibility Service (IMPORTANT!)

This is how Tucker will control your apps:

1. Open **Settings** on your tablet
2. Go to **Accessibility** (or **Accessibility Services**)
3. Find and enable **Accessibility Service for Termux** or any app automation service
4. Grant permissions when prompted

### Step 3: Install in Termux

Copy and paste this into Termux:

```bash
# Update packages
pkg update && pkg upgrade

# Install required packages
pkg install python git tesseract

# Create a directory for Tucker
mkdir -p ~/tucker
cd ~/tucker

# Clone the repository
git clone https://github.com/krikitthadev-spec/Tucker-ai.git
cd Tucker-ai

# Install Python dependencies
pip install -r requirements.txt
```

### Step 4: Get an API Key (Optional but Recommended)

For smarter AI, get a FREE API key:

**Option A: OpenAI (Free $5 credits)**
1. Go to https://platform.openai.com/api-keys
2. Create an account
3. Create an API key
4. Copy the key

**Option B: Anthropic Claude (Free tier)**
1. Go to https://console.anthropic.com/
2. Create an account
3. Get your API key

### Step 5: Configure Tucker

In Termux:

```bash
cd ~/tucker/Tucker-ai
cp .env.example .env
nano .env
```

Find these lines and add your API key:
```
OPENAI_API_KEY=sk_your_key_here
```

Press Ctrl+X, then Y to save.

### Step 6: Setup Permissions

```bash
termux-setup-storage
```

Answer "Allow" when prompted. This lets Tucker take screenshots and save files.

### Step 7: Start Tucker!

```bash
cd ~/tucker/Tucker-ai
python main.py
```

## 📚 Project Structure

```
Tucker-ai/
├── README.md                 # This file
├── requirements.txt          # Python dependencies
├── .env.example             # Example environment variables
├── main.py                  # Main entry point (RUN THIS!)
├── config.py                # Configuration settings
│
├── agents/
│   ├── ai_brain.py         # LLM interface (understands commands)
│   ├── tablet_controller.py # Accessibility Services controller
│   └── vision.py            # Screen analysis
│
├── tools/
│   ├── app_launcher.py     # Open apps
│   ├── web_search.py       # Search the web
│   ├── screen_capture.py   # Take screenshots
│   └── ui_automation.py    # Tap, swipe, type
│
└── examples/
    ├── simple_example.py    # Test setup
    ├── app_control_example.py # Control apps
    └── research_example.py  # Research topics
```

## 🎓 How It Works

```
1. You give Tucker a command
   "Search for Python tutorials"

2. Tucker's AI understands your command
   "I need to open a browser and search"

3. Tucker uses Accessibility Services
   - Opens Chrome
   - Taps the search bar
   - Types "Python tutorials"
   - Presses Enter

4. Tucker reads the results
   - Takes a screenshot
   - Analyzes what's on screen
   - Reports back to you
```

## 💻 Quick Start

### Test Your Setup

```bash
cd ~/tucker/Tucker-ai
python examples/simple_example.py
```

### Use Tucker (Interactive Mode)

```bash
python main.py
```

Then type commands like:
- `Open Chrome`
- `Search for Python`
- `Screenshot`
- `Open YouTube`
- `Help` (shows all commands)

### Example Commands

```
Tucker> Open Chrome
Tucker> Search for machine learning
Tucker> Open YouTube
Tucker> Screenshot
Tucker> Open Settings
```

## 🔧 Troubleshooting

### "ImportError: No module named..."

```bash
pip install -r requirements.txt --upgrade
```

### "Accessibility service not found"

Make sure you enabled it in Settings → Accessibility!

### "Permission denied"

In Termux, run:
```bash
termux-setup-storage
```

Then answer "Allow" when prompted.

### "Screenshot not saving"

Make sure storage permissions are granted:
```bash
termux-setup-storage
```

### Python not found

```bash
pkg install python
```

### Command "python" doesn't work

Try:
```bash
python3 main.py
```

Or create an alias:
```bash
echo 'alias python=python3' >> ~/.bashrc
source ~/.bashrc
```

## 📖 Learning Path

### Step 1: Test Basic Setup
```bash
python examples/simple_example.py
```

### Step 2: Try Simple Commands
```bash
python main.py
# Type: Open Chrome
```

### Step 3: Add an API Key
Get a free key from OpenAI and add it to `.env`

### Step 4: Learn the Code
Read the files in `agents/` and `tools/` folders

## 🤝 Common Commands

| Command | What it does |
|---------|--------------|
| `Open Chrome` | Opens Chrome browser |
| `Open YouTube` | Opens YouTube app |
| `Search for [topic]` | Searches Google for topic |
| `Screenshot` | Takes a screenshot |
| `Help` | Shows all commands |
| `Quit` | Exit Tucker |

## 🆘 Getting Help

**Problem: Commands not working**
1. Check Accessibility Service: Settings → Accessibility (must be ON)
2. Check Permissions: Run `termux-setup-storage`
3. Check Logs: Look in `logs/` folder in Termux

**Problem: Python not working**
```bash
# Reinstall Python
pkg install --reinstall python
```

**Problem: Git not working**
```bash
# Reinstall Git
pkg install --reinstall git
```

## 💡 Pro Tips

✅ **Enable Accessibility** - Settings → Accessibility (must be ON)
✅ **Grant Storage Permissions** - Run `termux-setup-storage`
✅ **Keep Termux Open** - Don't close the app while Tucker is running
✅ **Start Simple** - Learn the basics before advanced features
✅ **Get an API Key** - Free tier from OpenAI makes Tucker smarter
✅ **Use F-Droid** - More stable than Play Store for Termux

## 📝 License

MIT License - feel free to use and modify

---

## 🚀 Quick Setup Command

Copy and paste this entire thing into Termux to install everything at once:

```bash
pkg update && pkg upgrade && \
pkg install python git tesseract && \
mkdir -p ~/tucker && \
cd ~/tucker && \
git clone https://github.com/krikitthadev-spec/Tucker-ai.git && \
cd Tucker-ai && \
pip install -r requirements.txt && \
echo "✓ Installation complete! Run: python main.py"
```

---

**Ready to start?**

1. Install Termux
2. Enable Accessibility in Settings
3. Copy the setup command above into Termux
4. Run: `python main.py`

Enjoy! 🤖
