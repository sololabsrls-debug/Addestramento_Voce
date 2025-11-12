#!/bin/bash
# Setup script for Coqui XTTS v2

echo "Installing Coqui TTS (XTTS v2)..."

# Install TTS
pip install TTS

# Install dependencies
pip install torch torchaudio numpy scipy

echo "Coqui XTTS setup completato!"
echo "NOTA: I modelli verranno scaricati automaticamente al primo utilizzo (~2GB)"
