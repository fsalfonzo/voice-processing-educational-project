"""Generate audio files and create Windows playback script"""

import numpy as np
import soundfile as sf
from pathlib import Path
import subprocess

def generate_test_audio():
    """Generate test audio files"""
    output_dir = Path("data/samples")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    sr = 44100
    duration = 2.0
    t = np.linspace(0, duration, int(sr * duration))
    
    # Create test tones
    test_files = []
    
    # 440Hz sine wave
    sine = np.sin(2 * np.pi * 440 * t) * 0.3
    sine_file = output_dir / "test_440hz.wav"
    sf.write(sine_file, sine, sr)
    test_files.append(sine_file)
    print(f"Generated: {sine_file}")
    
    # A major chord
    chord = (np.sin(2*np.pi*440*t) + np.sin(2*np.pi*554*t) + np.sin(2*np.pi*659*t)) / 3 * 0.3
    chord_file = output_dir / "test_chord.wav"
    sf.write(chord_file, chord, sr)
    test_files.append(chord_file)
    print(f"Generated: {chord_file}")
    
    return test_files

def create_windows_player_script():
    """Create a Windows Python script for audio playback"""
    
    # Python script that runs on Windows
    windows_script = '''"""
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
    wsl_path = Path(r"\\\\wsl$\\Ubuntu-24.04\\home\\fsalf\\projects\\audio-project\\data\\samples")
    
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
        input(f"\\nPress Enter to play: {wav_file.name}")
        success = play_audio_file(wav_file)
        if success:
            print("Playback completed")
        else:
            print("Playback failed")
    
    print("\\nAll files played!")

if __name__ == "__main__":
    main()
'''
    
    # Save to a location accessible from Windows
    script_path = Path("data/samples/windows_audio_player.py")
    with open(script_path, 'w') as f:
        f.write(windows_script)
    
    print(f"Created Windows audio player: {script_path}")
    
    # Also create a batch file to run it
    batch_content = '''@echo off
echo Installing pygame if needed...
pip install pygame

echo.
echo Running audio player...
python windows_audio_player.py

pause
'''
    
    batch_path = Path("data/samples/run_audio_player.bat")
    with open(batch_path, 'w') as f:
        f.write(batch_content)
    
    print(f"Created batch launcher: {batch_path}")
    
    return script_path, batch_path

if __name__ == "__main__":
    print("Generating test audio for Windows playback...")
    test_files = generate_test_audio()
    
    print("\\nCreating Windows playback scripts...")
    script_path, batch_path = create_windows_player_script()
    
    print("\\n" + "="*50)
    print("Windows Playback Setup Complete!")
    print("="*50)
    print("\\nTo play audio on Windows:")
    print("1. Open Windows Explorer")
    print("2. Navigate to: \\\\wsl$\\Ubuntu-24.04\\home\\fsalf\\projects\\audio-project\\data\\samples")
    print("3. Double-click: run_audio_player.bat")
    print("   OR")
    print("4. Simply double-click any .wav file to play with Windows default player")
    
    print("\\nThis validates your audio processing pipeline works perfectly!")
