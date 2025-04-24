Installation Guide
==================

This guide walks through how to deploy the PuppyPi Cloud Robotics application on your own PuppyPi Pro Ultimate robot.

Hardware Requirements
---------------------

To successfully deploy the application, you will need:

- A **PuppyPi Pro Ultimate** robot running on a **Raspberry Pi 5**
- The **Raspberry Pi extension board** (included with the Pro Ultimate version)
- A local machine or terminal capable of **SSH access** to the PuppyPi
  - We used **VNC Viewer**, but any SSH-compatible tool (e.g., terminal, PuTTY) will work

Software Requirements
---------------------

The deployment process is automated via a setup script. The software dependencies and resources include:

- **Git** (for cloning the project repository)
- **Zsh** (used for running the installation script)
- Internet access (for downloading dependencies and connecting to cloud services)

Installation Steps
------------------

1. **Access the PuppyPi**

   SSH into your PuppyPi. If using VNC Viewer, ensure the PuppyPi is powered on and on the same network.

2. **Setup**
  Navigate to HiWonder-toolbox, open wifi_conf.py, change WIFI_MODE to 2, change WIFI_STA_SSID to the         name of the network (if in Dr. Chris Crawford's lab, this would be HTIL Router), change wifi_sta_password to the network password, then save the file.

  
  Type in terminal
  
  .. code-block:: zsh

    sudo systemctl restart wifi.service
    cd /home/pi/
    git init
    git remote add origin https://github.com/CS-495-Cloud-Robotics-Team/PuppyPi
    git fetch origin main
    git reset --hard origin/main
    nano .env

  Edit in the .env file: 
  
  - PICO_ACCESS_KEY = enter Picovoice access key here
  - AWS_API_KEY = enter AWS api key here
  - WIFI_STA_SSID = enter network name here
  - WIFI_STA_USERNAME = enter username here, if Enterprise
  - WIFI_STA_PASSWORD = enter network password here

  .. code-block:: zsh

    cd /home/puppypi/
    sudo cp git_sync.service/etc/systemd/system/
    sudo systemctl enable git_sync.service

  .. code-block:: zsh

    cd /home/pi/controller/
    chmod +x setup_dependencies.zsh
    ./setup_dependencies.zsh

  Run in terminal:

    .. code-block:: zsh

      python3 controller.py
   
  This will run the controller program so everything should work.
  
  In order to make the controller script run on startup:

    .. code-block:: zsh

      cd /home/pi/controller/
      sudo cp controller_startup.service
      /etc/systemd/system/
      sudo systemctl enable controller_startup.service
      sudo reboot raspberrypi

3. **Provide Credentials When Prompted**

   The script will prompt for the following:

   - Wi-Fi credentials (choose one):
     - WPA2 Personal: SSID and password
     - WPA Enterprise (without CA certificate): SSID, username, and password
   - **API Key for Dr. Chris Crawford's AWS-based API**
   - **API Key for Picovoice** (used for wake word detection)

   Once the setup is complete, the script will:
   - Clone the GitHub repository into `/home/pi`
   - Install required system and Python packages
   - Configure services for cloud connectivity
   - Enable automatic startup for voice command listening

External Resources
------------------

The application relies on the following external services:

- **GitHub** (Free): Hosts the source code and deployment scripts
- **AWS Lambda + API Gateway**:
  - Used for cloud-based voice command processing
  - Default configuration uses Dr. Crawford’s API
  - Accepts `.wav` file input sent from the PuppyPi
- **Picovoice** (Free/Paid Tiers): Handles wake word detection

   If you do not have access to Dr. Crawford's API key, you can set up your own endpoint by:

   - Creating an **API Gateway** linked to an **AWS Lambda function**
   - Using the Lambda logic in the `lambda/function` directory of the repository
   - Creating a Lambda layer using the `openai-aws-lambda-layer-3.9.zip` file in the `lambda` directory
   - This setup enables the use of the OpenAI Python library within your Lambda function

Next Steps
----------

Once the installation is complete, refer to the :doc:`features` section to explore the available voice-controlled capabilities of the PuppyPi.
