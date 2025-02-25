import json
import websocket
import threading
import pvporcupine
import pyaudio
import numpy as np
import wave
import os
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

def on_message(ws, message):
    print("Received message: ", message)

def on_error(ws, error):
    print("Error: ", error)

def on_close(ws, close_status_code, close_msg):
    print("Closed")

def on_open(ws):
    # Create the request to call the service
    payload = {
        "op": "call_service",
        "service": "/puppy_control/runActionGroup",
        "args": {
            "name": "pee.d6ac",   # Action name: "sit"
            "wait": True      # Wait for completion: True
        }
    }
    
    # Send the payload as JSON
    ws.send(json.dumps(payload))

def call_puppy_service():
    # Create the WebSocket connection
    ws = websocket.WebSocketApp(
        WEBSOCKET_URL,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
        on_open=on_open
    )
    
    # Start the WebSocket in a separate thread
    ws_thread = threading.Thread(target=ws.run_forever)
    ws_thread.start()

   
    ws_thread.join()

def record(Output_Filename, Audio = pa, Format = pyaudio.paInt16, Channels = 1, Rate = 44100, Chunk = 1024, Duration = 5):
    #important inputs are Duration which is the time it records in seconds and Output Filename for how to store it
    #OpenAI wisper accepts .wav files
    
    # Open stream for recording
    stream = Audio.open(format=Format, channels=Channels, rate=Rate, input=True, frames_per_buffer=Chunk)
    
    print("Recording...")

    #This is where the audio is stored
    frames = []
    
    #Record audio in chunks
    for _ in range(int(Rate / Chunk * Duration)):
        data = stream.read(Chunk)
        frames.append(data)
        
    
    print("Recording finished.")
    
    #Save the recorded data as a WAV file
    with wave.open(Output_Filename, 'wb') as wf:
        wf.setnchannels(Channels)
        wf.setsampwidth(Audio.get_sample_size(Format))
        wf.setframerate(Rate)
        wf.writeframes(b''.join(frames))
        
    

    print(f"Saved recording as {Output_Filename}")

if __name__ == "__main__":
    if not PICO_ACCESS_KEY:
        print(PICO_ACCESS_KEY)
        raise ValueError("Make sure you have an .env file with PICO_ACCESS_KEY for picovoice.")

    print("🎙 Listening...")

    try:
        while True:
            pcm = stream.read(porcupine.frame_length, exception_on_overflow=False)
            pcm = np.frombuffer(pcm, dtype=np.int16)

            # Volume test for mic check
            # volume = np.abs(pcm).mean()
            # print(f"🔊 Volume Level: {volume:.2f}")
            
            #reads in activation word and analizes audio
            result = porcupine.process(pcm.tolist())
            # if word is detected result will be >=0
            if result >= 0:
                print("🔥 Wake word detected!")
                # Function to listen and save the next "Duration" seconds of audio
                record(Output_Filename = "temp.wav", Duration = 3)
                # Add a function to send audio to cloud and call the program?
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

                responseString = gpt_analysis = data.get("gpt_analysis")
                action_group_file = action_groups_dict.get(responseString)
                    
                if action_group_file:
                    def on_open(ws):
                        payload = {
                            "op": "call_service",
                            "service": "/puppy_control/runActionGroup",
                            "args": {
                                "name": action_group_file, 
                                "wait": True
                            }
                        }
                        ws.send(json.dumps(payload))

                    call_puppy_service()
                else:
                    print("❌ No valid action group file found for response:", responseString)
                
                # Break for testing purposes, in real program this can be deleted to rerun
                # break
                os.remove("temp.wav")
                
                

    except KeyboardInterrupt:
        print("Stopping...")
        stream.close()
        pa.terminate()
        porcupine.delete()


    #call_puppy_service()