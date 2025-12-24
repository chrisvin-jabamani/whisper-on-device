"""
Transcription module with MLX optimization for Apple Silicon
Falls back to Faster Whisper on Intel Macs
"""

import platform
import os


class Transcriber:
    def __init__(self, model_size="base"):
        """
        Initialize Whisper model with the best available backend
        model_size options: tiny, base, small, medium, large
        'base' is a good balance of speed and accuracy
        """
        self.model_size = model_size
        self.backend = None
        self.model = None
        self._init_backend()
    
    def _is_apple_silicon(self):
        """Check if running on Apple Silicon Mac"""
        return (
            platform.system() == "Darwin" and 
            platform.machine() == "arm64"
        )
    
    def _init_backend(self):
        """Initialize the best available transcription backend"""
        # Try MLX first on Apple Silicon
        if self._is_apple_silicon():
            try:
                import mlx_whisper
                self.backend = "mlx"
                print(f"📦 Using MLX Whisper ({self.model_size}) - Apple Silicon optimized ⚡")
                print("✅ MLX backend ready!")
                return
            except ImportError:
                print("⚠️  MLX Whisper not installed, falling back to Faster Whisper")
        
        # Fall back to Faster Whisper
        from faster_whisper import WhisperModel
        print(f"📦 Loading Faster Whisper ({self.model_size})...")
        self.model = WhisperModel(self.model_size, device="cpu", compute_type="int8")
        self.backend = "faster_whisper"
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
            if self.backend == "mlx":
                return self._transcribe_mlx(audio_file)
            else:
                return self._transcribe_faster_whisper(audio_file)
                
        except Exception as e:
            print(f"❌ Transcription error: {e}")
            return None
        
        finally:
            # Clean up temp file
            try:
                os.unlink(audio_file)
            except:
                pass
    
    def _transcribe_mlx(self, audio_file):
        """Transcribe using MLX Whisper (Apple Silicon optimized)"""
        import mlx_whisper
        
        result = mlx_whisper.transcribe(
            audio_file,
            path_or_hf_repo=f"mlx-community/whisper-{self.model_size}-mlx"
        )
        
        text = result.get("text", "").strip()
        # Clean up extra spaces
        text = " ".join(text.split())
        
        return text if text else None
    
    def _transcribe_faster_whisper(self, audio_file):
        """Transcribe using Faster Whisper (CPU)"""
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
