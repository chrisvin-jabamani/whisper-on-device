"""
Hotkey listener - detects Cmd+Control pressed together
"""

from pynput import keyboard

class HotkeyListener:
    def __init__(self, callback):
        """
        callback: function to call when hotkey is detected
        """
        self.callback = callback
        self.listener = None
        self.pressed_keys = set()
        self.hotkey_triggered = False
        
    def on_press(self, key):
        """Handle key press events"""
        # Add key to pressed keys set
        self.pressed_keys.add(key)
        
        # Check if both Cmd and Control are pressed
        cmd_pressed = (keyboard.Key.cmd in self.pressed_keys or 
                      keyboard.Key.cmd_r in self.pressed_keys)
        ctrl_pressed = (keyboard.Key.ctrl in self.pressed_keys or 
                       keyboard.Key.ctrl_r in self.pressed_keys or
                       keyboard.Key.ctrl_l in self.pressed_keys)
        
        # Trigger callback only once per key combination
        if cmd_pressed and ctrl_pressed and not self.hotkey_triggered:
            print("✨ Cmd+Control detected!")
            self.hotkey_triggered = True
            self.callback()
    
    def on_release(self, key):
        """Handle key release events"""
        # Remove key from pressed keys set
        if key in self.pressed_keys:
            self.pressed_keys.remove(key)
        
        # Reset trigger flag when either key is released
        if key in [keyboard.Key.cmd, keyboard.Key.cmd_r, 
                   keyboard.Key.ctrl, keyboard.Key.ctrl_r, keyboard.Key.ctrl_l]:
            self.hotkey_triggered = False
    
    def start(self):
        """Start listening for hotkeys"""
        self.listener = keyboard.Listener(
            on_press=self.on_press,
            on_release=self.on_release
        )
        self.listener.start()
        print("🎹 Hotkey listener started (Cmd+Control)")
    
    def stop(self):
        """Stop listening"""
        if self.listener:
            self.listener.stop()
