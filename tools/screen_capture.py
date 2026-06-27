"""Screen Capture - Takes screenshots from the tablet.

Captures the tablet screen and saves to local files.
"""

from pathlib import Path
from loguru import logger
from config import Config
from agents.tablet_controller import TabletController

class ScreenCapture:
    """Captures screenshots from the tablet."""
    
    def __init__(self, controller: TabletController = None):
        """Initialize screen capture.
        
        Args:
            controller: TabletController instance
        """
        self.controller = controller or TabletController()
        self.screenshots_dir = Config.SCREENSHOTS_DIR
    
    def take_screenshot(self, filename: str = None) -> str:
        """Take a screenshot and save it.
        
        Args:
            filename: Output filename (auto-generated if not provided)
            
        Returns:
            Path to saved screenshot
        """
        if not filename:
            import datetime
            timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"screenshot_{timestamp}.png"
        
        filepath = self.screenshots_dir / filename
        
        self.controller.take_screenshot(str(filepath))
        
        if filepath.exists():
            logger.info(f"✓ Screenshot saved: {filepath}")
            return str(filepath)
        else:
            logger.error(f"✗ Failed to save screenshot")
            return None
    
    def get_recent_screenshot(self) -> str:
        """Get the most recent screenshot.
        
        Returns:
            Path to most recent screenshot
        """
        screenshots = sorted(self.screenshots_dir.glob('screenshot_*.png'),
                           key=lambda p: p.stat().st_mtime,
                           reverse=True)
        
        if screenshots:
            return str(screenshots[0])
        return None
    
    def clear_old_screenshots(self, keep_count: int = 10):
        """Delete old screenshots, keeping only recent ones.
        
        Args:
            keep_count: Number of screenshots to keep
        """
        screenshots = sorted(self.screenshots_dir.glob('screenshot_*.png'),
                           key=lambda p: p.stat().st_mtime,
                           reverse=True)
        
        to_delete = screenshots[keep_count:]
        for f in to_delete:
            f.unlink()
            logger.debug(f"Deleted old screenshot: {f.name}")

if __name__ == '__main__':
    capture = ScreenCapture()
    path = capture.take_screenshot()
    print(f"Screenshot saved to: {path}")
