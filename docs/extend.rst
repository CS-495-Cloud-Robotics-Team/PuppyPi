Extending and Modifying the Software
====================================

This guide provides instructions for developers and contributors who wish to modify or extend the functionality of the PuppyPi Cloud Robotics system.

Getting Started
---------------

To begin development, SSH into the PuppyPi and navigate to the working directory:

.. code-block:: zsh

   ssh pi@<puppypi-ip-address>
   cd /home/pi

You can SSH through VSCode or VNC Viewer for ease of coding.

The project’s major components are structured as follows:

- **Wi-Fi Configuration**
  - Located in: `/home/pi/hiwonder-toolbox`
  - Files to modify:
    - `wifi.py`
    - `wifi-conf.py`

- **Controller Service**
  - Located in: `/home/pi/controller`
  - Main script: `controller.py`
  - This service handles logic for wake word detection, API requests, and interpreting cloud responses.

- **Wake Word Configuration**
  - Wake word file: `ScuffyWakeWord.ppn`
  - To customize, retrain a wake word via the [Picovoice Console](https://console.picovoice.ai/) and replace the existing `.ppn` file.
  - Ensure the file is named exactly the same or update the reference in `controller.py`.

- **Robot Functionality (Caution)**
  - Requires interaction with the internal PuppyPi Docker container.
  - This container controls motor functions and system-level behavior.
  - **Do not restart or delete this container**, or you will need to re-flash the SD card with the original PuppyPi system image.

Language and Tools
------------------

- **Primary Language**: Python
- **Shell**: Zsh
- **Compiler**: Not applicable (interpreted language)
- **Build System**: None (runtime services)

Build and Integration
---------------------

- There are no automated builds, as the system is designed to run as persistent services.
- To implement **continuous integration**, modify the `git_sync.service` in the `/home/pi/puppypi` directory.

  Steps to configure:

  1. Edit `git_sync.service` and replace the GitHub URL with your own.
  2. Copy it into the systemd services directory:

     .. code-block:: zsh

        sudo cp git_sync.service /etc/systemd/system/
        sudo systemctl enable git_sync.service
        sudo systemctl start git_sync.service

Adding New Functionality
------------------------

- **New Wake Words**: Train via Picovoice, replace `.ppn` file.
- **New ROS Payloads**:
  - Edit `payloads_dict.py` in the `controller` directory.
  - Add a new key-value pair that maps a cloud response to an action.
  - To figure out the command you need: 

1. Find the ROS commands used to perform the functionality you want. This can require using multiple commands such as rostopic list, rosservice list, etc. We used VNC Viewer to check if the ROS commands worked - make sure you are using the Terminator (ROS1) and not the Terminal.
2. Figure out the proper format for these commands. This can require using rosservice info and other commands.
3. Convert the ROS commands to websocket format. Look at the payload_dictionary as an example - the "sit" command is really a "rosservice call /puppy_control/runActionGroup/sit.d6ac" command. Many functionalities require multiple commands, such as calling set_running or /enter or /exit.


- **Cloud Command Mapping**:
  - Located in the Lambda function (`lambda/function/commands.py`).
  - Ensure cloud-side updates match the expected payloads on the PuppyPi.
  - Troubleshoot usage in controller.py - many specialized functionalities require additional changes to the controller code.

Testing and Validation
----------------------

Due to the physical nature of the robot, **testing is performed manually**.

- **Wake Word & Command Tests**:
  - Speak commands such as:
    - “Scuffy, do the moonwalk”
    - “Scuffy, walk forward and then turn right”
  - Observe behavioral output.

- **Cloud API Tests**:
  - Send `.wav` files via POST requests to the Cloud API.
  - Verify the returned command string matches expected interpretation.

.. code-block:: json

   {
     "audio": "<base64-encoded-wav>",
     "format": "wav"
   }

  Use tools like `curl` or Postman for testing requests.

Backlog and Known Issues
------------------------

Project issues and enhancement requests are tracked on GitHub:

- Issues: https://github.com/CS-495-Cloud-Robotics-Team/PuppyPi/issues

**Major known issues** include:

- Testing compatibility with newer PuppyPi models (Standard, Advanced, Pro)
- Enhancing spatial awareness to detect colored objects beyond a few feet (wider-room context tracking)
- Occasional GPT issues including seemingly random glitches of PuppyPi not knowing what you're saying
- Getting overwhelmed by multiple requests or poor network connectivity
- Low-quality microphones resulting in poor performance and inability to perform certain commands
- Horrific battery life
- More testing on Face Detection, Line Following, Lidar, & Color Detection is needed - specifically, making sure the exit scripts are run and seeing if they can be interrupted.

Code Style Guidelines
---------------------

- Follow **PEP8** guidelines for Python code
- Use clear, descriptive variable and function names
- Comment all critical logic blocks and decisions
- Avoid hardcoding paths, use configuration files or environment variables where possible

Pull requests should include a brief explanation and links to related GitHub issues, if applicable.
