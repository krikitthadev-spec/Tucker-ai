"""Web Search - Performs web searches using the tablet.

Opens a browser and performs Google searches or other web queries.
"""

from loguru import logger
from agents.tablet_controller import TabletController
from tools.app_launcher import AppLauncher

class WebSearch:
    """Performs web searches on the tablet."""
    
    def __init__(self, controller: TabletController = None):
        """Initialize web search.
        
        Args:
            controller: TabletController instance
        """
        self.controller = controller or TabletController()
        self.launcher = AppLauncher(self.controller)
    
    def google_search(self, query: str) -> bool:
        """Perform a Google search.
        
        Args:
            query: Search query
            
        Returns:
            True if successful
        """
        logger.info(f"Searching Google for: {query}")
        
        # Open Chrome
        self.launcher.open_chrome()
        
        # Wait for app to open
        import time
        time.sleep(2)
        
        # Tap on search bar (adjust coordinates for your tablet)
        self.controller.tap(540, 100)
        time.sleep(0.5)
        
        # Type search query
        self.controller.type_text(query)
        time.sleep(0.5)
        
        # Press Enter to search
        self.controller.press_key('ENTER')
        
        logger.info("✓ Search executed")
        return True
    
    def youtube_search(self, query: str) -> bool:
        """Search YouTube.
        
        Args:
            query: Search query
            
        Returns:
            True if successful
        """
        logger.info(f"Searching YouTube for: {query}")
        
        # Open YouTube
        self.launcher.open_youtube()
        
        # Wait for app to open
        import time
        time.sleep(2)
        
        # Tap on search button (YouTube search icon)
        self.controller.tap(900, 50)
        time.sleep(0.5)
        
        # Type search query
        self.controller.type_text(query)
        time.sleep(0.5)
        
        # Press Enter
        self.controller.press_key('ENTER')
        
        logger.info("✓ YouTube search executed")
        return True

if __name__ == '__main__':
    search = WebSearch()
    search.google_search("Python tutorials")
