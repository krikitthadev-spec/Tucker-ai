"""Tests for TabletController."""

import pytest
from agents.mock_controller import MockTabletController

def test_check_connection():
    """Test connection check."""
    controller = MockTabletController()
    
    result = controller.check_connection()
    
    assert result == True

def test_tap():
    """Test tap functionality."""
    controller = MockTabletController()
    
    result = controller.tap(100, 200)
    
    assert result == True
    assert len(controller.tap_history) == 1
    assert controller.tap_history[0].x == 100
    assert controller.tap_history[0].y == 200

def test_type_text():
    """Test text input."""
    controller = MockTabletController()
    
    result = controller.type_text("hello world")
    
    assert result == True
    assert len(controller.text_history) == 1
    assert controller.text_history[0].text == "hello world"

def test_press_key():
    """Test key press."""
    controller = MockTabletController()
    
    result = controller.press_key('ENTER')
    
    assert result == True
    assert len(controller.key_presses) == 1
    assert controller.key_presses[0][0] == 'ENTER'

def test_swipe():
    """Test swipe functionality."""
    controller = MockTabletController()
    
    result = controller.swipe(100, 100, 200, 200, duration=500)
    
    assert result == True
    assert len(controller.swipe_history) == 1
    assert controller.swipe_history[0][0] == 100
    assert controller.swipe_history[0][1] == 100
    assert controller.swipe_history[0][2] == 200
    assert controller.swipe_history[0][3] == 200

def test_screenshot():
    """Test screenshot functionality."""
    controller = MockTabletController()
    
    result = controller.take_screenshot('/tmp/test_screenshot.png')
    
    assert result == True
    assert controller.screenshot_count == 1

def test_get_action_history():
    """Test action history tracking."""
    controller = MockTabletController()
    
    controller.tap(100, 200)
    controller.type_text("test")
    controller.press_key('ENTER')
    controller.swipe(10, 20, 30, 40)
    
    history = controller.get_action_history()
    
    assert len(history['taps']) == 1
    assert len(history['text_inputs']) == 1
    assert len(history['key_presses']) == 1
    assert len(history['swipes']) == 1

def test_reset_history():
    """Test history reset."""
    controller = MockTabletController()
    
    controller.tap(100, 200)
    controller.type_text("test")
    
    controller.reset_history()
    
    history = controller.get_action_history()
    assert len(history['taps']) == 0
    assert len(history['text_inputs']) == 0
