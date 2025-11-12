#!/bin/bash
# Setup script for Parler-TTS

echo "Installing Parler-TTS..."

# Install parler-tts
pip install git+https://github.com/huggingface/parler-tts.git

# Install dependencies
pip install torch torchaudio transformers accelerate

echo "Parler-TTS setup completato!"
echo "NOTA: I modelli verranno scaricati automaticamente da HuggingFace al primo utilizzo"
