#!/usr/bin/env python3
"""Simple Example - Basic Tucker AI usage.

This example shows the most basic Tucker features.
Run this first to test your setup!
"""

from agents.tablet_controller import TabletController
from tools.screen_capture import ScreenCapture
from tools.app_launcher import AppLauncher

print("🤖 Tucker AI - Simple Example\n")

print("1. Connecting to tablet...")
try:
    tablet = TabletController()
    if tablet.check_connection():
        print("   ✓ Connected!\n")
    else:
        print("   ✗ Not connected. Enable USB debugging on your tablet.\n")
        exit(1)
except Exception as e:
    print(f"   ✗ Error: {e}\n")
    exit(1)

print("2. Taking a screenshot...")
try:
    screen = ScreenCapture(tablet)
    path = screen.take_screenshot("example_screenshot.png")
    print(f"   ✓ Screenshot saved to: {path}\n")
except Exception as e:
    print(f"   ✗ Error: {e}\n")

print("3. Getting screen info...")
info = tablet.get_screen_info()
print(f"   Screen size: {info['width']}x{info['height']}\n")

print("4. Listing installed apps (first 10)...")
try:
    launcher = AppLauncher(tablet)
    apps = launcher.list_installed_apps()[:10]
    for app in apps:
        print(f"   - {app}")
    print()
except Exception as e:
    print(f"   ✗ Error: {e}\n")

print("✓ Simple example complete!")
print("Next, try: python main.py")
