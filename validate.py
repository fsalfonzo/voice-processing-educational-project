#!/usr/bin/env python3
"""Environment validation for audio-project"""

import sys
import os
import importlib
import warnings
warnings.filterwarnings('ignore')

def check_environment():
    print("🔍 Audio Project Environment Check\n")
    
    # Check Python version
    version = sys.version_info
    print(f"🐍 Python: {version.major}.{version.minor}.{version.micro}")
    if version.major == 3 and version.minor >= 10:
        print("✅ Excellent Python version!")
    else:
        print("⚠️  Consider upgrading to Python 3.10+")
    
    # Check virtual environment
    in_venv = 'audio-project/venv' in sys.executable
    print(f"📦 Virtual Environment: {'✅ Active' if in_venv else '❌ Not detected'}")
    
    # Test core imports
    core_libs = {
        'numpy': 'numpy',
        'librosa': 'librosa', 
        'torch': 'torch',
        'torchaudio': 'torchaudio',
        'matplotlib': 'matplotlib',
        'scipy': 'scipy',
        'sklearn': 'sklearn',
        'transformers': 'transformers',
        'soundfile': 'soundfile'
    }
    
    print("\n📚 Core Libraries:")
    all_good = True
    for name, module in core_libs.items():
        try:
            lib = importlib.import_module(module)
            version = getattr(lib, '__version__', 'unknown')
            print(f"   ✅ {name}: {version}")
        except ImportError:
            print(f"   ❌ {name}: Not installed")
            all_good = False
    
    # Check directory structure
    print("\n📁 Directory Structure:")
    expected_dirs = ['src', 'data', 'docs', 'venv']
    for dir_name in expected_dirs:
        exists = os.path.exists(dir_name)
        print(f"   {'✅' if exists else '❌'} {dir_name}/")
        if not exists:
            all_good = False
    
    # Quick audio test
    print("\n🎵 Audio Processing Test:")
    try:
        import librosa
        import numpy as np
        
        # Synthetic audio test
        sr = 22050
        t = np.linspace(0, 1, sr)
        y = np.sin(2 * np.pi * 440 * t)
        mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
        chroma = librosa.feature.chroma_stft(y=y, sr=sr)
        print(f"   ✅ MFCC extraction: {mfcc.shape}")
        print(f"   ✅ Chroma extraction: {chroma.shape}")
        
    except Exception as e:
        print(f"   ❌ Audio test failed: {e}")
        all_good = False
    
    # GPU/CUDA check
    print("\n🖥️  Compute Resources:")
    try:
        import torch
        if torch.cuda.is_available():
            device_name = torch.cuda.get_device_name(0)
            memory_gb = torch.cuda.get_device_properties(0).total_memory / 1e9
            print(f"   ✅ CUDA: {device_name} ({memory_gb:.1f} GB)")
        else:
            print("   ℹ️  CUDA: Not available (CPU mode)")
            
        # Test tensor creation
        x = torch.randn(10, 10)
        print(f"   ✅ PyTorch tensor creation: {x.shape}")
        
    except Exception as e:
        print(f"   ❌ PyTorch test failed: {e}")
        all_good = False
    
    print(f"\n{'🎉 Environment Ready!' if all_good else '⚠️  Issues detected - see above'}")
    
    if all_good:
        print("\n🚀 Next Steps:")
        print("   jupyter lab docs/notebooks  # Start coding!")
        print("   python src/test_setup.py    # Run audio test")
    
    return all_good

if __name__ == "__main__":
    check_environment()
