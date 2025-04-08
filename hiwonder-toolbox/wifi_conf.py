#!/usr/bin/python3
#coding:utf8

import os
from dotenv import load_dotenv

load_dotenv("/home/pi/.env")

WIFI_MODE = 2                               #wifi的工作模式， 1为AP模式， 2为STA模式
#WIFI_AP_SSID = 'HW-Robot'                  #AP模式下的SSID。字符和数字构成,需要以 HW- 开头，否则app功能无法使用
#WIFI_AP_PASSWORD = 'hiwonder'        #AP模式下的WIFI密码,字符和数字构成
WIFI_STA_SSID = os.getenv('WIFI_STA_SSID')            #STA模式下的SSID
WIFI_STA_USERNAME = os.getenv('WIFI_STA_USERNAME')
WIFI_STA_PASSWORD = os.getenv('WIFI_STA_PASSWORD')    #STA模式下的WIFI密码  
