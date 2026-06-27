#!/usr/bin/env python3
"""App Control Example - Controlling apps on the tablet.

This example shows how to:
- Open apps
- Tap on buttons
- Type text
- Navigate
"""

import time
from agents.tablet_controller import TabletController
from tools.app_launcher import AppLauncher
from tools.ui_automation import UIAutomation

print("🤖 Tucker AI - App Control Example\n")

print("Initializing...")
tablet = TabletController()
if not tablet.check_connection():
    print("Tablet not connected!")
    exit(1)

launcher = AppLauncher(tablet)
automation = UIAutomation(tablet)

print("\n1. Opening Chrome...")
launcher.open_chrome()
time.sleep(3)
print("   ✓ Chrome opened")

print("\n2. Taking a screenshot...")
tablet.take_screenshot("example_chrome.png")
print("   ✓ Screenshot saved")

print("\n3. Going home...")
automation.go_home()
time.sleep(2)
print("   ✓ Back to home screen")

print("\n✓ App control example complete!")
