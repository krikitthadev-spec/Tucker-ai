"""Tablet Controller - Controls the tablet via ADB.

Handles all communication with the tablet through Android Debug Bridge.
This is how Tucker actually interacts with your tablet.
"""

import subprocess
import os
from typing import List, Optional
from loguru import logger
from config import Config

class TabletController:
    """Controls tablet via ADB commands."""
    
    def __init__(self, host: str = None, port: int = None):
        """Initialize tablet controller.
        
        Args:
            host: ADB host (localhost for USB, IP for WiFi)
            port: ADB port
        """
        self.host = host or Config.ADB_HOST
        self.port = port or Config.ADB_PORT
        self.adb_cmd = self._find_adb()
        
        if not self.adb_cmd:
            raise Exception("ADB not found! Install it with: pkg install adb")
        
        logger.info(f"TabletController initialized with ADB: {self.adb_cmd}")
    
    def _find_adb(self) -> Optional[str]:
        """Find ADB executable."""
        # Try common locations
        common_paths = [
            'adb',
            '/usr/bin/adb',
            '/data/data/com.termux/files/usr/bin/adb',
        ]
        
        for path in common_paths:
            try:
                result = subprocess.run([path, '--version'], 
                                      capture_output=True, 
                                      text=True)
                if result.returncode == 0:
                    return path
            except FileNotFoundError:
                continue
        
        return None
    
    def _run_adb(self, *args) -> str:
        """Run an ADB command.
        
        Args:
            *args: Arguments to pass to adb
            
        Returns:
            Command output as string
        """
        cmd = [self.adb_cmd] + list(args)
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            
            if result.returncode != 0:
                logger.error(f"ADB error: {result.stderr}")
                return ""
            
            return result.stdout.strip()
        except subprocess.TimeoutExpired:
            logger.error("ADB command timed out")
            return ""
        except Exception as e:
            logger.error(f"Failed to run ADB command: {e}")
            return ""
    
    def check_connection(self) -> bool:
        """Check if tablet is connected.
        
        Returns:
            True if connected, False otherwise
        """
        output = self._run_adb('devices')
        connected = 'device' in output and 'offline' not in output
        
        if connected:
            logger.info("✓ Tablet connected!")
        else:
            logger.warning("✗ Tablet not connected")
        
        return connected
    
    def shell(self, command: str) -> str:
        """Execute shell command on tablet.
        
        Args:
            command: Shell command to execute
            
        Returns:
            Command output
        """
        return self._run_adb('shell', command)
    
    def tap(self, x: int, y: int) -> bool:
        """Tap at coordinates on tablet screen.
        
        Args:
            x: X coordinate
            y: Y coordinate
            
        Returns:
            True if successful
        """
        self.shell(f'input tap {x} {y}')
        logger.debug(f"Tapped at ({x}, {y})")
        return True
    
    def type_text(self, text: str) -> bool:
        """Type text on tablet.
        
        Args:
            text: Text to type
            
        Returns:
            True if successful
        """
        # Escape special characters
        text = text.replace('"', '\\"')
        text = text.replace(' ', '%s')  # ADB needs spaces as %s
        
        self.shell(f'input text {text}')
        logger.debug(f"Typed text: {text}")
        return True
    
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
        
        self.shell(f'input keyevent {code}')
        logger.debug(f"Pressed key: {key}")
        return True
    
    def swipe(self, x1: int, y1: int, x2: int, y2: int, duration: int = 500) -> bool:
        """Swipe on tablet screen.
        
        Args:
            x1, y1: Start coordinates
            x2, y2: End coordinates
            duration: Swipe duration in ms
            
        Returns:
            True if successful
        """
        self.shell(f'input swipe {x1} {y1} {x2} {y2} {duration}')
        logger.debug(f"Swiped from ({x1}, {y1}) to ({x2}, {y2})")
        return True
    
    def take_screenshot(self, filename: str) -> bool:
        """Take a screenshot on the tablet.
        
        Args:
            filename: Where to save the screenshot
            
        Returns:
            True if successful
        """
        tablet_path = '/sdcard/tucker_screenshot.png'
        
        # Take screenshot on tablet
        self.shell(f'screencap -p {tablet_path}')
        
        # Pull to computer
        try:
            self._run_adb('pull', tablet_path, filename)
            logger.info(f"Screenshot saved to {filename}")
            return True
        except Exception as e:
            logger.error(f"Failed to pull screenshot: {e}")
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
