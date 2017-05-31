#!/usr/bin/env python

# Copyright (C) 2017 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from __future__ import print_function

import argparse
import os.path
import json

import google.oauth2.credentials

from google.assistant.library import Assistant
from google.assistant.library.event import EventType
from google.assistant.library.file_helpers import existing_file

import subprocess,os,re,time,threading

def process_event(event):
	"""Pretty prints events.

	Prints all events that occur with two spaces between each new
	conversation and a single space between turns of a conversation.

	Args:
		event(event.Event): The current event to process.
	"""

	if event.type == EventType.ON_CONVERSATION_TURN_STARTED:
		subprocess.call(['aplay -fdat /home/pi/beep.wav'], shell=True)
		print()

	print(event)

	if (event.type == EventType.ON_CONVERSATION_TURN_FINISHED and
			event.args and not event.args['with_follow_on_turn']):
		print()

	if event.type == EventType.ON_RECOGNIZING_SPEECH_FINISHED:
		#print(event.args["text"])
		text = event.args["text"].lower()
		text = text.replace("two","2")
		text = text.replace("ten","10")
		if "channel" in text:
			if hasNumbers(text):
				no = re.findall('\d+', text)[0]
				print("Go to channel "+no)
				sendIR(no)
				return 1
			elif "up" in text:
				sendIR("TOT_channelup")
				return 1
			elif "down" in text:
				sendIR("TOT_channeldown")
				return 1
		elif "volume" in text and "up" in text:
			if hasNumbers(text):
				n = re.findall('\d+', text)[0]
				t = threading.Thread(target = sendRepeatIR, args = ("TOT_volumeup", n))
				t.start()
			else:		
				sendIR("TOT_volumeup")
			return 1
		elif "volume" in text and "down" in text:
			if hasNumbers(text):
				n = re.findall('\d+', text)[0]
				t = threading.Thread(target = sendRepeatIR, args = ("TOT_volumedown", n))
				t.start()
			else:		
				sendIR("TOT_volumedown")
			return 1
		elif "back" in text:
			if hasNumbers(text):
				n = re.findall('\d+', text)[0]
				t = threading.Thread(target = sendRepeatIR, args = ("TOT_left", n))
				t.start()
			else:		
				sendIR("TOT_left")
			return 1
		elif "forward" in text:
			if hasNumbers(text):
				n = re.findall('\d+', text)[0]
				t = threading.Thread(target = sendRepeatIR, args = ("TOT_right", n))
				t.start()
			else:		
				sendIR("TOT_right")
			return 1						
		elif "tv" in text:
			if "on" in text or "off" in text:
				t = threading.Thread(target = sendMultiIR, args = (["TOT_power","TV_power"]))
				t.start()
				return 1
		elif "hdmi" in text and hasNumbers(text):
			n = int(re.findall('\d+', text)[0])
			if n == 3:
				t = threading.Thread(target = sendMultiIR, args = (["TOT_power","TV_input","TV_right","TV_right","TV_ok"],))
				t.start()
			elif n == 1:
				t = threading.Thread(target = sendMultiIR, args = (["TOT_power","TV_input","TV_left","TV_left","TV_ok"],))
				t.start()
			return 1				
		elif "ac" in text:
			if "on" in text:
				sendIR("AC_on")
				return 1				
			elif "off" in text:
				sendIR("AC_off")
				return 1
			elif "up" in text:
				sendIR("AC_up")
				return 1
			elif "down" in text:
				sendIR("AC_down")
				return 1
		elif "shut down" in text:
			print("shutdown now")
			subprocess.call(['aplay -fdat /home/pi/shutdown.wav'], shell=True)
			os.system("sudo shutdown -h now")
			return 1
		elif "restart" in text:
			print("restart now")
			subprocess.call(['aplay -fdat /home/pi/shutdown.wav'], shell=True)
			os.system("sudo reboot")
			return 1			

def sendMultiIR(commandlist):
	for c in commandlist:
		sendIR(c)
		time.sleep(1.2)

def sendRepeatIR(command,num):
	for i in range(0,int(num)):
		sendIR(command)
		time.sleep(1.2)

def sendIR(command):
	print("	Writing IR command: "+str(command))
	subprocess.call(['aplay -fdat /home/pi/beep.wav'], shell=True)
	f=open("/home/pi/ir_command.txt", "a+")
	f.write(str(command))
	f.close()

def hasNumbers(inputString):
	return any(char.isdigit() for char in inputString)

def main():
	parser = argparse.ArgumentParser(
		formatter_class=argparse.RawTextHelpFormatter)
	parser.add_argument('--credentials', type=existing_file,
						metavar='OAUTH2_CREDENTIALS_FILE',
						default=os.path.join(
							os.path.expanduser('~/.config'),
							'google-oauthlib-tool',
							'credentials.json'
						),
						help='Path to store and read OAuth2 credentials')
	args = parser.parse_args()
	with open(args.credentials, 'r') as f:
		credentials = google.oauth2.credentials.Credentials(token=None,
															**json.load(f))

	with Assistant(credentials) as assistant:
		for event in assistant.start():
			if process_event(event) == 1:
				assistant.stop_conversation()

if __name__ == '__main__':
	main()
