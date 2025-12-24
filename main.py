#!/usr/bin/env python3
"""
Wispr Lite - Simple voice dictation for macOS
Press Cmd+Control to start/stop recording
"""

import threading
from recorder import AudioRecorder
from transcriber import Transcriber
from postprocessor import TextPostProcessor
from injector import TextInjector
from hotkeys import HotkeyListener
from ui import StatusIndicator

class WisprLite:
    def __init__(self):
        self.recorder = AudioRecorder()
        self.transcriber = Transcriber()
        self.postprocessor = TextPostProcessor()  # Ollama LLM cleanup
        self.injector = TextInjector()
        self.indicator = StatusIndicator(self)
        self.is_recording = False
        
        # Start hotkey listener with separate start/stop callbacks
        self.hotkey_listener = HotkeyListener(self.start_recording, self.stop_recording)
    
    def start_recording(self):
        """Start recording audio"""
        print("🎤 Started recording...")
        self.is_recording = True
        self.indicator.update_status("recording")
        self.recorder.start_recording()
    
    def stop_recording(self):
        """Stop recording and process audio"""
        if not self.is_recording:
            return
            
        print("⏸️  Stopped recording, processing...")
        self.is_recording = False
        self.indicator.update_status("processing")
        
        # Stop recording and get audio file
        audio_file = self.recorder.stop_recording()
        
        if audio_file:
            # Process in background thread so UI stays responsive
            threading.Thread(target=self._process_audio, args=(audio_file,)).start()
        else:
            print("❌ No audio recorded")
            self.indicator.update_status("idle")
    
    def _process_audio(self, audio_file):
        """Process audio file and inject text"""
        try:
            # Transcribe audio
            text = self.transcriber.transcribe(audio_file)
            print(f"📝 Transcribed: {text}")
            
            if text:
                # Clean up with LLM (if Ollama is running)
                text = self.postprocessor.process(text)
                
                # Inject into active application
                self.injector.inject_text(text)
                print("✅ Text injected!")
            else:
                print("❌ No text transcribed")
                
        except Exception as e:
            print(f"❌ Error processing audio: {e}")
        finally:
            self.indicator.update_status("idle")
    
    def run(self):
        """Start the application"""
        print("🚀 Wispr Lite started!")
        print("📌 Press Cmd+Control to start/stop recording")
        print("📌 Press Ctrl+C to quit")
        
        # Start hotkey listener
        self.hotkey_listener.start()
        
        # Run the menu bar app
        self.indicator.run()

if __name__ == "__main__":
    app = WisprLite()
    app.run()
