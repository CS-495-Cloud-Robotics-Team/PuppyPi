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
     - Allows control of the robot via vocal commands. Supports all basic movement commands from the original app.
   * - Cloud Integration
     - Enables remote control and monitoring through cloud services.
   * - AI Prompt Control
     - Prompts Chat GPT to interpret spoken phrases into individual commands.
   * - Extended Command Set
     - Adds new capabilities beyond the original app functionality.

Technical Features
------------------

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Component
     - Description
   * - on startup running
     - When the robot is turned on it automatically runs controller.py (you can turn this off)
   * - automatic github download
     - When the robot is turned on it automatically pulls from the github with updated code
   * - network interoperability
     - The robot can connect to various networks by going into the raspberry pi and connecting to the specific network via the terminal
   * - pyaudio recording
     - Uses pyaudio library to record and edit audio files input by the user via the mic
   * - noise reduction
     - uses vad python library to limit the amount of audio input to help get a clear command
   * - audio compression
     - uses audio compression techniques to speed up sending audio files to the cloud
   * - Silence based command detection
     - After the robot hears silence for 1.5 seconds it will assume the user has finished saying the command, will also hard stop after 10 seconds to ensure backround noise doesn't make it record forever
   * - Wake Word Detection
     - Uses picovoice python library to create a wake word (puppypi/user choice) that detects when the word is said to initalize the prompting
   * - Bluetooth mic
     - optional external bluetooth mic/headset to greatly increase amount of correct audio transmitted to the puppypi (wihtout this there is a large chance the motors drown out users voice)
   * - web socket
     - Uses an external websocket system to send information into the docker file to run specific commands, this way the code isn't deleted on startup
   * - command queue
     - a queue called "command_queue" to store which commands to run in a specific order across threads
   * - payload dictionary
     - A list of payloads connected via command_queue words (ex. "walk") that tell ross what to execute on the puppypi motors
   * - ai prompt
     - 
   * - text transcription
     - 
   * - Continuous Command Duration Control
     - when asking the robot to do a continuous command such as "walk", request a number of seconds for the program to run for
   * - Automatic Stopping
     - When prompting the robot again while its executing commands it will stop its current command and delete all future commands
   * - multicommand execution
     - 
   * - payload dictionary
     - 
   * - Face Detection
     - 
   * - speaker functionality
     - plays a barking sound to alert user that the robot is listening



Future Features
---------------

.. note::

   These are planned features under consideration for future development

- Advanced gesture recognition
- Autonomous navigation capabilities
- Multi-robot coordination system
- Enhanced security features for cloud connectivity
