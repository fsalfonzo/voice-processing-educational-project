"""Test module to verify audio processing setup"""

import librosa
import numpy as np
import matplotlib.pyplot as plt
import torch
from scipy import signal

def test_audio_processing():
    """Test complete audio processing workflow"""
    print("Testing Audio Processing Pipeline")
    
    # Generate test audio with multiple components
    sr = 22050
    duration = 3.0
    t = np.linspace(0, duration, int(sr * duration))
    
    # Create a complex test signal
    fundamental = 440  # A4
    y = (np.sin(2 * np.pi * fundamental * t) + 
         0.5 * np.sin(2 * np.pi * fundamental * 2 * t) +  # octave
         0.3 * np.sin(2 * np.pi * fundamental * 3 * t))   # fifth
    
    # Add some noise and envelope
    envelope = np.exp(-t * 0.5)  # decay
    noise = 0.1 * np.random.randn(len(t))
    y = y * envelope + noise
    
    print(f"Generated {duration}s test audio at {sr} Hz")
    
    # Test librosa features
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    chroma = librosa.feature.chroma_stft(y=y, sr=sr)
    spectral_centroid = librosa.feature.spectral_centroid(y=y, sr=sr)
    
    print(f"MFCC features: {mfcc.shape}")
    print(f"Chroma features: {chroma.shape}")
    print(f"Spectral centroid: {spectral_centroid.shape}")
    
    # Fixed tempo estimation - handle the formatting properly
    try:
        tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
        # Convert numpy scalar to Python float for safe formatting
        tempo_val = float(tempo) if hasattr(tempo, 'item') else tempo
        print(f"Tempo estimation: {tempo_val:.1f} BPM")
    except Exception as e:
        print(f"Tempo estimation skipped due to: {e}")
        tempo_val = None
    
    # Test PyTorch tensor operations
    y_tensor = torch.from_numpy(y).float()
    mfcc_tensor = torch.from_numpy(mfcc).float()
    
    # Simple neural network-style operations
    processed_mfcc = torch.relu(mfcc_tensor)
    mean_features = torch.mean(processed_mfcc, dim=1)
    
    print(f"PyTorch processing: {mean_features.shape}")
    
    # Test scipy signal processing
    frequencies, psd = signal.periodogram(y, sr)
    dominant_freq = frequencies[np.argmax(psd)]
    
    print(f"Dominant frequency: {dominant_freq:.1f} Hz")
    
    return {
        'audio': y,
        'sample_rate': sr,
        'mfcc': mfcc,
        'chroma': chroma,
        'spectral_centroid': spectral_centroid,
        'tempo': tempo_val,
        'dominant_frequency': dominant_freq
    }

def test_audio_io():
    """Test audio input/output capabilities"""
    print("\nTesting Audio I/O")
    
    try:
        import sounddevice as sd
        devices = sd.query_devices()
        
        input_devices = [d for d in devices if d['max_input_channels'] > 0]
        output_devices = [d for d in devices if d['max_output_channels'] > 0]
        
        print(f"Found {len(input_devices)} input devices")
        print(f"Found {len(output_devices)} output devices")
        
        if len(input_devices) > 0:
            print(f"   Default input: {input_devices[0]['name']}")
        if len(output_devices) > 0:
            print(f"   Default output: {output_devices[0]['name']}")
            
        return True
        
    except Exception as e:
        print(f"Audio I/O test failed: {e}")
        return False

def test_additional_features():
    """Test additional audio processing features"""
    print("\nTesting Additional Features")
    
    try:
        # Create test audio
        sr = 22050
        t = np.linspace(0, 2, sr * 2)
        y = np.sin(2 * np.pi * 440 * t)
        
        # Test more librosa features
        zero_crossings = librosa.feature.zero_crossing_rate(y)
        spectral_rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)
        rms = librosa.feature.rms(y=y)
        
        print(f"Zero crossing rate: {zero_crossings.shape}")
        print(f"Spectral rolloff: {spectral_rolloff.shape}")
        print(f"RMS energy: {rms.shape}")
        
        # Test onset detection
        onset_frames = librosa.onset.onset_detect(y=y, sr=sr)
        onset_times = librosa.onset.onset_detect(y=y, sr=sr, units='time')
        
        print(f"Detected {len(onset_frames)} onsets")
        
        return True
        
    except Exception as e:
        print(f"Additional features test failed: {e}")
        return False

if __name__ == "__main__":
    print("Audio Project Setup Test\n")
    
    # Test core audio processing
    try:
        results = test_audio_processing()
        print("Core audio processing tests passed!")
    except Exception as e:
        print(f"Core audio processing failed: {e}")
        import traceback
        traceback.print_exc()
    
    # Test audio I/O
    test_audio_io()
    
    # Test additional features
    test_additional_features()
    
    print("\nSetup validation complete!")
    print("Ready to start building your voice processing pipeline!")
