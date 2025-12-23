"""
Text injection module - inserts text into active application
"""

import pyperclip
import time
from pynput.keyboard import Controller, Key

class TextInjector:
    def __init__(self):
        self.keyboard = Controller()
    
    def inject_text(self, text):
        """
        Inject text into the currently active application
        Uses clipboard + paste to ensure compatibility
        """
        if not text:
            return
        
        # Save current clipboard content
        try:
            old_clipboard = pyperclip.paste()
        except:
            old_clipboard = ""
        
        # Copy our text to clipboard
        pyperclip.copy(text)
        
        # Small delay to ensure clipboard is ready
        time.sleep(0.05)
        
        # Paste using Cmd+V
        self.keyboard.press(Key.cmd)
        self.keyboard.press('v')
        self.keyboard.release('v')
        self.keyboard.release(Key.cmd)
        
        # Wait a bit before restoring clipboard
        time.sleep(0.2)
        
        # Restore old clipboard content
        try:
            pyperclip.copy(old_clipboard)
        except:
            pass
