# Voice Processing Educational Project

A comprehensive educational journey from basic audio fundamentals to advanced AI-based voice processing, aimed at building quantifiable understanding of voice preferences through measurable features.

## Mission Statement
*"I like this voice because it has these specific musical, timbral, and emotional characteristics that can be measured and understood."*

## Project Structure

audio-project/
├── src/                     # Source code
│   ├── features/            # Feature extraction modules
│   ├── models/              # ML/AI model implementations
│   ├── utils/               # Utility functions
│   ├── visualization/       # Plotting and visualization
│   └── preprocessing/       # Data preprocessing
├── data/                    # Audio files and datasets
│   ├── raw/                 # Original audio files
│   ├── processed/           # Processed audio data
│   ├── models/              # Trained model files
│   └── samples/             # Sample audio for testing
├── docs/                    # Documentation
│   ├── notebooks/           # Jupyter notebooks
│   └── tutorials/           # Learning tutorials
└── requirements.txt         # Python dependencies


## Development Environment

- **Platform**: WSL2 (Ubuntu 24.04 LTS)
- **Python**: 3.12.3
- **GPU**: NVIDIA RTX A2000 8GB
- **Key Libraries**: librosa, PyTorch, TensorFlow, scikit-learn

## Phase 1: Environment Setup ✅

- [x] Complete development environment with Python 3.12
- [x] Audio processing libraries (librosa, PyTorch, TensorFlow)
- [x] GPU acceleration (CUDA) setup and validation
- [x] WSL2 audio configuration and testing
- [x] Project structure and organization
- [x] Git version control and GitHub integration

## Getting Started

1. **Clone the repository**
```bash
   git clone git@github.com:fsalfonzo/voice-processing-educational-project.git
   cd voice-processing-educational-project
   
2. Set up virtual environment   
   
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   
3. Validate installation

 python validate.py
4. quick start
    ./activate.sh
    
    
Project Phases

Phase 1: Primer & Environment Setup ✅
Phase 2: Audio Fundamentals 🔄
Phase 3: Advanced Feature Engineering
Phase 4: Classical Audio Processing
Phase 5: Modern AI Approaches
Phase 6: Advanced Applications & Synthesis


Key Capabilities

Comprehensive audio processing pipeline
Real-time feature extraction (MFCC, spectral analysis, chroma)
Machine learning model training and inference
Voice synthesis and analysis
GPU-accelerated neural networks
Cross-platform audio validation (WSL2 + Windows)

Development Tools

Environment Management: Virtual environment with comprehensive dependencies
Validation: Automated testing scripts for environment and audio processing
Audio I/O: Multiple approaches for audio generation and playback
Version Control: Git with proper .gitignore for audio projects

Technical Achievements

Successfully configured WSL2 + Ubuntu 24.04 for audio processing
Integrated modern Python 3.12 with latest audio/ML libraries
Established GPU acceleration with CUDA support
Created robust project structure for educational progression
Implemented cross-platform audio workflow (Linux dev + Windows playback)

Next Steps
Moving into Phase 2: Audio Fundamentals

Waveform analysis and manipulation
Frequency domain representations
Time-frequency analysis techniques
Perceptual audio features

License
This project is for educational purposes.
