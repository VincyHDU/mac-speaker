# mac-speaker Skill

## Description
Text-to-speech (TTS) skill for MacBook using macOS built-in `say` command. Converts text to speech and plays through MacBook speakers or saves to audio files.

## Activation
Activate when user mentions:
- Text-to-speech
- MacBook speaker
- Voice output
- Audio generation
- TTS
- "speak this text"
- "read this aloud"

## Prerequisites
- macOS (built-in `say` command)
- No additional installation required

## Features
- **Text-to-speech**: Convert any text to spoken audio
- **Voice selection**: Choose from 50+ built-in voices
- **Multi-language**: Support for English, Chinese, Spanish, French, etc.
- **Rate control**: Adjust speech speed (50-400 words per minute)
- **Audio files**: Save speech to AIFF, WAV, or MP4 files
- **Playback**: Play audio files through speakers
- **Background operation**: Speak without blocking

## Usage Examples

### Basic speech:
```python
from mac_speaker import MacSpeaker

speaker = MacSpeaker()
speaker.speak("Hello, how are you today?")
```

### With specific voice:
```python
speaker.speak("你好，这是一个测试", voice="Ting-Ting")
```

### Save to audio file:
```python
audio_file = speaker.speak_to_file(
    "This will be saved to an audio file",
    output_path="speech.aiff",
    voice="Alex"
)
```

### List available voices:
```python
voices = speaker.list_voices()
for voice in voices[:5]:  # Show first 5
    print(f"{voice['name']} - {voice['language']}")
```

## Integration with OpenClaw
This skill can be integrated into OpenClaw workflows:
- Read notifications aloud
- Convert text responses to speech
- Create audio logs
- Language learning tools
- Accessibility features

## Voice Examples
- **Alex** (en_US): Default male voice, clear and natural
- **Samantha** (en_US): High-quality female voice
- **Ting-Ting** (zh_CN): Chinese female voice
- **Kyoko** (ja_JP): Japanese female voice
- **Thomas** (fr_FR): French male voice

## File Formats
- **AIFF**: Default, high quality
- **WAV**: Uncompressed
- **MP4**: Compressed, smaller files
- **M4A**: Apple audio format

## Notes
- Volume control uses system volume
- Some voices may require internet download on first use
- Chinese/Japanese voices work best with corresponding text
- Background speech continues even if Python exits

## Troubleshooting
**"say command not found"**
- Only available on macOS
- Check with `which say`

**"Voice not available"**
- List voices with `say -v ?`
- Some voices download on first use

**"No sound"**
- Check system volume
- Check if speakers are muted
- Try `afplay test.aiff` to test audio playback

## Related Skills
- [mac-camera](../mac-camera/): Photo/video capture
- [audio-processing](../audio-processing/): Audio manipulation
- [voice-recognition](../voice-recognition/): Speech to text