#!/usr/bin/env python3
# coding=utf8

import sounddevice as sd
import numpy as np
import wave

DURATION = 5  # seconds
SAMPLERATE = 44100  # CD-quality sound
DEVICE_INDEX = 0  # Current device index of USB mic. Find device index by running script in micFindIndex

def record_audio(filename="micRecordTest1.wav"):
    print(f"Recording from device {DEVICE_INDEX}...")
    audio_data = sd.rec(int(DURATION * SAMPLERATE), samplerate=SAMPLERATE, channels=1, dtype=np.int16, device=DEVICE_INDEX)
    sd.wait()  # Wait until recording is finished
    print("Recording finished.")

    # Save as WAV file
    with wave.open(filename, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)  # 16-bit audio
        wf.setframerate(SAMPLERATE)
        wf.writeframes(audio_data.tobytes())

    print(f"Saved recording as {filename}")

record_audio()
