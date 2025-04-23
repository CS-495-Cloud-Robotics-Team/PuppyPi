Frequently Asked Questions (FAQs)
=================================

This section answers common questions that users may encounter while deploying, using, or troubleshooting the PuppyPi Cloud Robotics system.

1. How do I change the network the PuppyPi is connected to?
-----------------------------------------------------------

To change the Wi-Fi network:

1. SSH into the PuppyPi or connect via Micro HDMI.
2. Open the `.env` file:

   .. code-block:: zsh

      nano /home/pi/.env

3. Update the following fields:

   - `WIFI_STA_SSID`: Set this to your new network name.
   - `WIFI_STA_USERNAME`: Leave blank unless you're on a WPA Enterprise network.
   - `WIFI_STA_PASSWORD`: Enter the new network password.

4. Save the file and apply changes by either:

   - Rebooting the PuppyPi:

     .. code-block:: zsh

        sudo reboot raspberrypi

   - Or restarting the Wi-Fi service:

     .. code-block:: zsh

        sudo systemctl restart wifi.service

2. How does the command interpretation work via WebSocket?
----------------------------------------------------------

Command interpretation occurs through a cloud-to-robot interaction model:

- **Voice Command** (Cloud):
  - Interpreted on AWS Lambda using a custom dictionary in:
    `lambda/function/lambda_function.py`

- **Payloads** (Local):
  - Each recognized command corresponds to one or more payloads defined in:
    `controller/payloads_dict.py`

These payloads are sent via WebSocket to the PuppyPi’s ROS Docker, which executes the associated actions via ROS topics and services. Complex or chain commands are composed as sequences of payloads.

To add new commands:

1. Add an entry to the cloud command dictionary.
2. Map that command to a local payload in `payloads_dict.py`.

3. Why is the PuppyPi running slowly?
-------------------------------------

The system’s performance is often tied to **network strength**:

- Audio commands are recorded and sent as `.wav` files via a POST request to AWS.
- Long commands or weak Wi-Fi can result in **delays up to several seconds**.

**Recommendations:**

- Use a strong, stable Wi-Fi signal.
- Shorten spoken commands when possible.
- Monitor local network latency.

Even long (~10 second) audio clips typically upload in 1–2 seconds on a good connection.

4. Why does the PuppyPi stop listening after 10 seconds?
--------------------------------------------------------

This is intentional — a timeout prevents the system from recording indefinitely due to loud ambient noise.

- The timeout duration is controlled by the `max_duration` variable in:

  .. code-block:: python

     controller/controller.py

To increase the timeout:

1. Open the file in a text editor.
2. Modify the `max_duration` variable (in seconds).
3. Save and restart the service or reboot the PuppyPi.

Be aware that longer audio files take longer to upload to the cloud and process.

5. How do I create new commands and make the PuppyPi perform them?
------------------------------------------------------------------

This can be done through the use of ROS, websockets, and the lambda function.

1. Find the ROS commands used to perform the functionality you want. This can require using multiple commands such as rostopic list, rosservice list, etc. We used VNC Viewer to check if the ROS commands worked - make sure you are using the Terminator (ROS1) and not the Terminal.
2. Figure out the proper format for these commands. This can require using rosservice info and other commands.
3. Convert the ROS commands to websocket format. Look at the payload_dictionary as an example - the "sit" command is really a "rosservice call /puppy_control/runActionGroup/sit.d6ac" command. Many functionalities require multiple commands, such as calling set_running or /enter or /exit.
4. Add the command words to the lambda function
5. Troubleshoot usage in controller.py - many specialized functionalities require additional changes to the controller code.

5. What are some examples of ROS commands?
------------------------------------------
Any Action Group: rosservice call /puppy_control/runActionGroup/[insert action group filename].d6ac

Start Walking: 
- rosservice call /puppy_control/set_running True
- rostopic pub /cmd_vel geometry_msgs/Twist "{ linear: { x: 1.0, y: 0.0, z: 0.0 }, angular: { x: 0.0, y: 0.0, z: 0.0 } }"

Stop Walking: 
- rostopic pub /cmd_vel geometry_msgs/Twist "{ linear: { x: 0.0, y: 0.0, z: 0.0 }, angular: { x: 0.0, y: 0.0, z: 0.0 } }"
- rosservice call /puppy_control/set_running False

7. What is all the stuff in the VNC Viewer?
-------------------------------------------
- Terminator - used for running ROS1 commands, and is inside the docker
- Terminal - used for running python programs, outside the docker
- Lab Tool - camera viewing

For more info & details on the app and other functionalities make sure to check out the HiWonder PuppyPi documentation: https://docs.hiwonder.com/projects/PuppyPi/en/latest/

Also, you can email HiWonder with questions if you get very stuck. Their customer support is helpful.

Additional Notes and Troubleshooting
====================================

Network Connectivity Issues
---------------------------

- **Initial Setup Failures**: DNS issues between the Raspberry Pi and its Docker containers can occasionally prevent internet access. These are partially resolved by our setup script, but manual DNS configuration may be necessary.
- **Large Networks**: On large or enterprise networks, the PuppyPi’s IP may be hidden. If SSH fails:
  - Connect via Micro HDMI (port is next to the power switch).
  - Edit `/home/pi/.env` manually to switch to a simpler network.

- **Access Point Mode**: If no valid network is found, the PuppyPi enters **Access Point Mode** (`HW-...`), which allows SSH access. However, it cannot process cloud commands in this mode.

Picovoice API Expiration
------------------------

- The **free tier** of the Picovoice API may expire or limit access.
- If wake word detection fails, verify or update your API key.

To update API keys:

1. Open `.env` in the `/home/pi` directory:

   .. code-block:: zsh

      nano /home/pi/.env

2. Update the following:

   - `PICO_ACCESS_KEY`: Picovoice API key
   - `COMMAND_API_KEY`: AWS Lambda key

3. Save the file and restart the Raspberry Pi:

   .. code-block:: zsh

      sudo reboot raspberrypi
