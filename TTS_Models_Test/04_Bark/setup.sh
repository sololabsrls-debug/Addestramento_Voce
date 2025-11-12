#!/bin/bash
# Setup script for Bark TTS

echo "Installing Bark TTS..."

# Install bark
pip install git+https://github.com/suno-ai/bark.git

# Install dependencies
pip install scipy numpy

echo "Bark setup completato!"
echo "NOTA: Al primo utilizzo, Bark scaricherà automaticamente i modelli (~2GB)"
