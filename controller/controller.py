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
from payloads_dict import payloads_dict
from MP3 import MP3
import io

task_done_event = threading.Event()

# Localhost, connection to port 9090 on itself
PUPPYPI_IP = "localhost"
# WebSocket URL (rosbridge default is ws://<PuppyPi-IP>:9090)
WEBSOCKET_URL = f"ws://{PUPPYPI_IP}:9090"

#Loads the .env file
load_dotenv("/home/pi/.env")

#PicoVoice Access Key
PICO_ACCESS_KEY = os.getenv("PICO_ACCESS_KEY")

#Replace file with custom, to activate this one say "PicoVoice"
porcupine = pvporcupine.create(access_key=PICO_ACCESS_KEY, keyword_paths=["ScuffyWakeWord.ppn"]) 

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
    task_done_event.set()

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
        payload = command_queue.get()  # Wait for a command
        print(f"payload is {payload}")
        
        if isinstance(payload, list):  # Check if it's a list of commands
            for command in payload:
                ws.send(json.dumps(command))
                print(f"Sent command: {command}")
                # Check if the command has a "wait" key
                if isinstance(command, dict) and "wait" in command:
                    # if command == "walk":
                    #     walk_time = 5.0  # Change this to any desired time
                    #     json_command = json.dumps(payloads_dict).replace("{{walk_time}}", str(walk_time))
                    wait_time = command["wait"]
                    print(f"Waiting for {wait_time} seconds...")
                    time.sleep(wait_time)  # Sleep for the specified wait time
                else:
                    print("No wait time specified. Proceeding without delay.")
            task_done_event.wait()
            task_done_event.clear()
        else:
            # Handle single command
            ws.send(json.dumps(payload))
            print(f"Sent payload: {payload}")
            task_done_event.wait()
            task_done_event.clear()
            # Check if the payload has a "wait" key
            if isinstance(payload, dict) and "wait" in payload:
                wait_time = payload["wait"]
                print(f"Waiting for {wait_time} seconds...")
                time.sleep(wait_time)  # Sleep for the specified wait time
            else:
                print("No wait time specified. Proceeding without delay.")
                

                
def is_speaking(frame):
    return vad.is_speech(frame, 16000)

def record():
    """
    Records audio from the microphone until the user stops speaking,
    using WebRTC Voice Activity Detection (VAD).
    
    Returns:
        io.BytesIO: A WAV audio buffer containing the recorded audio.
    """
    stream = pa.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=320)
    print("Recording...")

    audio_frames = []
    silence_duration = 1.5  # Stop recording after this many seconds of silence
    silence_start = None
    start_time = time.time()
    max_duration = 10 #seconds

    while True:
        frame = stream.read(320)
        audio_frames.append(frame)
        
        if time.time() - start_time >= max_duration:
            print("Time is up. Saving recording...")
            break

        if is_speaking(frame):
            silence_start = None  # Reset silence timer if speech is detected
        else:
            if silence_start is None:
                silence_start = time.time()  # Mark silence start time
            elif time.time() - silence_start > silence_duration:
                print("Stopped speaking. Saving recording...")
                break
    
    # Save recorded audio to an in-memory WAV file
    audio_buffer = io.BytesIO()
    with wave.open(audio_buffer, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(pa.get_sample_size(pyaudio.paInt16))
        wf.setframerate(16000)
        wf.writeframes(b''.join(audio_frames))
        
    # Rewind audio_buffer for future reading
    audio_buffer.seek(0)

    return audio_buffer

def record_and_process():
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
            payload = payloads_dict.get(oneResponse)
            
            if payload:
                print(f"Adding to queue: {payload}")
                command_queue.put(payload)  # Add command(s) to queue
                print(f"Queue contents: {list(command_queue.queue)}")
            else:
                print("No valid action group file found for response:", oneResponse)
                command_queue.put(payloads_dict.get("shake-head"))
    
    audio_buffer.close()
    
# def puppypi_force_stop():
#     print("resetting queue")
#     while not command_queue.empty():
#         command_queue.get()
    
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
            
            # check if wake word is detected
            if result >= 0:
                # record and send audio to cloud, recieve a list of commands, and run them
                record_and_process()

    except KeyboardInterrupt:
        print("Stopping...")
        stream.close()
        pa.terminate()
        porcupine.delete()
