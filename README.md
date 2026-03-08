# mac-speaker OpenClaw Skill

Convert text to speech using your MacBook's built-in speakers. Uses macOS `say` command for high-quality, natural-sounding speech in multiple languages.

## Features

- **Text-to-Speech**: Convert any text to spoken audio
- **50+ Voices**: Built-in voices for English, Chinese, Japanese, Spanish, French, etc.
- **Rate Control**: Adjust speech speed (50-400 words per minute)
- **Audio Files**: Save speech to AIFF, WAV, MP4, or M4A files
- **Playback Control**: Play audio files through speakers
- **Background Operation**: Speak without blocking main thread
- **Multi-language**: Support for international text

## Quick Start

```python
from mac_speaker import MacSpeaker

# Initialize speaker
speaker = MacSpeaker()

# Speak text aloud
speaker.speak("Hello, this is your MacBook speaking!")

# Save to audio file
audio_file = speaker.speak_to_file(
    "This text will be saved as an audio file",
    output_path="speech.aiff"
)

# List available voices
voices = speaker.list_voices()
print(f"Available voices: {len(voices)}")
```

## Installation

No installation required! Uses macOS built-in `say` command.

```bash
# Just copy the skill folder to your OpenClaw skills directory
cp -r mac-speaker ~/.openclaw/skills/
```

## Usage Examples

### Basic Usage
```python
from mac_speaker import MacSpeaker

speaker = MacSpeaker()

# Simple speech
speaker.speak("Welcome to OpenClaw!")

# With specific voice
speaker.speak("你好，世界", voice="Ting-Ting")

# Adjust speech rate
speaker.speak("Speaking slowly", rate=100)
speaker.speak("Speaking quickly", rate=300)
```

### Advanced Features
```python
# Convert and save to file
speaker.speak_to_file(
    "This is important information",
    output_path="important.aiff",
    voice="Samantha",
    rate=200
)

# Convert and play immediately
speaker.convert_and_play(
    "This text will be converted and played",
    voice="Alex",
    delete_after=True  # Clean up temp file
)

# Play existing audio file
speaker.play_audio_file("music.mp3", wait=False)
```

### Voice Management
```python
# List all voices
voices = speaker.list_voices()
for voice in voices:
    print(f"{voice['name']:20} {voice['language']:10} {voice['gender']}")

# Get default voice
default = speaker.get_default_voice()
print(f"Default voice: {default}")

# Find Chinese voices
chinese_voices = [v for v in voices if "zh_" in v["language"]]
print(f"Chinese voices: {len(chinese_voices)}")
```

## Available Voices

macOS includes 50+ high-quality voices:

### English Voices
- **Alex** - Default male voice (US English)
- **Samantha** - High-quality female voice (US English)
- **Daniel** - British English
- **Karen** - Australian English
- **Tessa** - South African English

### Chinese Voices
- **Ting-Ting** - Female Mandarin
- **Sin-Ji** - Female Cantonese

### Other Languages
- **Kyoko** - Japanese
- **Yuna** - Korean
- **Thomas** - French
- **Anna** - German
- **Paola** - Spanish

## Integration with OpenClaw

### As a Standalone Skill
```python
# In your OpenClaw skill
def handle_text_to_speech(text, voice=None):
    speaker = MacSpeaker()
    return speaker.speak(text, voice=voice)
```

### With Other Skills
```python
# Combine with mac-camera
from mac_camera import MacCamera
from mac_speaker import MacSpeaker

def capture_and_describe():
    camera = MacCamera()
    speaker = MacSpeaker()
    
    # Take photo
    photo = camera.capture_photo()
    
    # Describe action
    speaker.speak(f"Photo captured: {photo}")
    
    return photo
```

## File Formats

| Format | Quality | Size | Notes |
|--------|---------|------|-------|
| AIFF | High | Large | Default, uncompressed |
| WAV | High | Large | Windows compatible |
| MP4 | Good | Small | Compressed, widely supported |
| M4A | Good | Small | Apple audio format |

## System Requirements

- **macOS** 10.7 or later
- **Python** 3.6+
- **No external dependencies** - uses built-in `say` and `afplay` commands

## Troubleshooting

### Common Issues

**No sound output**
```bash
# Test system audio
afplay /System/Library/Sounds/Glass.aiff
```

**Voice not available**
```bash
# List all voices
say -v '?'

# Download additional voices (first time use may trigger download)
say -v "Samantha" "Testing"
```

**Permission issues**
- Grant microphone access if saving to file
- Check Privacy & Security settings

**Slow speech generation**
- Reduce text length for immediate feedback
- Use background mode for long texts

## Performance Tips

1. **Short texts**: Use `speak()` for immediate feedback
2. **Long texts**: Use `speak_to_file()` then `play_audio_file()`
3. **Background**: Set `wait=False` for non-blocking operation
4. **Caching**: Voice list is cached after first call

## License

MIT License - See LICENSE file

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new features
4. Submit a pull request

## Related Projects

- [mac-camera](../mac-camera/): Photo and video capture
- [OpenClaw](https://github.com/openclaw/openclaw): Main framework
- [ClawHub](https://clawhub.com): Skill marketplace

---

**Enjoy natural-sounding speech from your MacBook!** 🎤