import os
import time
import subprocess

print "sleep 10 s" # wait for audio device
time.sleep(10)
print "done"

os.system("sudo python /home/pi/autocheck_ir_command.py &")
result = None
while result is None:
    try:
    	subprocess.call(['aplay -fdat /home/pi/beep.wav'], shell=True)
        result = os.system("sudo su pi -c './launch-assistant.sh'")
    except:
         pass