"""
Windows-side audio player for WSL2-generated files
Run this script from Windows PowerShell or Command Prompt
"""

import pygame
import time
import sys
from pathlib import Path

def play_audio_file(filepath):
    """Play audio file using pygame"""
    try:
        pygame.mixer.init()
        pygame.mixer.music.load(str(filepath))
        print(f"Playing: {filepath.name}")
        pygame.mixer.music.play()
        
        # Wait for playback to complete
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)
        
        pygame.mixer.quit()
        return True
    except Exception as e:
        print(f"Error playing {filepath}: {e}")
        return False

def main():
    # Path to WSL2 files from Windows
    wsl_path = Path(r"\\wsl$\Ubuntu-24.04\home\fsalf\projects\audio-project\data\samples")
    
    if not wsl_path.exists():
        print("Cannot access WSL2 files. Make sure WSL2 is running and path is correct.")
        return
    
    # Find all wav files
    wav_files = list(wsl_path.glob("*.wav"))
    
    if not wav_files:
        print("No .wav files found in samples directory")
        return
    
    print(f"Found {len(wav_files)} audio files")
    print("Press Enter to play each file...")
    
    for wav_file in sorted(wav_files):
        input(f"\nPress Enter to play: {wav_file.name}")
        success = play_audio_file(wav_file)
        if success:
            print("Playback completed")
        else:
            print("Playback failed")
    
    print("\nAll files played!")

if __name__ == "__main__":
    main()
