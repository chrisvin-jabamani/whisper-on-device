"""
Audio recording module using PyAudio
"""

import pyaudio
import wave
import tempfile
import os
import time

class AudioRecorder:
    def __init__(self, sample_rate=16000, chunk_size=1024):
        self.sample_rate = sample_rate
        self.chunk_size = chunk_size
        self.audio = pyaudio.PyAudio()
        self.stream = None
        self.frames = []
        self.recording = False
        self.temp_file = None
        
    def start_recording(self):
        """Start recording audio from microphone"""
        self.frames = []
        self.recording = True
        
        # Open audio stream
        self.stream = self.audio.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=self.sample_rate,
            input=True,
            frames_per_buffer=self.chunk_size,
            stream_callback=self._audio_callback
        )
        
        self.stream.start_stream()
    
    def _audio_callback(self, in_data, frame_count, time_info, status):
        """Callback for audio stream"""
        if self.recording:
            self.frames.append(in_data)
        return (in_data, pyaudio.paContinue)
    
    def stop_recording(self):
        """Stop recording and save to file"""
        self.recording = False
        
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
        
        # Don't process if no audio was recorded
        if not self.frames:
            return None
        
        # Create temp file
        self.temp_file = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)
        temp_path = self.temp_file.name
        
        # Write audio to WAV file
        with wave.open(temp_path, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(self.audio.get_sample_size(pyaudio.paInt16))
            wf.setframerate(self.sample_rate)
            wf.writeframes(b''.join(self.frames))
        
        return temp_path
    
    def cleanup(self):
        """Clean up audio resources"""
        if self.stream:
            self.stream.close()
        self.audio.terminate()
        
        # Delete temp file if it exists
        if self.temp_file and os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)
