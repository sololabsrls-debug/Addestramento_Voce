#!/bin/bash
# Setup script for Piper TTS

echo "Installing Piper TTS..."

# Install piper-tts
pip install piper-tts

# Download Italian voice model (it_IT-riccardo-x_low)
mkdir -p models
cd models

# Download the Italian model from Piper repository
wget https://huggingface.co/rhasspy/piper-voices/resolve/main/it/it_IT/riccardo/x_low/it_IT-riccardo-x_low.onnx
wget https://huggingface.co/rhasspy/piper-voices/resolve/main/it/it_IT/riccardo/x_low/it_IT-riccardo-x_low.onnx.json

cd ..

echo "Piper setup completato!"
