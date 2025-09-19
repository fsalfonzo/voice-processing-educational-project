"""Test audio processing with playback functionality"""

import librosa
import numpy as np
import sounddevice as sd
import time
from IPython.display import Audio, display
import matplotlib.pyplot as plt

def create_test_sounds():
    """Create various test sounds for playback"""
    sr = 22050
    duration = 2.0
    t = np.linspace(0, duration, int(sr * duration))
    
    sounds = {}
    
    # 1. Pure sine wave (A4 - 440 Hz)
    sounds['sine_440'] = {
        'audio': np.sin(2 * np.pi * 440 * t),
        'description': 'Pure sine wave (A4 - 440 Hz)'
    }
    
    # 2. Major chord (A major triad)
    chord = (np.sin(2 * np.pi * 440 * t) +      # A4
             np.sin(2 * np.pi * 554.37 * t) +   # C#5  
             np.sin(2 * np.pi * 659.25 * t))    # E5
    sounds['major_chord'] = {
        'audio': chord / 3,  # Normalize
        'description': 'A major chord (A-C#-E)'
    }
    
    # 3. Chirp (frequency sweep)
    f0, f1 = 200, 2000  # Start and end frequencies
    sounds['chirp'] = {
        'audio': np.sin(2 * np.pi * (f0 + (f1 - f0) * t / duration) * t),
        'description': f'Frequency sweep ({f0}-{f1} Hz)'
    }
    
    # 4. Noise burst
    envelope = np.exp(-t * 2)  # Quick decay
    sounds['noise_burst'] = {
        'audio': np.random.randn(len(t)) * envelope * 0.3,
        'description': 'Decaying noise burst'
    }
    
    # 5. Complex harmonic series
    fundamental = 220  # A3
    harmonic_series = np.zeros_like(t)
    for harmonic in range(1, 6):  # First 5 harmonics
        amplitude = 1.0 / harmonic  # Decreasing amplitude
        harmonic_series += amplitude * np.sin(2 * np.pi * fundamental * harmonic * t)
    
    sounds['harmonic_series'] = {
        'audio': harmonic_series / np.max(np.abs(harmonic_series)),
        'description': 'Harmonic series (A3 fundamental)'
    }
    
    return sounds, sr

def play_sound_safe(audio, sr=22050, volume=0.3):
    """Safely play audio with volume control"""
    try:
        # Normalize and apply volume control
        audio_normalized = audio / np.max(np.abs(audio)) * volume
        
        print(f"Playing audio... ({len(audio_normalized)/sr:.1f}s)")
        sd.play(audio_normalized, sr)
        sd.wait()  # Wait for completion
        print("Playback complete!")
        return True
        
    except Exception as e:
        print(f"Playback failed: {e}")
        print("Note: Audio playback requires working PulseAudio in WSL2")
        return False

def analyze_and_play(audio, sr, description):
    """Analyze audio features and then play it"""
    print(f"\n--- {description} ---")
    
    # Basic analysis
    duration = len(audio) / sr
    rms = np.sqrt(np.mean(audio**2))
    max_val = np.max(np.abs(audio))
    
    print(f"Duration: {duration:.2f}s")
    print(f"RMS: {rms:.4f}")
    print(f"Peak: {max_val:.4f}")
    
    # Frequency analysis
    frequencies, psd = np.fft.rfftfreq(len(audio), 1/sr), np.abs(np.fft.rfft(audio))
    dominant_freq = frequencies[np.argmax(psd)]
    print(f"Dominant frequency: {dominant_freq:.1f} Hz")
    
    # Play the sound
    success = play_sound_safe(audio, sr, volume=0.2)  # Lower volume for safety
    
    if success:
        time.sleep(0.5)  # Brief pause between sounds
    
    return success

def test_audio_devices():
    """Test available audio devices"""
    print("Available Audio Devices:")
    print("-" * 40)
    
    devices = sd.query_devices()
    for i, device in enumerate(devices):
        device_type = []
        if device['max_input_channels'] > 0:
            device_type.append('input')
        if device['max_output_channels'] > 0:
            device_type.append('output')
        
        print(f"[{i}] {device['name']} ({', '.join(device_type)})")
    
    print(f"\nDefault input: {sd.query_devices(kind='input')['name']}")
    print(f"Default output: {sd.query_devices(kind='output')['name']}")

def create_jupyter_audio_demo():
    """Create audio widgets for Jupyter notebook use"""
    try:
        from IPython.display import Audio, display, HTML
        
        print("Creating Jupyter audio widgets...")
        sounds, sr = create_test_sounds()
        
        widgets = {}
        for name, sound_data in sounds.items():
            audio_normalized = sound_data['audio'] / np.max(np.abs(sound_data['audio']))
            widgets[name] = Audio(audio_normalized, rate=sr)
            print(f"Created widget for: {sound_data['description']}")
        
        return widgets
        
    except ImportError:
        print("IPython not available - skipping Jupyter widgets")
        return None

if __name__ == "__main__":
    print("Audio Playback Test")
    print("=" * 50)
    
    # Test audio devices
    test_audio_devices()
    
    # Create test sounds
    print("\nGenerating test sounds...")
    sounds, sr = create_test_sounds()
    print(f"Created {len(sounds)} test sounds at {sr} Hz")
    
    # Analyze and play each sound
    print("\nTesting playback (volume set low for safety)...")
    
    playback_results = {}
    for name, sound_data in sounds.items():
        success = analyze_and_play(sound_data['audio'], sr, sound_data['description'])
        playback_results[name] = success
    
    # Summary
    successful_plays = sum(playback_results.values())
    print(f"\nPlayback Summary:")
    print(f"Successful: {successful_plays}/{len(sounds)}")
    
    if successful_plays == len(sounds):
        print("All audio tests passed! 🎵")
    elif successful_plays > 0:
        print("Partial success - some audio played correctly")
    else:
        print("No audio played - check WSL2 PulseAudio configuration")
        print("\nTroubleshooting tips:")
        print("1. Ensure Windows audio is working")
        print("2. Check WSLg is running (Windows 11 required)")
        print("3. Verify PULSE_SERVER environment variable")
        print("4. Try: pulseaudio --check -v")
