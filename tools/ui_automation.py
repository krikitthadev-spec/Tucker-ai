"""UI Automation - Automates user interface interactions.

Higher-level UI automation like scrolling, form filling, etc.
"""

import time
from loguru import logger
from agents.tablet_controller import TabletController

class UIAutomation:
    """Automates UI interactions on the tablet."""
    
    def __init__(self, controller: TabletController = None):
        """Initialize UI automation.
        
        Args:
            controller: TabletController instance
        """
        self.controller = controller or TabletController()
    
    def scroll_down(self, distance: int = 500, duration: int = 500) -> bool:
        """Scroll down on the screen.
        
        Args:
            distance: Distance to scroll
            duration: Duration in ms
            
        Returns:
            True if successful
        """
        screen = self.controller.get_screen_info()
        width = screen.get('width', 1080)
        height = screen.get('height', 1920)
        
        start_y = height // 2
        end_y = start_y - distance
        
        self.controller.swipe(width // 2, start_y, width // 2, end_y, duration)
        logger.debug(f"Scrolled down by {distance}px")
        return True
    
    def scroll_up(self, distance: int = 500, duration: int = 500) -> bool:
        """Scroll up on the screen.
        
        Args:
            distance: Distance to scroll
            duration: Duration in ms
            
        Returns:
            True if successful
        """
        screen = self.controller.get_screen_info()
        width = screen.get('width', 1080)
        height = screen.get('height', 1920)
        
        start_y = height // 2
        end_y = start_y + distance
        
        self.controller.swipe(width // 2, start_y, width // 2, end_y, duration)
        logger.debug(f"Scrolled up by {distance}px")
        return True
    
    def fill_form(self, fields: list) -> bool:
        """Fill a form with multiple fields.
        
        Args:
            fields: List of tuples (x, y, text)
            
        Returns:
            True if successful
        """
        for x, y, text in fields:
            self.controller.tap(x, y)
            time.sleep(0.3)
            self.controller.type_text(text)
            time.sleep(0.2)
        
        logger.info(f"Filled form with {len(fields)} fields")
        return True
    
    def double_tap(self, x: int, y: int) -> bool:
        """Double tap at coordinates.
        
        Args:
            x, y: Coordinates
            
        Returns:
            True if successful
        """
        self.controller.tap(x, y)
        time.sleep(0.1)
        self.controller.tap(x, y)
        logger.debug(f"Double tapped at ({x}, {y})")
        return True
    
    def long_press(self, x: int, y: int, duration: int = 1000) -> bool:
        """Long press at coordinates.
        
        Args:
            x, y: Coordinates
            duration: Press duration in ms
            
        Returns:
            True if successful
        """
        # Use swipe with same start and end point for long press
        self.controller.swipe(x, y, x, y, duration)
        logger.debug(f"Long pressed at ({x}, {y}) for {duration}ms")
        return True
    
    def go_home(self) -> bool:
        """Go to home screen.
        
        Returns:
            True if successful
        """
        self.controller.press_key('HOME')
        logger.info("Pressed HOME button")
        return True
    
    def go_back(self) -> bool:
        """Go back (press BACK button).
        
        Returns:
            True if successful
        """
        self.controller.press_key('BACK')
        logger.info("Pressed BACK button")
        return True

if __name__ == '__main__':
    automation = UIAutomation()
    print("UI Automation ready!")
