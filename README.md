# Google-Assistant-SDK-Broadlink-RM-Pro
Modification Gogole Assistant SDK on Raspberry Pi with Broadlink RM Pro


<h2>Requirement</h2>
Google Assistant on Raspberry Pi
https://developers.google.com/assistant/sdk/prototype/getting-started-pi-python/<br>
Python control for Broadlink RM2 IR controllers
https://github.com/mjg59/python-broadlink


<h3>To make Google Assistant run on startup:</h3>
```
sudo chmod +x launch-assistant.sh
sudo nano /etc/rc.local
Add /home/pi/launch-assistant.sh
```

