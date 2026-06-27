"""Tablet Controller - Controls the tablet via Accessibility Services.

Handles all communication with the tablet through shell commands and accessibility services.
This version works when running Tucker directly on your tablet via Termux.
"""

import subprocess
import os
import time
from typing import List, Optional, Tuple
from loguru import logger
from config import Config

class TabletController:
    """Controls tablet via shell commands (works on Termux)."""
    
    def __init__(self, host: str = None, port: int = None):
        """Initialize tablet controller.
        
        Args:
            host: Not used in Termux mode
            port: Not used in Termux mode
        """
        self.host = host or "localhost"
        self.port = port or 5037
        logger.info("TabletController initialized (Termux mode - direct shell access)")
    
    def _run_shell(self, *args, check_output=False) -> str:
        """Run a shell command directly.
        
        Args:
            *args: Command arguments
            check_output: If True, return output
            
        Returns:
            Command output as string
        """
        cmd = list(args)
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            
            if result.returncode != 0 and check_output:
                logger.error(f"Shell error: {result.stderr}")
                return ""
            
            return result.stdout.strip()
        except subprocess.TimeoutExpired:
            logger.error("Command timed out")
            return ""
        except Exception as e:
            logger.error(f"Failed to run shell command: {e}")
            return ""
    
    def check_connection(self) -> bool:
        """Check if we can access the tablet (always true in Termux mode).
        
        Returns:
            True (always connected when running on tablet)
        """
        logger.info("✓ Tablet connected! (Running on Termux)")
        return True
    
    def shell(self, command: str) -> str:
        """Execute shell command directly on tablet.
        
        Args:
            command: Shell command to execute
            
        Returns:
            Command output
        """
        try:
            result = subprocess.run(['sh', '-c', command], 
                                  capture_output=True, 
                                  text=True, 
                                  timeout=10)
            return result.stdout.strip()
        except Exception as e:
            logger.error(f"Shell command failed: {e}")
            return ""
    
    def tap(self, x: int, y: int) -> bool:
        """Tap at coordinates on tablet screen using input command.
        
        Args:
            x: X coordinate
            y: Y coordinate
            
        Returns:
            True if successful
        """
        try:
            self.shell(f'input tap {x} {y}')
            logger.debug(f"Tapped at ({x}, {y})")
            return True
        except Exception as e:
            logger.error(f"Failed to tap: {e}")
            return False
    
    def type_text(self, text: str) -> bool:
        """Type text on tablet.
        
        Args:
            text: Text to type
            
        Returns:
            True if successful
        """
        try:
            # Escape special characters for shell
            text = text.replace('"', '\\"')
            text = text.replace("'", "\\'")
            
            # Use input text command
            self.shell(f'input text "{text}"')
            logger.debug(f"Typed text: {text}")
            return True
        except Exception as e:
            logger.error(f"Failed to type: {e}")
            return False
    
    def press_key(self, key: str) -> bool:
        """Press a key on the tablet.
        
        Args:
            key: Key name (BACK, HOME, POWER, ENTER, etc.)
            
        Returns:
            True if successful
        """
        key_codes = {
            'BACK': 4,
            'HOME': 3,
            'POWER': 26,
            'ENTER': 66,
            'SPACE': 62,
            'DEL': 67,
        }
        
        code = key_codes.get(key.upper())
        if not code:
            logger.warning(f"Unknown key: {key}")
            return False
        
        try:
            self.shell(f'input keyevent {code}')
            logger.debug(f"Pressed key: {key}")
            return True
        except Exception as e:
            logger.error(f"Failed to press key: {e}")
            return False
    
    def swipe(self, x1: int, y1: int, x2: int, y2: int, duration: int = 500) -> bool:
        """Swipe on tablet screen.
        
        Args:
            x1, y1: Start coordinates
            x2, y2: End coordinates
            duration: Swipe duration in ms
            
        Returns:
            True if successful
        """
        try:
            self.shell(f'input swipe {x1} {y1} {x2} {y2} {duration}')
            logger.debug(f"Swiped from ({x1}, {y1}) to ({x2}, {y2})")
            return True
        except Exception as e:
            logger.error(f"Failed to swipe: {e}")
            return False
    
    def take_screenshot(self, filename: str) -> bool:
        """Take a screenshot on the tablet (Termux mode).
        
        Args:
            filename: Where to save the screenshot
            
        Returns:
            True if successful
        """
        try:
            # In Termux, we can use screencap directly
            result = subprocess.run(['screencap', '-p', filename], 
                                  capture_output=True, 
                                  text=True,
                                  timeout=5)
            
            if result.returncode == 0:
                logger.info(f"Screenshot saved to {filename}")
                return True
            else:
                logger.error(f"Screenshot failed: {result.stderr}")
                return False
                
        except FileNotFoundError:
            logger.error("screencap not found. Try: pkg install scrcpy")
            return False
        except Exception as e:
            logger.error(f"Failed to take screenshot: {e}")
            return False
    
    def get_screen_info(self) -> dict:
        """Get information about tablet screen.
        
        Returns:
            Dict with screen dimensions and info
        """
        try:
            output = self.shell('wm size')
            # Output format: "Physical size: 1920x1080"
            if 'x' in output:
                size = output.split(':')[1].strip()
                width, height = map(int, size.split('x'))
                return {
                    'width': width,
                    'height': height,
                    'size': size
                }
        except Exception as e:
            logger.error(f"Failed to get screen info: {e}")
        
        return {'width': 1080, 'height': 1920}  # Default

if __name__ == '__main__':
    # Test the tablet controller
    try:
        controller = TabletController()
        print("Checking tablet connection...")
        if controller.check_connection():
            print("✓ Ready to control tablet!")
        else:
            print("✗ Tablet not connected")
    except Exception as e:
        print(f"Error: {e}")
