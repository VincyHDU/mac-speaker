#!/usr/bin/env python3
"""
Example usage of the mac-speaker skill
Demonstrates text-to-speech capabilities
"""

from mac_speaker import MacSpeaker
import os
import time

def main():
    print("=== mac-speaker Example Usage ===")
    
    # Initialize speaker
    speaker = MacSpeaker()
    
    # Get system info
    info = speaker.get_system_info()
    print(f"\n📊 System Info:")
    print(f"   TTS available: {info['say_available']}")
    print(f"   Default voice: {info['default_voice']}")
    print(f"   Total voices: {info['total_voices']}")
    print(f"   English voices: {info['voice_categories']['english']}")
    print(f"   Chinese voices: {info['voice_categories']['chinese']}")
    
    # List some voices
    print(f"\n🗣️ Sample Voices:")
    voices = speaker.list_voices()
    for voice in voices[:5]:  # Show first 5
        print(f"   {voice['name']:15} {voice['language']:10} ({voice['gender']})")
    
    # Test 1: Basic speech
    print(f"\n1️⃣ Testing basic speech...")
    print("   Speaking: 'Hello, this is a test of the MacBook speaker system.'")
    success1 = speaker.speak("Hello, this is a test of the MacBook speaker system.", wait=True)
    
    if success1:
        print("   ✅ Basic speech works!")
        
        # Test 2: Different rates
        print(f"\n2️⃣ Testing different speech rates...")
        rates = [100, 175, 300]
        for rate in rates:
            print(f"   Rate: {rate} wpm - 'Testing speech rate'")
            speaker.speak("Testing speech rate", rate=rate, wait=True)
            time.sleep(0.5)
        
        # Test 3: Multi-language
        print(f"\n3️⃣ Testing multi-language support...")
        
        # Try Chinese if available
        chinese_voices = [v for v in voices if "zh_" in v["language"]]
        if chinese_voices:
            chinese_voice = chinese_voices[0]["name"]
            print(f"   Chinese voice: {chinese_voice}")
            speaker.speak("你好，这是一个中文语音测试。", voice=chinese_voice, wait=True)
        else:
            print("   ⚠️ No Chinese voices found, using default")
            speaker.speak("Testing with default voice.", wait=True)
        
        # Test 4: Save to audio file
        print(f"\n4️⃣ Testing save to audio file...")
        desktop_path = os.path.expanduser("~/Desktop/speech_demo.aiff")
        audio_file = speaker.speak_to_file(
            "This is a demonstration of text-to-speech saving to an audio file. "
            "You can play this file anytime.",
            output_path=desktop_path,
            voice=speaker.get_default_voice(),
            rate=200
        )
        
        if audio_file and os.path.exists(audio_file):
            file_size = os.path.getsize(audio_file)
            print(f"   ✅ Audio file saved: {audio_file}")
            print(f"   Size: {file_size:,} bytes")
            
            # Test 5: Play from file
            print(f"\n5️⃣ Testing playback from file...")
            print("   Playing the audio file...")
            success5 = speaker.play_audio_file(audio_file, wait=True)
            
            if success5:
                print("   ✅ Playback successful!")
                
                # Optional: Keep or delete the file
                keep = input("\n   Keep the audio file? (y/n): ").strip().lower()
                if keep != 'y':
                    os.remove(audio_file)
                    print("   🧹 Audio file deleted")
                else:
                    print(f"   💾 Audio file kept at: {audio_file}")
            else:
                print("   ❌ Playback failed")
        else:
            print("   ❌ Audio file creation failed")
        
        print(f"\n🎉 All tests completed!")
        print(f"\n💡 Try these commands:")
        print(f"   python3 -c \"from mac_speaker import MacSpeaker; s=MacSpeaker(); s.speak('Your text here')\"")
        print(f"   python3 -c \"from mac_speaker import MacSpeaker; s=MacSpeaker(); print([v['name'] for v in s.list_voices()[:3]])\"")
        
    else:
        print("   ❌ Basic speech test failed")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)