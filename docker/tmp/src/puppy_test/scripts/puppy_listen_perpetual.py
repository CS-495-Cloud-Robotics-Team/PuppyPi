#!/usr/bin/env python3
# coding=utf8

# Author: Eli Weber
# Date: 2/25/25
# File to record audio, upload to cloud, get response, and run action group

import os
import sys
import math
import rospy
import threading 
import json
import requests
import sounddevice as sd
import numpy as np
import wave
from std_srvs.srv import SetBool
from puppy_control.msg import Velocity, Pose, Gait
from puppy_control.srv import SetRunActionName
from action_groups_dict import action_groups_dict
import threading
from threading import RLock, Timer

# ROS Constants
ROS_NODE_NAME = 'puppy_extend_demo'

# Define Pose and Gait Configurations
PuppyPose = {'roll': math.radians(0), 'pitch': math.radians(0), 'yaw': 0.000, 'height': -10, 'x_shift': -0.5, 'stance_x': 0, 'stance_y': 0}
GaitConfig = {'overlap_time': 0.3, 'swing_time': 0.2, 'clearance_time': 0.0, 'z_clearance': 5}

# Audio Constants
DURATION = 5  # seconds
SAMPLERATE = 44100  # CD-quality sound
DEVICE_INDEX = 0  # Replace with your actual device index
FILE_PATH = "/home/ubuntu/share/tmp/src/audio/temp.wav"

# API Config
HEADERS = {
    'Content-Type': 'audio/wav',
    'x-api-key': 'qqs7Jq96RQ6SUBwpsAlrZu5Y05MxVEfrXq0r0Y30',  # Replace with a valid API key if needed
}
URL = "https://1fl0qfare6.execute-api.us-east-1.amazonaws.com/default/puppyPiProcessingFunction"

responseString = None
running = True

def record_audio(filename=FILE_PATH):
    """Records audio and saves it as a WAV file."""
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

def hitcloud():
    """Sends recorded audio to cloud and retrieves the response."""
    global responseString
    try:
        with open(FILE_PATH, 'rb') as f:
            data = f.read()
        response = requests.post(URL, headers=HEADERS, data=data)
        data = response.json()
        print("Response JSON:", data)
        responseString = data.get("gpt_analysis")
        print('Response String:', responseString)
    except requests.exceptions.RequestException as e:
        print("Error:", e)
        responseString = None

def record_and_process_loop():
    """Continuously records audio, processes it, and triggers action groups."""
    global running
    while not rospy.is_shutdown() and running:
        record_audio()
        hitcloud()
        if responseString:
            action_group_file = action_groups_dict.get(responseString)
            print('Action Group File:', action_group_file)
            runActionGroup_srv(action_group_file, True)
        rospy.sleep(5)  # Wait before next iteration

def stop():
    """Stops the robot and ends the loop on shutdown."""
    global running
    PuppyVelocityPub.publish(x=0, y=0, yaw_rate=0)
    running = False
    print('Stopping...')

if __name__ == '__main__':
    rospy.init_node(ROS_NODE_NAME, log_level=rospy.INFO)
    rospy.on_shutdown(stop)

    # Initialize ROS Publishers & Services
    PuppyPosePub = rospy.Publisher('/puppy_control/pose', Pose, queue_size=1)
    PuppyGaitConfigPub = rospy.Publisher('/puppy_control/gait', Gait, queue_size=1)
    PuppyVelocityPub = rospy.Publisher('/puppy_control/velocity', Velocity, queue_size=1)
    runActionGroup_srv = rospy.ServiceProxy('/puppy_control/runActionGroup', SetRunActionName)
    set_mark_time_srv = rospy.ServiceProxy('/puppy_control/set_mark_time', SetBool)

    # Set Initial Pose & Gait Configurations
    PuppyPosePub.publish(**PuppyPose, run_time=500)
    rospy.sleep(0.5)
    PuppyGaitConfigPub.publish(**GaitConfig)

    #Start the recording and processing loop in a separate thread
    loop_thread = threading.Thread(target=record_and_process_loop)
    loop_thread.daemon = True  # Ensure it stops when the script exits
    loop_thread.start()

    #Let ROS handle everything else
    rospy.spin()
