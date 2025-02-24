import sounddevice as sd

def list_audio_devices():
    devices = sd.query_devices()
    print(devices)

list_audio_devices()
