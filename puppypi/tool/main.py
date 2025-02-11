#!/usr/bin/env python3
# encoding: utf-8
import os
import sys
import time
from PyQt5.QtWidgets import (QWidget, QLabel, QComboBox, QPushButton,
                             QApplication, QHBoxLayout, QVBoxLayout)

class App(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        self.setWindowTitle('ROS选择器')

        # 控件
        self.label = QLabel('选择ROS版本:')
        self.combo = QComboBox()
        self.combo.addItems(['ROS1', 'ROS2'])

        self.btn_confirm = QPushButton('Save') 
        self.btn_exit = QPushButton('exit')
        
        # 设置窗口大小
        self.resize(320, 300)

        # 布局
        hbox = QHBoxLayout()
        hbox.addWidget(self.label)
        hbox.addWidget(self.combo)

        buttons_hbox = QHBoxLayout()
        buttons_hbox.addWidget(self.btn_confirm)  
        buttons_hbox.addWidget(self.btn_exit)

        vbox = QVBoxLayout()
        vbox.addLayout(hbox)
        vbox.addLayout(buttons_hbox)
        self.setLayout(vbox)

        # 连接槽函数
        self.btn_confirm.clicked.connect(self.handleConfirm)
        self.btn_exit.clicked.connect(self.close)

        self.show()

    def handleConfirm(self):
        if self.combo.currentText() == 'ROS1':
            os.system("docker stop puppypi_ros2")
            time.sleep(0.02) 
            os.system("docker start puppypi")
            time.sleep(0.02)
            os.system('sudo systemctl restart start_node.service')
            
            print('Running ROS1...')
        elif self.combo.currentText() == 'ROS2':
            os.system('sudo systemctl stop start_node.service')
            time.sleep(0.02)
            os.system("docker stop puppypi")
            time.sleep(0.02)
            os.system('~/puppypi/.stop_ros1.sh')
            time.sleep(0.02)
            os.system("docker start puppypi_ros2")
            time.sleep(0.02) 
            
            print('Running ROS2...')
        else:
            print('Please select ROS version')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())