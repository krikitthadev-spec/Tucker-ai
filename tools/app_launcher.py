"""App Launcher - Opens applications on the tablet.

Simple utility to launch apps by package name.
"""

from loguru import logger
from agents.tablet_controller import TabletController

class AppLauncher:
    """Launches applications on the tablet."""
    
    def __init__(self, controller: TabletController = None):
        """Initialize app launcher.
        
        Args:
            controller: TabletController instance
        """
        self.controller = controller or TabletController()
    
    def open_app(self, package_name: str) -> bool:
        """Open an app by package name.
        
        Args:
            package_name: App package name (e.g., com.android.chrome)
            
        Returns:
            True if successful
        """
        try:
            # Try using am start command with the Termux am binary
            cmd = f'{self.controller.am_path} start -n {package_name}/{package_name}.MainActivity'
            output = self.controller.shell(cmd)
            logger.info(f"Launched app: {package_name}")
            return True
        except Exception as e:
            logger.error(f"Failed to launch app {package_name}: {e}")
            return False
    
    def open_chrome(self) -> bool:
        """Open Google Chrome."""
        return self.open_app('com.android.chrome')
    
    def open_youtube(self) -> bool:
        """Open YouTube."""
        return self.open_app('com.google.android.youtube')
    
    def open_google_search(self) -> bool:
        """Open Google Search."""
        return self.open_app('com.google.android.googlequicksearchbox')
    
    def close_app(self, package_name: str) -> bool:
        """Close an app.
        
        Args:
            package_name: App package name
            
        Returns:
            True if successful
        """
        try:
            self.controller.shell(f'{self.controller.am_path} force-stop {package_name}')
            logger.info(f"Closed app: {package_name}")
            return True
        except Exception as e:
            logger.error(f"Failed to close app {package_name}: {e}")
            return False
    
    def list_installed_apps(self) -> list:
        """List all installed apps.
        
        Returns:
            List of package names
        """
        try:
            output = self.controller.shell('pm list packages')
            apps = [line.replace('package:', '') for line in output.split('\n')]
            return [app for app in apps if app]
        except Exception as e:
            logger.error(f"Failed to list apps: {e}")
            return []

if __name__ == '__main__':
    launcher = AppLauncher()
    print("Installed apps:")
    for app in launcher.list_installed_apps():
        print(f"  - {app}")
