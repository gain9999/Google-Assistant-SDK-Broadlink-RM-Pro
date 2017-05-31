import os.path,os
import broadlink,time

print "Connecting to broadlink..."
devices = broadlink.discover(timeout=5)
print devices
devices[0].auth()

commandfile = "ir_command.txt"
ircode_dir = "/home/pi/ir_codes/"

print "Running auto check ir command..."
while True:
	try:
		if(os.path.exists(commandfile)):
			f=open(commandfile, "r")
			button = f.read()
			f.close()
			if button.isdigit():
				if len(button) == 1:
					f=open(ircode_dir+button+".txt", "r")
					ir_packet = f.read()
					f.close()
					devices[0].send_data(ir_packet)
				elif len(button) == 2:
					no_array = list(str(button))
					for n in no_array:
						f=open(ircode_dir+n+".txt", "r")
						ir_packet = f.read()
						f.close()
						devices[0].send_data(ir_packet)
			else:
				f=open(ircode_dir+button+".txt", "r")
				ir_packet = f.read()
				devices[0].send_data(ir_packet)
				f.close()		
			print "	+ Send "+button+" IR packet"
			os.remove(commandfile)
		time.sleep(1)
	except (KeyboardInterrupt, SystemExit):
	    print '\n...Program Stopped Manually!'
	    raise