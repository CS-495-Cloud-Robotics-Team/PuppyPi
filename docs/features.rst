Features
========

This section outlines the key features of the PuppyPi Cloud Robotics system.

Core Features
-------------

.. list-table:: 
   :header-rows: 1
   :widths: 20 60

   * - Feature Name
     - Description
   * - Voice Command System
     - Allows control of the robot via vocal commands. Supports all basic movement commands from the original app - these include walking as well as all the Action Group files ('Performance' section of the app).
   * - Cloud Integration
     - Enables remote control and monitoring through cloud services.
   * - AI Prompt Control
     - Prompts Chat-GPT to interpret spoken phrases into individual commands.
   * - Extended Command Set
     - Adds new capabilities beyond the original app functionality, including chaining multiple commands together and command interruption.

Technical Features
------------------

.. list-table::
   :header-rows: 1
   :widths: 20 60

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
   * - Silence based command detection
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
   * - AI prompt
     - 
   * - Text transcription
     - 
   * - Continuous Command Duration Control
     - When asking the robot to do a continuous command such as "walk", request a number of seconds for the program to run for
   * - Automatic Stopping
     - When prompting the robot again while its executing commands it will stop its current command and delete all future commands
   * - Speaker functionality
     - Plays a barking sound to alert user that the robot is listening



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
- Final app functionalities - color tracking, apriltag recognition, and lidar
