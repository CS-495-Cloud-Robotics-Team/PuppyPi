#!/bin/bash
docker stop puppypi_ros2
xhost +
docker exec -u ubuntu -w /home/ubuntu puppypi /bin/zsh -c "source /home/ubuntu/puppypi/src/puppy_bringup/scripts/source_env.bash roslaunch puppy_bringup start_node.launch"


