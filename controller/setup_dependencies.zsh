#!/usr/bin/env zsh

echo "Installing Python dependencies..."
pip install websocket-client pvporcupine pydub webrtcvad || {
    echo "Failed to install Python packages"
    exit 1
}

echo "Installing system dependencies..."
sudo apt update && sudo apt install -y portaudio19-dev || {
    echo "Failed to install portaudio"
    exit 1
}

echo "Installing PyAudio..."
pip install pyaudio || {
    echo "Failed to install pyaudio"
    exit 1
}

echo "All dependencies installed successfully!"
