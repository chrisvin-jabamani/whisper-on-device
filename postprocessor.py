"""
Text post-processing with Ollama LLM
Cleans up transcriptions: removes filler words, fixes grammar, adds punctuation
"""

import requests


class TextPostProcessor:
    def __init__(self, model="llama3.2:1b", enabled=True):
        """
        Initialize the post-processor
        
        Args:
            model: Ollama model to use (default: llama3.2:1b for speed)
            enabled: Whether to enable LLM cleanup (default: True)
        """
        self.model = model
        self.enabled = enabled
        self.ollama_url = "http://localhost:11434/api/generate"
        self._ollama_available = None
        
    def _check_ollama(self):
        """Check if Ollama is running (cached result)"""
        if self._ollama_available is None:
            try:
                response = requests.get("http://localhost:11434", timeout=2)
                self._ollama_available = response.status_code == 200
                if self._ollama_available:
                    print(f"🤖 Ollama detected - LLM cleanup enabled ({self.model})")
                else:
                    print("⚠️  Ollama not responding - LLM cleanup disabled")
            except requests.exceptions.RequestException:
                self._ollama_available = False
                print("⚠️  Ollama not running - LLM cleanup disabled")
        
        return self._ollama_available
    
    def process(self, text):
        """
        Clean up transcribed text using Ollama
        
        Returns original text if:
        - Post-processing is disabled
        - Ollama is not running
        - Any error occurs
        """
        if not self.enabled or not text or not text.strip():
            return text
        
        if not self._check_ollama():
            return text
        
        prompt = f"""Remove filler words (um, uh, like) and fix punctuation. Return only the text, nothing else.

{text}"""
        
        try:
            response = requests.post(
                self.ollama_url,
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.1,  # Low temperature for consistency
                        "num_predict": 500,  # Limit output length
                    }
                },
                timeout=15
            )
            
            if response.status_code == 200:
                result = response.json().get("response", "").strip()
                # Remove surrounding quotes if present
                if result.startswith('"') and result.endswith('"'):
                    result = result[1:-1]
                if result.startswith("'") and result.endswith("'"):
                    result = result[1:-1]
                # Basic validation - don't return empty text
                if result and len(result) > 0:
                    print(f"🧹 Cleaned: {result}")
                    return result
            
            return text
            
        except requests.exceptions.Timeout:
            print("⚠️  Ollama timeout - using raw transcription")
            return text
        except requests.exceptions.RequestException as e:
            print(f"⚠️  Ollama error: {e} - using raw transcription")
            return text
        except Exception as e:
            print(f"⚠️  Post-processing error: {e}")
            return text
    
    def reset_cache(self):
        """Reset Ollama availability cache (for retry after starting Ollama)"""
        self._ollama_available = None

