import pvporcupine
import pyaudio
import numpy as np
import wave
import os
from dotenv import load_dotenv
import requests
import json

#Loads the .env file
load_dotenv()

#PicoVoice Access Key
PICO_ACCESS_KEY = os.getenv("PICO_ACCESS_KEY")
if not PICO_ACCESS_KEY:
    print(PICO_ACCESS_KEY)
    raise ValueError("Make sure you have an .env file with PICO_ACCESS_KEY for picovoice.")

#Replace file with custom, to activate this one say "PicoVoice"
porcupine = pvporcupine.create(access_key=PICO_ACCESS_KEY, keyword_paths=["PuppyPi123.ppn"]) 

pa = pyaudio.PyAudio()
stream = pa.open(format=pyaudio.paInt16, channels=1, rate=porcupine.sample_rate, 
                 input=True, frames_per_buffer=porcupine.frame_length)

def record(Output_Filename = "recorded_audio.wav", Audio = pa, Format = pyaudio.paInt16, Channels = 1, Rate = 44100, Chunk = 1024, Duration = 5):
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
            record()
            # Saves the audio recording to recorded_audio.wav which is to be delated later in the program
            headers = {
                'Content-Type': 'audio/wav',
                'x-api-key': os.getenv("AWS_API_KEY"),
            }
            
            # record() function saves the audio to recorded_audio.wav
            with open('recorded_audio.wav', 'rb') as f:
                data = f.read()

            response = requests.post(
                'https://1fl0qfare6.execute-api.us-east-1.amazonaws.com/default/puppyPiProcessingFunction',
                headers=headers,
                data=data,
            )
            
            # Prints output from cloud, for testing purposes
            print(response.content)
            
            # decodes response and grabs gpt_analysis which is the single command we want it to grab
            output_str = response.content.decode("utf-8")
            output_json = json.loads(output_str)
            command = output_json.get("gpt_analysis")

            # currently prints out the command, in the future command will be used to run a puppy pi 
            print(command)
            
            # Removes "temporary" file
            os.remove("recorded_audio.wav")
            
            
            # Break for testing purposes, in real program this can be deleted to rerun
            break
            
            
except KeyboardInterrupt:
    print("Stopping...")
    stream.close()
    pa.terminate()
    porcupine.delete()
