#!/bin/bash
# Setup script for Resemble Chatterbox

echo "Installing Resemble Chatterbox..."

# Install from HuggingFace
pip install torch torchaudio transformers accelerate

echo "Resemble Chatterbox setup completato!"
echo "NOTA: Il modello verrà scaricato da HuggingFace al primo utilizzo (~1GB)"
