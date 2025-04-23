Features
========

This section outlines the key features of the PuppyPi Cloud Robotics system.

Core Features
-------------

.. list-table:: 
   :header-rows: 1
   :widths: 20 80

   * - Feature Name
     - Description
   * - Voice Command System
     - Allows control of the robot via vocal commands. Supports all basic movement commands from the original app - these include walking as well as all the Action Group files ('Performance' section of the app).
   * - Cloud Integration
     - Enables remote control and monitoring through cloud services.
   * - AI Prompt Control
     - Prompts ChatGPT to interpret spoken phrases into individual commands.
   * - Extended Command Set
     - Adds new capabilities beyond the original app functionality, including chaining multiple commands together and command interruption.

Technical Features
------------------

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Component
     - Description
   * - On-startup running
     - When the robot is turned on, it automatically runs controller.py (you can turn this off)
   * - Automatic github download
     - When the robot is turned, on it automatically pulls from the github with updated code
   * - Network interoperability
     - The robot can connect to various networks by going into the Raspberry Pi and connecting to the specific network via the terminal
   * - PyAudio recording
     - Uses pyaudio library to record and edit audio files input by the user via the mic
   * - Noise reduction
     - Uses vad python library to limit the amount of audio input to help get a clear command
   * - Audio compression
     - Uses audio compression techniques to speed up sending audio files to the cloud
   * - Silence/time based spoken command detection
     - After the robot hears silence for 1.5 seconds it will assume the user has finished saying the command. After 10 seconds, it hard stops to ensure backround noise doesn't make it record forever
   * - Wake Word Detection
     - Uses picovoice python library to create a wake word (default = 'PuppyPi', can be edited by user) that detects when the word is said to initalize the prompting
   * - Bluetooth mic
     - Optional external bluetooth mic/headset to greatly increase amount of correct audio transmitted to the PuppyPi (without this there is a large chance the motors drown out user's voice)
   * - Websocket
     - Uses an external websocket system to send information into the docker file to run specific commands, this way the code isn't deleted on startup
   * - Command queue
     - A queue called "command_queue" to store which commands to run in a specific order across threads. This allows for multicommand execution
   * - Payload dictionary
     - A list of payloads connected via command_queue words (ex. "walk") that tell ROS what to execute on the PuppyPi motors
   * - Text transcription
     - Uses OpenAI Wisper to convert the user's spoken phrase into text for the AI prompt, works in many different languages.
   * - AI prompt
     - A long string inside the lambda function that prompts gpt for a set of commands based on the user's phrase (first turned audio into text for prompt). This can be changed for specific edge cases with additional prompting.
   * - Continuous Command Duration Control
     - When asking the robot to do a continuous command such as "walk", request a number of seconds for the program to run for
   * - Automatic Stopping
     - When prompting the robot again while its executing commands it will stop its current command and delete all future commands
   * - Speaker functionality
     - Plays a barking sound to alert user that the robot is listening
   * - Multilingual
     - Able to understand commands in most languages, including Google Translated commands
   * - Command generation
     - Ability to perform non-existing commands if the functionality could be created by a chain of current commands, such as "walk in a square" (walking and turning)
   * - Variable time commands
     - Specifically for walk the user can ask for a number of seconds it should walk for, will be input into the command_queue and interpreted by the code in controller.py
   * - Face Detection
     - When this command is run the robot will wave its paw when it detects a face
   * - Color Detection
     - When this command is run the robot will nod its head when a specific color is found
   * - Visual Patrol/Line following
     - When this command is run the robot will follow a line of a specific color

List of Current Voice-Executable Commands
-----------------------------------------

.. list-table:: 
   :header-rows: 1
   :widths: 20 20 20 20 20

   * - Action
     - Description
     - Type
     - Parameters/Notes
     - Sample Command
   * - Two leg stand
     - Make the PuppyPi stand on its two back legs
     - Rosservice, action group
     - N/A
     - "PuppyPi, can you stand on two legs?"
   * - Bow
     - Make the PuppyPi do a bowing motion by lowering its head
     - Rosservice, action group
     - N/A
     - "PuppyPi, can you bow?"
   * - Boxing
     - Make the PuppyPi stand on its hind legs and punch with its front legs
     - Rosservice, action group
     - N/A, boxing-main and boxing-alt do the same thing
     - "PuppyPi, do a boxing punch"
   * - Grab
     - Make the PuppyPi grab the object in front of it with its detachable arm
     - Rosservice, action group
     - N/A, untested functionality, for grabber arm only
     - "PuppyPi, grab with your arm"
   * - Jump
     - Make the PuppyPi "jump"
     - Rosservice, action group
     - N/A, does not jump high at all
     - "PuppyPi, jump for me"
   * - Kick ball
     - Make the PuppyPi kick forward with its front feet
     - Rosservice, action group
     - Kick-ball-left or kick-ball-right, do not know what kick-ball-left-bak does
     - "PuppyPi, can you kick with your left/right foot"
   * - Lie down
     - Make the PuppyPi lie down
     - Rosservice, action group
     - N/A
     - "PuppyPi, can you lie down?"
   * - Look down
     - Make the PuppyPi look down
     - Rosservice, action group
     - look-down-short doesn't seem to do anything different
     - "PuppyPi, can you look down?"
   * - Moonwalk
     - Make the PuppyPi do the moonwalk - 4 sets of leg movements
     - Rosservice, action group
     - N/A
     - "PuppyPi, can you do the moonwalk?"
   * - Nod
     - Make the PuppyPi nod its head up and down
     - Rosservice, action group
     - N/A
     - "PuppyPi, can you nod your head?"
   * - Pee
     - Make the PuppyPi do a peeing motion
     - Rosservice, action group
     - N/A
     - "PuppyPi, can you pee on the floor?"
   * - Push-up
     - Make the PuppyPi do 2 push ups
     - Rosservice, action group
     - N/A
     - "PuppyPi, can you do some push ups?"
   * - Run
     - Make the PuppyPi run - version of the "walk" command with faster linear x velocity
     - Rostopic publish to /cmd_vel geometry_msgs/Twist
     - N/A
     - "PuppyPi, can you run?"


Future Features
---------------

.. note::

   These are planned features under consideration for future development

- Advanced gesture recognition
- Autonomous navigation capabilities
- Multi-robot coordination system
- Enhanced security features for cloud connectivity
- Utilizing the arm that comes with the PuppyPi to pick up and grab objects
- More advanced computer vision techniques, allowing PuppyPi to dynamically interact with its environment
- Ability to run python programs on PuppyPi instead of individual ROS commands one by one
- Final app functionalities - color tracking
- Advanced command generation - ability to extrapolate and move PuppyPi creatively
- Allowing face detection, line following, color detection, & lidar to be interrupted with a call to the wake word
