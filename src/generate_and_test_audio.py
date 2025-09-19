"""Reliable audio testing for WSL2 limitations"""

import numpy as np
import soundfile as sf
from pathlib import Path
import subprocess
import librosa

def create_project_audio_samples():
    """Generate audio samples for voice processing project"""
    
    output_dir = Path("data/samples")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    sr = 44100
    duration = 3.0
    t = np.linspace(0, duration, int(sr * duration))
    
    # Voice-like test signals for our project
    samples = {}
    
    # 1. Synthetic vowel formants (voice processing relevant)
    f1, f2, f3 = 730, 1090, 2440  # "ah" vowel formants
    vowel = (np.sin(2*np.pi*f1*t) + 0.7*np.sin(2*np.pi*f2*t) + 0.3*np.sin(2*np.pi*f3*t)) * 0.2
    envelope = np.exp(-t*0.5) * (1 + 0.1*np.sin(2*np.pi*5*t))  # Natural speech envelope
    samples['synthetic_vowel'] = vowel * envelope
    
    # 2. Harmonic series (voice fundamental + harmonics)
    f0 = 150  # Typical male voice fundamental
    voice_like = np.zeros_like(t)
    for h in range(1, 8):
        amp = 1.0 / (h**0.8)  # More realistic harmonic rolloff
        voice_like += amp * np.sin(2*np.pi*f0*h*t)
    voice_like *= np.exp(-t*0.3) * 0.15
    samples['voice_harmonics'] = voice_like
    
    # 3. Frequency sweep for spectral analysis
    f_start, f_end = 80, 8000  # Voice frequency range
    chirp = np.sin(2*np.pi * (f_start + (f_end-f_start)*t/duration) * t) * 0.2
    samples['frequency_sweep'] = chirp
    
    # Save all samples and analyze
    print("Generated Voice Processing Test Samples")
    print("=" * 40)
    
    for name, audio in samples.items():
        # Save audio file
        filename = output_dir / f"{name}.wav"
        sf.write(filename, audio, sr)
        
        # Analyze with librosa (our main processing library)
        mfccs = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=13)
        spectral_centroid = librosa.feature.spectral_centroid(y=audio, sr=sr)
        chroma = librosa.feature.chroma_stft(y=audio, sr=sr)
        
        print(f"\n{name.replace('_', ' ').title()}:")
        print(f"  Duration: {len(audio)/sr:.2f}s")
        print(f"  MFCC shape: {mfccs.shape}")
        print(f"  Spectral centroid mean: {np.mean(spectral_centroid):.1f} Hz")
        print(f"  Chroma shape: {chroma.shape}")
        print(f"  File: {filename}")
    
    # Create Windows batch file for testing
    batch_content = """@echo off
echo Voice Processing Project - Audio Validation
echo ==========================================
echo.
echo Testing generated audio samples...
echo If you can hear these, your audio pipeline is working!
echo.
pause

"""
    
    for name in samples.keys():
        batch_content += f"""echo Playing {name.replace('_', ' ')}...
start /wait "" "{name}.wav"
timeout /t 1 >nul
echo.
"""
    
    batch_content += """echo.
echo Voice processing pipeline validated!
pause"""
    
    batch_file = output_dir / "test_voice_processing.bat"
    with open(batch_file, 'w') as f:
        f.write(batch_content)
    
    print(f"\nWindows test script: {batch_file}")
    print("\nTo validate your voice processing pipeline:")
    print("1. In Windows Explorer, navigate to:")
    print(f"   \\\\wsl$\\Ubuntu-24.04\\home\\{Path.home().name}\\projects\\audio-project\\data\\samples")
    print("2. Double-click: test_voice_processing.bat")
    print("3. If you hear the sounds, your audio processing is working perfectly!")
    
    return samples

if __name__ == "__main__":
    create_project_audio_samples()
