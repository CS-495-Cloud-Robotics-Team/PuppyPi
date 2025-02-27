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
from action_groups_dict import action_groups_dict

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

# Queue for WebSocket commands
command_queue = queue.Queue()

def on_message(ws, message):
    print("Received message: ", message)

def on_error(ws, error):
    print("Error: ", error)

def on_close(ws, close_status_code, close_msg):
    print("WebSocket Closed")

def websocket_handler():
    """Maintains a persistent WebSocket connection and processes commands from the queue."""
    def on_open(ws):
        print("WebSocket connected ✅")

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
        print(f"📡 Sent action group command: {action_group_file}")

def record(Output_Filename, Duration=5):
    stream = pa.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)
    print("🎤 Recording...")

    frames = []
    for _ in range(int(44100 / 1024 * Duration)):
        data = stream.read(1024)
        frames.append(data)

    print("🎤 Recording finished.")
    
    with wave.open(Output_Filename, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(pa.get_sample_size(pyaudio.paInt16))
        wf.setframerate(44100)
        wf.writeframes(b''.join(frames))

    print(f"💾 Saved recording as {Output_Filename}")

if __name__ == "__main__":
    if not PICO_ACCESS_KEY:
        raise ValueError("Make sure you have an .env file with PICO_ACCESS_KEY for picovoice.")

    # Start WebSocket handler in a separate thread
    threading.Thread(target=websocket_handler, daemon=True).start()

    try:
        while True:
            print("🎙 Listening...")
            pcm = stream.read(porcupine.frame_length, exception_on_overflow=False)
            pcm = np.frombuffer(pcm, dtype=np.int16)

            result = porcupine.process(pcm.tolist())
            if result >= 0:
                print("🔥 Wake word detected!")
                record(Output_Filename="temp.wav", Duration=3)

                headers = {
                    'Content-Type': 'audio/wav',
                    'x-api-key': os.getenv("COMMAND_API_KEY"),
                }
                with open('temp.wav', 'rb') as f:
                    data = f.read()

                response = requests.post(
                    'https://1fl0qfare6.execute-api.us-east-1.amazonaws.com/default/puppyPiProcessingFunction',
                    headers=headers,
                    data=data,
                )

                data = response.json()
                responseString = data.get("gpt_analysis")
                for oneResponse in responseString:
                    action_group_file = action_groups_dict.get(oneResponse)
                    if action_group_file:
                        print(f"Putting into queue: {action_group_file}")
                        command_queue.put(action_group_file)  # Add command to queue
                    else:
                        print("❌ No valid action group file found for response:", oneResponse)
                   
                   
                # if action_group_file:
                #     command_queue.put(action_group_file)  # Add command to queue
                # else:
                #     print("❌ No valid action group file found for response:", responseString)

                
                os.remove("temp.wav")

    except KeyboardInterrupt:
        print("Stopping...")
        stream.close()
        pa.terminate()
        porcupine.delete()
