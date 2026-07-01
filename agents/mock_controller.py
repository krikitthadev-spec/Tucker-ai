"""Mock Tablet Controller - For testing without a real tablet.

Provides a simulated tablet interface for testing and development.
"""

from typing import Dict, List, Optional
from loguru import logger
from dataclasses import dataclass
from datetime import datetime

@dataclass
class TapEvent:
    """Record of a tap event."""
    x: int
    y: int
    timestamp: str

@dataclass
class TextEvent:
    """Record of a text input event."""
    text: str
    timestamp: str

class MockTabletController:
    """Mock tablet controller for testing."""
    
    def __init__(self, host: str = None, port: int = None):
        """Initialize mock controller.
        
        Args:
            host: Ignored (mock)
            port: Ignored (mock)
        """
        self.host = "mock"
        self.port = 0
        self.am_path = "am"
        self.is_connected = True
        
        # Track all actions for verification
        self.tap_history: List[TapEvent] = []
        self.text_history: List[TextEvent] = []
        self.key_presses: List[tuple] = []
        self.app_launches: List[str] = []
        self.swipe_history: List[tuple] = []
        self.screenshot_count = 0
        
        logger.info("✓ Mock TabletController initialized")
    
    def check_connection(self) -> bool:
        """Check connection (always true in mock mode)."""
        logger.info("✓ Mock tablet connected")
        return self.is_connected
    
    def shell(self, command: str) -> str:
        """Execute shell command (mock).
        
        Args:
            command: Shell command
            
        Returns:
            Mock output
        """
        logger.debug(f"[MOCK] Shell: {command}")
        
        # Return mock screen size for wm size command
        if 'wm size' in command:
            return "Physical size: 1080x1920"
        
        # Return mock app list for pm list packages
        if 'pm list packages' in command:
            return "package:com.android.chrome\npackage:com.google.android.youtube"
        
        return ""
    
    def tap(self, x: int, y: int) -> bool:
        """Record tap event (mock).
        
        Args:
            x: X coordinate
            y: Y coordinate
            
        Returns:
            True (always successful)
        """
        event = TapEvent(x=x, y=y, timestamp=datetime.now().isoformat())
        self.tap_history.append(event)
        logger.debug(f"[MOCK] Tapped at ({x}, {y})")
        return True
    
    def type_text(self, text: str) -> bool:
        """Record text input (mock).
        
        Args:
            text: Text to type
            
        Returns:
            True (always successful)
        """
        event = TextEvent(text=text, timestamp=datetime.now().isoformat())
        self.text_history.append(event)
        logger.debug(f"[MOCK] Typed: {text}")
        return True
    
    def press_key(self, key: str) -> bool:
        """Record key press (mock).
        
        Args:
            key: Key name
            
        Returns:
            True (always successful)
        """
        self.key_presses.append((key, datetime.now().isoformat()))
        logger.debug(f"[MOCK] Pressed key: {key}")
        return True
    
    def swipe(self, x1: int, y1: int, x2: int, y2: int, duration: int = 500) -> bool:
        """Record swipe event (mock).
        
        Args:
            x1, y1: Start coordinates
            x2, y2: End coordinates
            duration: Duration in ms
            
        Returns:
            True (always successful)
        """
        self.swipe_history.append((x1, y1, x2, y2, duration, datetime.now().isoformat()))
        logger.debug(f"[MOCK] Swiped from ({x1}, {y1}) to ({x2}, {y2})")
        return True
    
    def take_screenshot(self, filename: str) -> bool:
        """Mock screenshot (create empty file).
        
        Args:
            filename: Where to save
            
        Returns:
            True (always successful)
        """
        try:
            # Create empty file to simulate screenshot
            with open(filename, 'w') as f:
                f.write(f"MOCK_SCREENSHOT_{self.screenshot_count}")
            self.screenshot_count += 1
            logger.debug(f"[MOCK] Screenshot saved to {filename}")
            return True
        except Exception as e:
            logger.error(f"Failed to create mock screenshot: {e}")
            return False
    
    def get_screen_info(self) -> Dict:
        """Get mock screen info.
        
        Returns:
            Dict with screen dimensions
        """
        return {'width': 1080, 'height': 1920, 'size': '1080x1920'}
    
    def get_action_history(self) -> Dict:
        """Get all recorded actions for verification.
        
        Returns:
            Dict with all action histories
        """
        return {
            'taps': self.tap_history,
            'text_inputs': self.text_history,
            'key_presses': self.key_presses,
            'swipes': self.swipe_history,
            'screenshots': self.screenshot_count
        }
    
    def reset_history(self):
        """Clear all action history."""
        self.tap_history.clear()
        self.text_history.clear()
        self.key_presses.clear()
        self.swipe_history.clear()
        self.screenshot_count = 0
        logger.debug("[MOCK] History cleared")
