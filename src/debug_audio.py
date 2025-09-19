"""Debug the audio processing issue"""
import librosa
import numpy as np

def debug_tempo_issue():
    """Isolate the tempo estimation problem"""
    print("Testing tempo estimation...")
    
    # Create simple test audio
    sr = 22050
    duration = 3.0
    t = np.linspace(0, duration, int(sr * duration))
    y = np.sin(2 * np.pi * 440 * t)  # Simple sine wave
    
    try:
        tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
        print(f"Tempo type: {type(tempo)}")
        print(f"Tempo value: {tempo}")
        print(f"Tempo repr: {repr(tempo)}")
        
        # Test different formatting approaches
        print("Testing format approaches:")
        print(f"Direct: {tempo}")
        print(f"Float cast: {float(tempo)}")
        print(f"Item(): {tempo.item() if hasattr(tempo, 'item') else 'No item method'}")
        
        return tempo, beats
        
    except Exception as e:
        print(f"Error in tempo estimation: {e}")
        return None, None

if __name__ == "__main__":
    debug_tempo_issue()
