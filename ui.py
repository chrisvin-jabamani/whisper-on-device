"""
Menu bar status indicator using rumps
"""

import rumps

class StatusIndicator(rumps.App):
    def __init__(self, wispr_app):
        super(StatusIndicator, self).__init__("🎤", quit_button=None)
        self.wispr_app = wispr_app
        self.menu = [
            "Status: Idle",
            None,  # Separator
            rumps.MenuItem("Quit", callback=self.quit_app)
        ]
    
    def update_status(self, status):
        """Update the status text in menu"""
        status_map = {
            "idle": ("🎤", "Status: Idle (Double-tap Cmd to record)"),
            "recording": ("🔴", "Status: Recording..."),
            "processing": ("⏳", "Status: Processing...")
        }
        
        icon, text = status_map.get(status, ("🎤", "Status: Unknown"))
        self.title = icon
        self.menu["Status: Idle"].title = text
    
    def quit_app(self, _):
        """Quit the application"""
        print("👋 Shutting down...")
        self.wispr_app.recorder.cleanup()
        self.wispr_app.hotkey_listener.stop()
        rumps.quit_application()
