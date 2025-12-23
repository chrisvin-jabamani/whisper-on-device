# Wispr Lite

Simple, minimal voice dictation for macOS. Double-tap Cmd to record, speak naturally, and have text appear in any app.

## Features

- 🎤 **System-wide**: Works in any app (Slack, Gmail, Cursor, etc.)
- ⚡ **Fast**: ~1-2s latency on M4 Mac
- 🔒 **Private**: Everything runs on-device, no cloud
- 💯 **Free**: Uses open-source models
- 🎯 **Simple**: Double-tap Cmd to start/stop

## Installation

### 1. Install Dependencies

```bash
cd /Users/chrisvin/dev/wispr

# Install Python packages
pip3 install -r requirements.txt

# Install Ollama (optional, for cleanup)
brew install ollama
ollama pull llama3.2:1b
```

### 2. Grant Permissions

On first run, macOS will request:
- **Microphone Access**: Allow
- **Accessibility Access**: System Settings → Privacy & Security → Accessibility → Add Python
- **Input Monitoring**: System Settings → Privacy & Security → Input Monitoring → Add Python

## Usage

### Start the app:

```bash
python3 main.py
```

A microphone icon (🎤) will appear in your menu bar.

### Use it:

1. Click into any text field
2. Double-tap **Cmd** key
3. Speak naturally
4. Double-tap **Cmd** again (or wait for silence)
5. Text appears!

### Quit:

Click the menu bar icon → Quit

## How It Works

```
Double-tap Cmd → Record Audio → Whisper Transcription → Text Injection
```

- **Faster Whisper**: High-quality speech recognition
- **PyAudio**: Microphone capture
- **pynput**: Keyboard automation
- **rumps**: Menu bar UI

## Configuration

Edit `transcriber.py` to change model size:
- `tiny`: Fastest, least accurate
- `base`: Good balance (default)
- `small`: More accurate, slower
- `medium`: Very accurate, much slower

## Troubleshooting

**"No audio recorded"**
- Check microphone permissions
- Ensure microphone is working

**"Permission denied"**
- Grant Accessibility and Input Monitoring permissions in System Settings

**Slow transcription**
- Use `tiny` model instead of `base`
- Check CPU usage

**Text not appearing**
- Ensure Accessibility permissions are granted
- Try clicking in the text field again

## Future Features

- [ ] LLM cleanup (remove filler words)
- [ ] Custom dictionary
- [ ] Push-to-talk mode
- [ ] Command mode ("make this friendlier")
- [ ] Settings UI

## Credits

Built with:
- [Faster Whisper](https://github.com/guillaumekln/faster-whisper)
- [Whisper.cpp](https://github.com/ggerganov/whisper.cpp)
- [PyAudio](https://people.csail.mit.edu/hubert/pyaudio/)
- [pynput](https://github.com/moses-palmer/pynput)

Inspired by [Wispr Flow](https://wisprflow.ai)
