"""
Transcription module using Faster Whisper
"""

from faster_whisper import WhisperModel
import os

class Transcriber:
    def __init__(self, model_size="base", device="cpu"):
        """
        Initialize Whisper model
        model_size options: tiny, base, small, medium, large
        'base' is a good balance of speed and accuracy
        """
        print(f"📦 Loading Whisper model: {model_size}...")
        self.model = WhisperModel(model_size, device=device, compute_type="int8")
        print("✅ Model loaded!")
        
    def transcribe(self, audio_file):
        """
        Transcribe audio file to text
        Returns cleaned text or None if transcription fails
        """
        if not os.path.exists(audio_file):
            print(f"❌ Audio file not found: {audio_file}")
            return None
        
        try:
            # Transcribe with VAD filter to remove silence
            segments, info = self.model.transcribe(
                audio_file,
                vad_filter=True,
                vad_parameters=dict(min_silence_duration_ms=500)
            )
            
            # Combine all segments into one text
            text_parts = []
            for segment in segments:
                text_parts.append(segment.text.strip())
            
            text = " ".join(text_parts)
            
            # Clean up extra spaces
            text = " ".join(text.split())
            
            return text if text else None
            
        except Exception as e:
            print(f"❌ Transcription error: {e}")
            return None
        
        finally:
            # Clean up temp file
            try:
                os.unlink(audio_file)
            except:
                pass
