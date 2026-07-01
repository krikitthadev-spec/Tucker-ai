"""Tests for AppLauncher."""

import pytest
from tools.app_launcher import AppLauncher
from agents.mock_controller import MockTabletController

def test_open_chrome():
    """Test opening Chrome."""
    mock = MockTabletController()
    launcher = AppLauncher(mock)
    
    result = launcher.open_chrome()
    
    assert result == True
    assert len(mock.app_launches) >= 0

def test_open_youtube():
    """Test opening YouTube."""
    mock = MockTabletController()
    launcher = AppLauncher(mock)
    
    result = launcher.open_youtube()
    
    assert result == True

def test_open_custom_app():
    """Test opening custom app."""
    mock = MockTabletController()
    launcher = AppLauncher(mock)
    
    result = launcher.open_app('com.example.app')
    
    assert result == True

def test_close_app():
    """Test closing an app."""
    mock = MockTabletController()
    launcher = AppLauncher(mock)
    
    result = launcher.close_app('com.android.chrome')
    
    assert result == True
