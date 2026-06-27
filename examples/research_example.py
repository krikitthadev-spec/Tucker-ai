#!/usr/bin/env python3
"""Research Example - Having Tucker research a topic.

This example shows Tucker performing research by:
- Opening a browser
- Searching for a topic
- Analyzing results
"""

import time
from agents.tablet_controller import TabletController
from agents.ai_brain import AIBrain
from tools.app_launcher import AppLauncher
from tools.web_search import WebSearch
from tools.screen_capture import ScreenCapture
from agents.vision import VisionProcessor

print("🤖 Tucker AI - Research Example\n")

print("Initializing...")
tablet = TabletController()
if not tablet.check_connection():
    print("Tablet not connected!")
    exit(1)

research_topic = "Machine Learning"
print(f"\nResearching: {research_topic}\n")

print("1. Opening browser...")
launcher = AppLauncher(tablet)
launcher.open_chrome()
time.sleep(3)

print("\n2. Searching...")
search = WebSearch(tablet)
search.google_search(research_topic)
time.sleep(5)

print("\n3. Taking screenshot of results...")
screen = ScreenCapture(tablet)
screenshot_path = screen.take_screenshot(f"research_{research_topic.replace(' ', '_')}.png")

print("\n4. Analyzing results...")
vision = VisionProcessor()
analysis = vision.analyze_screenshot(screenshot_path)

if analysis.get('success'):
    print(f"   Text found: {analysis['text'][:200]}...")
else:
    print("   Could not analyze image")

print(f"\n✓ Research complete! Results saved to: {screenshot_path}")
