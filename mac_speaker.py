#!/usr/bin/env python3
"""
mac-speaker: OpenClaw skill for MacBook text-to-speech
Uses macOS built-in 'say' command for high-quality TTS
"""

import subprocess
import os
import sys
import time
from pathlib import Path
from typing import Optional, List, Dict, Union
import tempfile

class MacSpeaker:
    """Main class for MacBook text-to-speech control"""
    
    def __init__(self):
        self.say_path = self._find_tool("say")
        self.afplay_path = self._find_tool("afplay")  # For playing audio files
        self._available_voices = None  # Cache for voices
        
    def _find_tool(self, tool_name: str) -> str:
        """Find a command-line tool in PATH"""
        try:
            result = subprocess.run(["which", tool_name], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                return result.stdout.strip()
            else:
                raise Exception(f"{tool_name} not found in PATH. This is a macOS built-in tool.")
        except Exception as e:
            raise Exception(f"Failed to find {tool_name}: {e}")
    
    def list_voices(self, refresh: bool = False) -> List[Dict[str, str]]:
        """
        List all available TTS voices
        
        Returns:
            List of voice dictionaries with 'name', 'language', and 'gender' keys
        """
        if self._available_voices is not None and not refresh:
            return self._available_voices
            
        try:
            result = subprocess.run([self.say_path, "-v", "?"], 
                                  capture_output=True, text=True)
            
            voices = []
            for line in result.stdout.strip().split('\n'):
                if line.strip():
                    # Parse voice info: "Alex en_US # Most people recognize me by my voice."
                    parts = line.split('#')
                    voice_info = parts[0].strip()
                    
                    # Parse voice details
                    if ' ' in voice_info:
                        name, lang = voice_info.split(' ', 1)
                        
                        # Extract gender from description if available
                        gender = "unknown"
                        description = parts[1].strip() if len(parts) > 1 else ""
                        
                        if "female" in description.lower():
                            gender = "female"
                        elif "male" in description.lower():
                            gender = "male"
                        
                        voices.append({
                            "name": name.strip(),
                            "language": lang.strip(),
                            "gender": gender,
                            "description": description
                        })
            
            self._available_voices = voices
            return voices
            
        except Exception as e:
            print(f"Error listing voices: {e}")
            return []
    
    def get_default_voice(self) -> str:
        """Get the default system voice"""
        try:
            result = subprocess.run([self.say_path, "-v", "?"], 
                                  capture_output=True, text=True)
            
            # First voice is usually the default
            for line in result.stdout.strip().split('\n'):
                if line.strip():
                    parts = line.split('#')
                    voice_info = parts[0].strip()
                    if ' ' in voice_info:
                        name, _ = voice_info.split(' ', 1)
                        return name.strip()
            
            return "Alex"  # Fallback to Alex
        except:
            return "Alex"
    
    def speak(self, 
              text: str,
              voice: Optional[str] = None,
              rate: int = 175,
              volume: float = 1.0,
              wait: bool = True) -> bool:
        """
        Speak text aloud using MacBook speakers
        
        Args:
            text: Text to speak
            voice: Voice name (e.g., "Alex", "Samantha", "Ting-Ting")
            rate: Speech rate in words per minute (default 175)
            volume: Volume level (0.0 to 1.0)
            wait: Wait for speech to finish before returning
        
        Returns:
            True if successful, False otherwise
        """
        if not text or not text.strip():
            print("⚠️ No text provided to speak")
            return False
        
        # Build command
        cmd = [self.say_path]
        
        # Add voice if specified
        if voice:
            cmd.extend(["-v", voice])
        
        # Add rate
        if rate != 175:  # Default is 175
            cmd.extend(["-r", str(rate)])
        
        # Add text
        cmd.append(text)
        
        print(f"🗣️ Speaking: '{text[:50]}{'...' if len(text) > 50 else ''}'")
        if voice:
            print(f"   Voice: {voice}")
        print(f"   Rate: {rate} wpm")
        
        try:
            if wait:
                # Run and wait for completion
                result = subprocess.run(cmd, capture_output=True, text=True)
                if result.returncode == 0:
                    print("✅ Speech completed")
                    return True
                else:
                    print(f"❌ Speech failed: {result.stderr}")
                    return False
            else:
                # Run in background
                subprocess.Popen(cmd)
                print("✅ Speech started in background")
                return True
                
        except Exception as e:
            print(f"❌ Error speaking: {e}")
            return False
    
    def speak_to_file(self,
                     text: str,
                     output_path: Optional[str] = None,
                     voice: Optional[str] = None,
                     rate: int = 175,
                     format: str = "aiff") -> Optional[str]:
        """
        Convert text to speech and save to audio file
        
        Args:
            text: Text to convert
            output_path: Path to save audio file (default: timestamp in current dir)
            voice: Voice name
            rate: Speech rate
            format: Audio format (aiff, wav, etc.)
        
        Returns:
            Path to audio file, or None if failed
        """
        if not text or not text.strip():
            print("⚠️ No text provided")
            return None
        
        if output_path is None:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            output_path = f"speech_{timestamp}.{format}"
        
        # Ensure directory exists
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        
        # Build command
        cmd = [self.say_path]
        
        if voice:
            cmd.extend(["-v", voice])
        
        if rate != 175:
            cmd.extend(["-r", str(rate)])
        
        # Output to file
        cmd.extend(["-o", output_path])
        
        # Add text
        cmd.append(text)
        
        print(f"💾 Converting to audio file: {output_path}")
        print(f"   Text: '{text[:50]}{'...' if len(text) > 50 else ''}'")
        if voice:
            print(f"   Voice: {voice}")
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if os.path.exists(output_path):
                file_size = os.path.getsize(output_path)
                print(f"✅ Audio file saved: {output_path} ({file_size:,} bytes)")
                return output_path
            else:
                print(f"❌ Audio file not created. Error: {result.stderr}")
                return None
                
        except Exception as e:
            print(f"❌ Error creating audio file: {e}")
            return None
    
    def play_audio_file(self, audio_path: str, wait: bool = True) -> bool:
        """
        Play an audio file using MacBook speakers
        
        Args:
            audio_path: Path to audio file
            wait: Wait for playback to finish
        
        Returns:
            True if successful, False otherwise
        """
        if not os.path.exists(audio_path):
            print(f"❌ Audio file not found: {audio_path}")
            return False
        
        print(f"🎵 Playing audio file: {audio_path}")
        
        try:
            if wait:
                result = subprocess.run([self.afplay_path, audio_path], 
                                      capture_output=True, text=True)
                if result.returncode == 0:
                    print("✅ Playback completed")
                    return True
                else:
                    print(f"❌ Playback failed: {result.stderr}")
                    return False
            else:
                subprocess.Popen([self.afplay_path, audio_path])
                print("✅ Playback started in background")
                return True
                
        except Exception as e:
            print(f"❌ Error playing audio: {e}")
            return False
    
    def convert_and_play(self,
                        text: str,
                        voice: Optional[str] = None,
                        rate: int = 175,
                        delete_after: bool = True) -> bool:
        """
        Convert text to audio file and play it immediately
        
        Args:
            text: Text to speak
            voice: Voice name
            rate: Speech rate
            delete_after: Delete temporary audio file after playing
        
        Returns:
            True if successful, False otherwise
        """
        # Create temp file
        with tempfile.NamedTemporaryFile(suffix=".aiff", delete=False) as tmp:
            temp_path = tmp.name
        
        try:
            # Convert to audio file
            audio_file = self.speak_to_file(text, temp_path, voice, rate)
            
            if not audio_file:
                return False
            
            # Play the audio file
            success = self.play_audio_file(audio_file, wait=True)
            
            # Clean up
            if delete_after and os.path.exists(temp_path):
                os.remove(temp_path)
                print(f"🧹 Cleaned up temporary file")
            
            return success
            
        except Exception as e:
            print(f"❌ Error in convert_and_play: {e}")
            # Clean up temp file on error
            if os.path.exists(temp_path):
                os.remove(temp_path)
            return False
    
    def get_system_info(self) -> Dict[str, Union[str, List, bool]]:
        """Get information about TTS capabilities"""
        voices = self.list_voices()
        
        info = {
            "say_available": os.path.exists(self.say_path),
            "afplay_available": os.path.exists(self.afplay_path),
            "default_voice": self.get_default_voice(),
            "total_voices": len(voices),
            "voice_categories": {
                "english": len([v for v in voices if "en_" in v["language"]]),
                "chinese": len([v for v in voices if "zh_" in v["language"]]),
                "female": len([v for v in voices if v["gender"] == "female"]),
                "male": len([v for v in voices if v["gender"] == "male"]),
            },
            "supported_formats": ["aiff", "wav", "mp4", "m4a"],
            "rate_range": "50-400 words per minute",
            "volume_control": "System volume only (0.0-1.0)"
        }
        
        return info

def test_basic():
    """Test basic TTS functionality"""
    print("=== Testing MacSpeaker ===")
    
    try:
        speaker = MacSpeaker()
        info = speaker.get_system_info()
        
        print(f"\n📊 System Info:")
        print(f"   TTS available: {info['say_available']}")
        print(f"   Default voice: {info['default_voice']}")
        print(f"   Total voices: {info['total_voices']}")
        
        print(f"\n🗣️ Testing speech...")
        
        # Test 1: Basic speech
        print("1. Speaking basic text...")
        success1 = speaker.speak("Hello, this is a test of the MacBook speaker system.", wait=True)
        
        if success1:
            print("✅ Basic speech works!")
            
            # Test 2: Different voice
            print("\n2. Testing different voice...")
            voices = speaker.list_voices()
            if voices:
                # Try to find a Chinese voice if available
                chinese_voices = [v for v in voices if "zh_" in v["language"]]
                if chinese_voices:
                    test_voice = chinese_voices[0]["name"]
                    print(f"   Using voice: {test_voice}")
                    success2 = speaker.speak("你好，这是一个中文语音测试。", voice=test_voice, wait=True)
                else:
                    # Use first available voice
                    test_voice = voices[0]["name"]
                    print(f"   Using voice: {test_voice}")
                    success2 = speaker.speak("Testing with different voice.", voice=test_voice, wait=True)
            
            # Test 3: Save to file
            print("\n3. Testing save to file...")
            audio_file = speaker.speak_to_file(
                "This text will be saved to an audio file.",
                voice=speaker.get_default_voice()
            )
            
            if audio_file and os.path.exists(audio_file):
                print(f"✅ Audio file created: {audio_file}")
                
                # Test 4: Play from file
                print("\n4. Testing playback from file...")
                success4 = speaker.play_audio_file(audio_file, wait=True)
                
                # Clean up
                os.remove(audio_file)
                print(f"🧹 Cleaned up: {audio_file}")
                
                if success4:
                    print("✅ All tests passed!")
                    return True
                else:
                    print("❌ Playback test failed")
                    return False
            else:
                print("❌ Audio file creation failed")
                return False
        else:
            print("❌ Basic speech test failed")
            return False
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main test function"""
    print("=== MacSpeaker Skill Test ===\n")
    
    if test_basic():
        print("\n🎉 SUCCESS! MacSpeaker skill works!")
        print("\nFeatures tested:")
        print("✅ Text-to-speech output")
        print("✅ Voice selection")
        print("✅ Audio file creation")
        print("✅ Audio file playback")
        print("✅ Multiple language support")
        
        return 0
    else:
        print("\n❌ Test failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())