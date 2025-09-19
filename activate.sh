#!/bin/bash
# Quick activation for audio-project
cd ~/projects/audio-project
source venv/bin/activate
echo "🎵 Audio Project Environment Activated"
echo "📁 Project: $(pwd)"
echo "🐍 Python: $(python --version)"
echo ""
echo "Quick commands:"
echo "  python validate.py          # Check environment"
echo "  jupyter lab docs/notebooks  # Start Jupyter"
echo "  python src/test_setup.py    # Test audio processing"
