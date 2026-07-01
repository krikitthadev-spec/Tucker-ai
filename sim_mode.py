#!/usr/bin/env python3
"""Tucker AI - Simulation Mode

Run Tucker in simulation mode for testing without a real tablet.
"""

import time
import sys
from loguru import logger
from config import Config
from agents.mock_controller import MockTabletController
from agents.ai_brain import AIBrain
from tools.screen_capture import ScreenCapture
from tools.app_launcher import AppLauncher

# Configure logging
logger.remove()
logger.add(sys.stderr, level="INFO", format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan> - <level>{message}</level>")
logger.add(Config.LOGS_DIR / "tucker_sim.log", level="DEBUG")

class TuckerAISim:
    """Tucker AI in simulation mode."""
    
    def __init__(self):
        """Initialize Tucker AI simulator."""
        logger.info("🤖 Initializing Tucker AI (SIMULATION MODE)...")
        
        self.tablet = MockTabletController()
        self.brain = AIBrain()
        self.launcher = AppLauncher(self.tablet)
        
        logger.info("✓ Tucker AI Simulator ready!")
    
    def check_ready(self) -> bool:
        """Check if simulator is ready."""
        if not self.tablet.check_connection():
            logger.error("✗ Simulation failed to initialize")
            return False
        
        logger.info("✓ Simulation ready")
        return True
    
    def execute_command(self, command: str) -> bool:
        """Execute a command in simulation mode.
        
        Args:
            command: User command
            
        Returns:
            True if successful
        """
        logger.info(f">>> [SIM] Executing: {command}")
        
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
            activity = result.get('activity')
            logger.info(f"[SIM] Opening app: {app}")
            if activity:
                self.launcher.open_app(app, activity)
            else:
                self.launcher.open_app(app)
            time.sleep(0.5)  # Faster in simulation
        
        elif action == 'search':
            query = result.get('query')
            logger.info(f"[SIM] Searching for: {query}")
            self.launcher.open_chrome()
            time.sleep(0.2)
            self.tablet.tap(540, 100)
            time.sleep(0.1)
            self.tablet.type_text(query)
            time.sleep(0.1)
            self.tablet.press_key('ENTER')
        
        elif action == 'tap':
            x = result.get('x')
            y = result.get('y')
            logger.info(f"[SIM] Tapping at ({x}, {y})")
            self.tablet.tap(x, y)
        
        elif action == 'type':
            text = result.get('text')
            logger.info(f"[SIM] Typing: {text}")
            self.tablet.type_text(text)
        
        elif action == 'screenshot':
            logger.info("[SIM] Taking screenshot")
            self.tablet.take_screenshot('/tmp/sim_screenshot.png')
        
        logger.info("✓ [SIM] Command executed")
        return True
    
    def run_test_sequence(self):
        """Run a sequence of test commands."""
        logger.info("\n=== Running Test Sequence ===")
        
        test_commands = [
            "Take a screenshot",
            "Open Chrome",
            "Open YouTube",
            "Search for Python",
        ]
        
        for cmd in test_commands:
            logger.info(f"\n[TEST] {cmd}")
            self.execute_command(cmd)
            time.sleep(0.5)
        
        self._print_action_history()
        logger.info("\n✓ Test sequence complete!")
    
    def _print_action_history(self):
        """Print action history for verification."""
        history = self.tablet.get_action_history()
        
        logger.info("\n=== Action History ===")
        logger.info(f"Taps: {len(history['taps'])}")
        for tap in history['taps']:
            logger.info(f"  - ({tap.x}, {tap.y})")
        
        logger.info(f"Text Inputs: {len(history['text_inputs'])}")
        for text in history['text_inputs']:
            logger.info(f"  - {text.text}")
        
        logger.info(f"Key Presses: {len(history['key_presses'])}")
        for key, _ in history['key_presses']:
            logger.info(f"  - {key}")
        
        logger.info(f"Swipes: {len(history['swipes'])}")
        logger.info(f"Screenshots: {history['screenshots']}")
    
    def interactive_sim_mode(self):
        """Run interactive simulation mode."""
        logger.info("\n=== Tucker AI - Simulation Mode (Interactive) ===")
        logger.info("Commands (same as normal mode):")
        logger.info("  - Open [app name]")
        logger.info("  - Search for [query]")
        logger.info("  - Screenshot")
        logger.info("  - Test (run test sequence)")
        logger.info("  - History (show action history)")
        logger.info("  - Help")
        logger.info("  - Quit\n")
        
        while True:
            try:
                command = input("[SIM] Tucker> ").strip()
                
                if not command:
                    continue
                
                if command.lower() == 'quit':
                    logger.info("👋 Simulation ended")
                    break
                
                elif command.lower() == 'help':
                    logger.info("\nAvailable commands:")
                    logger.info("  Open Chrome / Open YouTube")
                    logger.info("  Search for [topic]")
                    logger.info("  Screenshot")
                    logger.info("  Test - run full test sequence")
                    logger.info("  History - show action history")
                    logger.info()
                
                elif command.lower() == 'test':
                    self.run_test_sequence()
                
                elif command.lower() == 'history':
                    self._print_action_history()
                
                else:
                    self.execute_command(command)
            
            except KeyboardInterrupt:
                logger.info("\n👋 Simulation interrupted")
                break
            except Exception as e:
                logger.error(f"Error: {e}")

def main():
    """Main entry point for simulation mode."""
    try:
        logger.info("\n🎮 Tucker AI - Simulation Mode")
        logger.info("(No real tablet needed - perfect for testing!)\n")
        
        sim = TuckerAISim()
        
        if not sim.check_ready():
            logger.error("Simulation setup failed")
            return
        
        # Run test sequence first, then interactive mode
        sim.run_test_sequence()
        sim.interactive_sim_mode()
    
    except KeyboardInterrupt:
        logger.info("\n👋 Simulation ended")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
