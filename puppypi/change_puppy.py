import os
import subprocess

result = subprocess.run(["docker", "ps"], stdout=subprocess.PIPE)
output = result.stdout.decode()

# 按行分割
lines = output.strip().split('\n')
# 获取最后一行
last_line = lines[-1]
# 按空格分割
columns = last_line.split()
# 获取 NAMES 列（最后一个元素）
container_name = columns[-1]

command = "~/software/puppypi_control/puppypi.sh"
#command_ros2 = 'source ~/.zshrc;sleep 0.01;ros2 launch peripherals usb_cam.launch.py;~/software/lab_tool/main.sh'
command_ros2 = 'source ~/.zshrc;sleep 0.01;~/software/puppypi_control/puppypi.sh;ros2 launch puppy_control puppy_control.launch.py;'

if container_name == 'puppypi':
    command_list = ["docker", "exec", "-u", "ubuntu", "-w", "/home/ubuntu", container_name, "/bin/zsh", "-c", command]
    subprocess.run(command_list)
    
if container_name == 'puppypi_ros2':
    command_list = ["docker", "exec", "-u", "ubuntu", "-w", "/home/ubuntu", container_name, "/bin/zsh", "-c", command_ros2]
    subprocess.run(command_list)