"""AI Brain - The AI that makes decisions.

This is the core AI that understands commands and plans actions.
You can swap different AI backends here (OpenAI, Claude, local models, etc.)
"""

import os
from typing import Optional, List, Dict
from loguru import logger
from config import Config

class AIBrain:
    """The AI brain that processes commands and makes decisions."""
    
    def __init__(self, model: str = None):
        """Initialize AI brain.
        
        Args:
            model: AI model to use (gpt-3.5-turbo, claude-2, etc.)
        """
        self.model = model or Config.AI_MODEL
        self.temperature = Config.AI_TEMPERATURE
        self.max_tokens = Config.AI_MAX_TOKENS
        self.api_backend = None
        
        self._initialize_backend()
        logger.info(f"AIBrain initialized with model: {self.model}")
    
    def _initialize_backend(self):
        """Initialize the appropriate AI backend."""
        if 'gpt' in self.model.lower():
            if not Config.OPENAI_API_KEY:
                logger.warning("OpenAI API key not found")
                return
            try:
                import openai
                openai.api_key = Config.OPENAI_API_KEY
                self.api_backend = 'openai'
                logger.info("✓ OpenAI backend ready")
            except ImportError:
                logger.error("OpenAI library not installed: pip install openai")
        
        elif 'claude' in self.model.lower():
            if not Config.ANTHROPIC_API_KEY:
                logger.warning("Anthropic API key not found")
                return
            try:
                import anthropic
                self.client = anthropic.Anthropic(api_key=Config.ANTHROPIC_API_KEY)
                self.api_backend = 'anthropic'
                logger.info("✓ Anthropic backend ready")
            except ImportError:
                logger.error("Anthropic library not installed: pip install anthropic")
        
        else:
            # Try local models
            try:
                from transformers import pipeline
                self.api_backend = 'local'
                logger.info("✓ Local model backend ready")
            except ImportError:
                logger.error("Transformers not installed: pip install transformers torch")
    
    def process_command(self, user_input: str, context: str = "") -> Dict:
        """Process a user command and return action plan.
        
        Args:
            user_input: The user's command
            context: Current context (what's on screen)
            
        Returns:
            Dict with action plan
        """
        logger.info(f"Processing command: {user_input}")
        
        if not self.api_backend:
            # No API available - use simple heuristics
            return self._simple_response(user_input)
        
        if self.api_backend == 'openai':
            return self._process_openai(user_input, context)
        elif self.api_backend == 'anthropic':
            return self._process_anthropic(user_input, context)
        else:
            return self._simple_response(user_input)
    
    def _process_openai(self, user_input: str, context: str) -> Dict:
        """Process command using OpenAI API."""
        try:
            import openai
            
            system_prompt = """You are Tucker AI, an intelligent agent that controls an Android tablet. 
You can:
- Open apps (provide package name)
- Take screenshots
- Tap on screen coordinates
- Type text
- Search the web
- Navigate apps

Respond with a JSON action plan:
{
    "action": "app_open" | "tap" | "type" | "swipe" | "search" | "navigate",
    "app": "package name" (for app_open),
    "activity": "activity name" (optional, for app_open),
    "x": int, "y": int (for tap/swipe),
    "text": "text to type" (for type),
    "query": "search term" (for search),
    "reason": "why you're doing this"
}"""
            
            response = openai.ChatCompletion.create(
                model=self.model,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Context: {context}\n\nCommand: {user_input}"}
                ]
            )
            
            return {
                "success": True,
                "response": response.choices[0].message.content,
                "backend": "openai"
            }
        except Exception as e:
            logger.error(f"OpenAI error: {e}")
            return self._simple_response(user_input)
    
    def _process_anthropic(self, user_input: str, context: str) -> Dict:
        """Process command using Anthropic Claude API."""
        try:
            system_prompt = """You are Tucker AI, an intelligent agent that controls an Android tablet."""
            
            message = self.client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                messages=[
                    {"role": "user", "content": f"Context: {context}\n\nCommand: {user_input}"}
                ]
            )
            
            return {
                "success": True,
                "response": message.content[0].text,
                "backend": "anthropic"
            }
        except Exception as e:
            logger.error(f"Anthropic error: {e}")
            return self._simple_response(user_input)
    
    def _simple_response(self, user_input: str) -> Dict:
        """Fallback: Simple command parsing without AI.
        
        This works even without an API key!
        """
        logger.info("Using simple response (no AI backend)")
        
        text = user_input.lower()
        
        if 'open' in text:
            if 'chrome' in text or 'browser' in text:
                return {
                    "success": True,
                    "action": "app_open",
                    "app": "com.android.chrome",
                    "activity": "com.google.android.apps.chrome.Main",
                    "reason": "User asked to open Chrome"
                }
            elif 'youtube' in text:
                return {
                    "success": True,
                    "action": "app_open",
                    "app": "com.google.android.youtube",
                    "reason": "User asked to open YouTube"
                }
        
        elif 'search' in text:
            query = text.replace('search', '').replace('for', '').strip()
            return {
                "success": True,
                "action": "search",
                "query": query,
                "reason": f"User asked to search for: {query}"
            }
        
        elif 'screenshot' in text or 'capture' in text:
            return {
                "success": True,
                "action": "screenshot",
                "reason": "User asked for screenshot"
            }
        
        return {
            "success": False,
            "reason": "Could not understand command",
            "suggestion": "Try: 'Open Chrome', 'Search for..', 'Take screenshot'"
        }

if __name__ == '__main__':
    # Test the AI brain
    brain = AIBrain()
    result = brain.process_command("Open Chrome")
    print(result)
