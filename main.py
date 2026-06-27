#!/usr/bin/env python3
"""Tucker AI - Main Entry Point

This is the main program that runs Tucker AI.
You can start Tucker from here!
"""

import time
import sys
from loguru import logger
from config import Config
from agents.tablet_controller import TabletController
from agents.ai_brain import AIBrain
from tools.screen_capture import ScreenCapture
from tools.app_launcher import AppLauncher

# Configure logging
logger.remove()  # Remove default handler
logger.add(sys.stderr, level="INFO", format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan> - <level>{message}</level>")
logger.add(Config.LOGS_DIR / "tucker.log", level="DEBUG")

class TuckerAI:
    """Main Tucker AI agent."""
    
    def __init__(self):
        """Initialize Tucker AI."""
        logger.info("🤖 Initializing Tucker AI...")
        
        self.tablet = TabletController()
        self.brain = AIBrain()
        self.screen = ScreenCapture()
        self.launcher = AppLauncher(self.tablet)
        
        logger.info("✓ Tucker AI ready!")
    
    def check_ready(self) -> bool:
        """Check if Tucker is ready to use.
        
        Returns:
            True if tablet is connected
        """
        if not self.tablet.check_connection():
            logger.error("✗ Tablet not connected")
            return False
        
        logger.info("✓ Tablet connected")
        return True
    
    def execute_command(self, command: str) -> bool:
        """Execute a command.
        
        Args:
            command: User command
            
        Returns:
            True if successful
        """
        logger.info(f">>> Executing: {command}")
        
        # Take screenshot for context
        screenshot = self.screen.take_screenshot()
        
        # Ask AI brain what to do
        result = self.brain.process_command(command)
        
        logger.info(f"AI Decision: {result}")
        
        if not result.get('success'):
            logger.warning(f"Failed: {result.get('reason')}")
            return False
        
        # Execute based on action
        action = result.get('action')
        
        if action == 'app_open':
            app = result.get('app')
            self.launcher.open_app(app)
            time.sleep(2)
        
        elif action == 'search':
            query = result.get('query')
            self.launcher.open_chrome()
            time.sleep(2)
            # Search
            self.tablet.tap(540, 100)  # Tap search bar
            time.sleep(0.3)
            self.tablet.type_text(query)
            time.sleep(0.3)
            self.tablet.press_key('ENTER')
        
        elif action == 'tap':
            x = result.get('x')
            y = result.get('y')
            self.tablet.tap(x, y)
        
        elif action == 'type':
            text = result.get('text')
            self.tablet.type_text(text)
        
        elif action == 'screenshot':
            path = self.screen.take_screenshot()
            logger.info(f"Screenshot saved to: {path}")
        
        logger.info("✓ Command executed")
        return True
    
    def interactive_mode(self):
        """Run in interactive mode where you can give commands."""
        logger.info("\n=== Tucker AI - Interactive Mode ===")
        logger.info("Commands:")
        logger.info("  - Open [app name]")
        logger.info("  - Search for [query]")
        logger.info("  - Screenshot")
        logger.info("  - Help")
        logger.info("  - Quit\n")
        
        while True:
            try:
                command = input("Tucker> ").strip()
                
                if not command:
                    continue
                
                if command.lower() == 'quit':
                    logger.info("👋 Goodbye!")
                    break
                
                elif command.lower() == 'help':
                    self._show_help()
                
                else:
                    self.execute_command(command)
            
            except KeyboardInterrupt:
                logger.info("\n👋 Interrupted. Goodbye!")
                break
            except Exception as e:
                logger.error(f"Error: {e}")
    
    def _show_help(self):
        """Show help information."""
        print("\n=== Tucker AI Help ===")
        print("Examples:")
        print("  Open Chrome          - Opens Chrome browser")
        print("  Open YouTube         - Opens YouTube app")
        print("  Search for Python    - Searches for 'Python' on Google")
        print("  Screenshot           - Takes a screenshot")
        print("  Help                 - Shows this help")
        print("  Quit                 - Exit Tucker")
        print()
    
    def demo_mode(self):
        """Run a demo showing Tucker's capabilities."""
        logger.info("\n=== Tucker AI - Demo Mode ===")
        
        commands = [
            "Take a screenshot",
            "Open Chrome",
        ]
        
        for cmd in commands:
            logger.info(f"\nDemo: {cmd}")
            self.execute_command(cmd)
            time.sleep(2)
        
        logger.info("\n✓ Demo complete!")

def main():
    """Main entry point."""
    try:
        tucker = TuckerAI()
        
        if not tucker.check_ready():
            logger.error("Tucker is not ready. Connect your tablet and enable USB debugging.")
            return
        
        # You can choose:
        # tucker.demo_mode()        # Show what Tucker can do
        tucker.interactive_mode()  # Let user give commands
    
    except KeyboardInterrupt:
        logger.info("\n👋 Goodbye!")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
