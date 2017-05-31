# Google-Assistant-SDK-Broadlink-RM-Pro
Modification Gogole Assistant SDK on Raspberry Pi with Broadlink RM Pro


## Requirement
* Google Assistant on Raspberry Pi
https://developers.google.com/assistant/sdk/prototype/getting-started-pi-python/
* Python control for Broadlink RM2 IR controllers
https://github.com/mjg59/python-broadlink


#### To make Google Assistant run on startup:
```
sudo chmod +x launch-assistant.sh
sudo nano /etc/rc.local
Add /home/pi/launch-assistant.sh
```

#### To learn and save IR code for each button
1. create folder ir_codes in /home/pi
2. run ir.py
3. enter button name

Since Google Assistant run on Python 3 and Broadlink API run on Python 2 I wrote autocheck_ir_command.py to check the IR command from text file every 1 second. The IR command is created by Google Asssitant in __main__.py There might be a better way around to do this though.

Location of __main__.py: /home/pi/env/local/lib/python2.7/site-packages/google/assistant/
