#!/bin/bash
xhost + 
docker exec -it -u ubuntu -w /home/ubuntu puppypi /bin/zsh -c "source /home/ubuntu/puppypi/.zshrc; python3 /home/ubuntu/software/puppypi_control/arm_Test.py"
