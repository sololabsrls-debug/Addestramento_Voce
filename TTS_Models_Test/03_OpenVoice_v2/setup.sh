#!/bin/bash
# Setup script for OpenVoice v2

echo "Installing OpenVoice v2..."

# Clone repository
if [ ! -d "OpenVoice" ]; then
    git clone https://github.com/myshell-ai/OpenVoice.git
    cd OpenVoice
else
    cd OpenVoice
fi

# Install requirements
pip install -r requirements.txt

# Download checkpoints
mkdir -p checkpoints
cd checkpoints

# Download v2 models
if [ ! -f "converter/config.json" ]; then
    wget https://myshell-public-repo-hosting.s3.amazonaws.com/openvoice/checkpoints_v2.zip
    unzip checkpoints_v2.zip
    rm checkpoints_v2.zip
fi

cd ../..

echo "OpenVoice v2 setup completato!"
