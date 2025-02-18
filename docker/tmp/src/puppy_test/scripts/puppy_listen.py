#!/usr/bin/env python3
# coding=utf8

#Author: Eli Weber
#Date: 2/15/25
#file to test cloud speech connection

import os
import sys
import math
import rospy
from std_srvs.srv import SetBool
from puppy_control.msg import Velocity, Pose, Gait
#Action Group Include
from puppy_control.srv import SetRunActionName
#Includes for json and curl requests
import json
import requests
# #Dictionary Include - dictionary must be in the same directory as this for reference to work
from action_groups_dict import action_groups_dict

runActionGroup_srv = rospy.ServiceProxy('/puppy_control/runActionGroup', SetRunActionName)


#Curl command to get the json string from the cloud
# Set up headers with content type and API key (if required)
headers = {
    'Content-Type': 'audio/wav',
    'x-api-key': '[redacted]', 
}

# Path to the audio file           ---Relies on saved audio file, change to real-time audio stream later
file_path = '/home/ubuntu/share/tmp/src/puppy_test/shake.wav'  # actual file path in docker

# Read the file in binary mode
with open(file_path, 'rb') as f:
    data = f.read()

# The API endpoint
url = "https://1fl0qfare6.execute-api.us-east-1.amazonaws.com/default/puppyPiProcessingFunction"

try:
    # Make the POST request
    response = requests.post(url, headers=headers, data=data)
    data = response.json()
    print("Response JSON:", data)  # Pretty print the JSON response
    #Respnse is JSON formatted as: {'transcription': 'Sit, puppy pie, sit.', 'gpt_analysis': 'sit'}

except requests.exceptions.RequestException as e:
    print("Error:", e)

# Get Command string from json response
responseString = gpt_analysis = data.get("gpt_analysis")
print('Response String value for gpt_analysis after transferred into python string:', responseString)

#Get the action group file from the dictionary
action_group_file = action_groups_dict.get(responseString)
print('Action Group File:', action_group_file)

runActionGroup_srv(action_group_file,True)
rospy.sleep(2)



