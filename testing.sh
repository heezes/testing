
#!/bin/bash

#sudo python3 main.py --device_addr "2818117-893931543"
source /home/pi/Desktop/flasher/src/debug.sh & sudo python3 main.py --device_addr "2621513-893931545"  --ble_interface True && fg
#sudo python3 main.py --device_addr "2621513-893931545" --ble_interface False &
