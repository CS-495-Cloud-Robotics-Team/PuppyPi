import json
import websocket
import threading
import pvporcupine
import pyaudio
import numpy as np
import wave
import os
import queue
from dotenv import load_dotenv
import requests
import time
import webrtcvad
from action_groups_dict import action_groups_dict
from MP3 import MP3
import io

# Localhost, connection to port 9090 on itself
PUPPYPI_IP = "localhost"
# WebSocket URL (rosbridge default is ws://<PuppyPi-IP>:9090)
WEBSOCKET_URL = f"ws://{PUPPYPI_IP}:9090"

#Loads the .env file
load_dotenv("/home/pi/.env")

#PicoVoice Access Key
PICO_ACCESS_KEY = os.getenv("PICO_ACCESS_KEY")

#Replace file with custom, to activate this one say "PicoVoice"
porcupine = pvporcupine.create(access_key=PICO_ACCESS_KEY, keyword_paths=["RBWakeWordTrained.ppn"]) 

pa = pyaudio.PyAudio()
stream = pa.open(format=pyaudio.paInt16, channels=1, rate=porcupine.sample_rate, 
                input=True, frames_per_buffer=porcupine.frame_length)

MP3_addr = 0x7b  # I2C address of the MP3 module
mp3 = MP3(MP3_addr)  # Create MP3 player instance
mp3.volume(40)  # Highest possible
mp3_positive_response = 25

# Queue for WebSocket commands
command_queue = queue.Queue()

vad = webrtcvad.Vad()
vad.set_mode(3)

def on_message(ws, message):
    print("Received message: ", message)
    command_queue.task_done()

def on_error(ws, error):
    print("Error: ", error)

def on_close(ws, close_status_code, close_msg):
    print("WebSocket Closed")

def websocket_handler():
    """Maintains a persistent WebSocket connection and processes commands from the queue."""
    def on_open(ws):
        print("WebSocket connected")

    ws = websocket.WebSocketApp(
        WEBSOCKET_URL,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
        on_open=on_open
    )

    # Run WebSocket in a separate thread
    wst = threading.Thread(target=ws.run_forever, daemon=True)
    wst.start()

    while True:
        action_group_file = command_queue.get()  # Wait for a command
        payload = {
            "op": "call_service",
            "service": "/puppy_control/runActionGroup",
            "args": {
                "name": action_group_file,  
                "wait": True  
            }
        }
        ws.send(json.dumps(payload))
        print(f"Sent action group command: {action_group_file}")
                
def is_speaking(frame):
    return vad.is_speech(frame, 16000)

def record():
    """Records until the user stops speaking based on WebRTCVAD."""
    stream = pa.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=320)
    print("Recording...")

    frames = []
    silence_duration = 1.5  # Stop recording after this many seconds of silence
    silence_start = None

    while True:
        frame = stream.read(320)
        frames.append(frame)

        if is_speaking(frame):
            silence_start = None  # Reset silence timer if speech is detected
        else:
            if silence_start is None:
                silence_start = time.time()  # Mark silence start time
            elif time.time() - silence_start > silence_duration:
                print("Stopped speaking. Saving recording...")
                break

    audio_buffer = io.BytesIO()
    with wave.open(audio_buffer, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(pa.get_sample_size(pyaudio.paInt16))
        wf.setframerate(16000)
        wf.writeframes(b''.join(frames))
        
    # Seek to the start of the buffer so it can be read later
    audio_buffer.seek(0)

    return audio_buffer

if __name__ == "__main__":
    if not PICO_ACCESS_KEY:
        raise ValueError("Make sure you have an .env file with PICO_ACCESS_KEY for picovoice.")

    # Start WebSocket handler in a separate thread
    threading.Thread(target=websocket_handler, daemon=True).start()
    print("Listening...")
    try:
        while True:
            pcm = stream.read(porcupine.frame_length, exception_on_overflow=False)
            pcm = np.frombuffer(pcm, dtype=np.int16)

            result = porcupine.process(pcm.tolist())
            if result >= 0:
                print("Wake word detected!")
                mp3.playNum(mp3_positive_response)
                audio_buffer = record()

                headers = {
                    'Content-Type': 'audio/wav',
                    'x-api-key': os.getenv("COMMAND_API_KEY"),
                }
                
                data = audio_buffer.read()

                response = requests.post(
                    'https://1fl0qfare6.execute-api.us-east-1.amazonaws.com/default/puppyPiProcessingFunction',
                    headers=headers,
                    data=data,
                )
                
                data = response.json()
                print(data)
                responseString = data.get("gpt_analysis")
                if responseString:
                    for oneResponse in responseString:
                        command_queue.join()
                        action_group_file = action_groups_dict.get(oneResponse)
                        if action_group_file:
                            print(f"Putting into queue: {action_group_file}")
                            command_queue.put(action_group_file)  # Add command to queue
                            print(f"this is the entire queue {list(command_queue.queue)}")
                        else:
                            print("No valid action group file found for response:", oneResponse)
                            command_queue.put("shake_head.d6ac")
                
                audio_buffer.close()

    except KeyboardInterrupt:
        print("Stopping...")
        stream.close()
        pa.terminate()
        porcupine.delete()
