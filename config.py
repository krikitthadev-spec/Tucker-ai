"""Configuration file for Tucker AI.

Loads settings from environment variables and .env file.
Modify this file to customize Tucker's behavior.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Configuration settings for Tucker AI."""
    
    # Project Paths
    PROJECT_ROOT = Path(__file__).parent
    LOGS_DIR = PROJECT_ROOT / "logs"
    SCREENSHOTS_DIR = PROJECT_ROOT / "screenshots"
    DATA_DIR = PROJECT_ROOT / "data"
    
    # Create directories if they don't exist
    LOGS_DIR.mkdir(exist_ok=True)
    SCREENSHOTS_DIR.mkdir(exist_ok=True)
    DATA_DIR.mkdir(exist_ok=True)
    
    # API Keys
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
    
    # ADB Configuration
    ADB_PORT = int(os.getenv("ADB_PORT", "5037"))
    ADB_HOST = os.getenv("ADB_HOST", "localhost")
    TABLET_IP = os.getenv("TABLET_IP", "192.168.1.100")
    TABLET_PORT = int(os.getenv("TABLET_PORT", "5555"))
    
    # AI Configuration
    AI_MODEL = os.getenv("AI_MODEL", "gpt-3.5-turbo")
    AI_TEMPERATURE = float(os.getenv("AI_TEMPERATURE", "0.7"))
    AI_MAX_TOKENS = int(os.getenv("AI_MAX_TOKENS", "1000"))
    
    # App Package Names
    BROWSER_APP = os.getenv("BROWSER_APP", "com.android.chrome")
    YOUTUBE_APP = os.getenv("YOUTUBE_APP", "com.google.android.youtube")
    SEARCH_ENGINE = os.getenv("SEARCH_ENGINE", "com.google.android.googlequicksearchbox")
    
    # Debug Settings
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    DEBUG_SCREENSHOTS = os.getenv("DEBUG_SCREENSHOTS", "False").lower() == "true"
    
    @classmethod
    def validate(cls):
        """Validate configuration."""
        if not cls.OPENAI_API_KEY and not cls.ANTHROPIC_API_KEY:
            print("⚠️ Warning: No API key configured.")
            print("Add OPENAI_API_KEY or ANTHROPIC_API_KEY to .env file for AI features.")
            print("You can still use basic tablet control without an API key.")

# Validate on import
Config.validate()
