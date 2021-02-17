#!/bin/bash

#sudo python3 main.py --device_addr "2818117-893931543"
sudo openocd -f /home/pi/Desktop/flasher/debug.cfg & sudo python3 main.py --device_addr "2818117-893931543" && fg
