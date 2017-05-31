import broadlink
import time

devices = broadlink.discover(timeout=5)
print devices
devices[0].auth()

#learning 
while True:
	try:
		commandname = raw_input('Enter a button name: ')
		devices[0].enter_learning()
		ir_packet = None
		while ir_packet == None:
			ir_packet = devices[0].check_data()		
		f=open("/home/pi/ir_codes/"+commandname+".txt", "a+")
		f.write(ir_packet)
		f.close()
		print(commandname+" button Saved!")
	except (KeyboardInterrupt, SystemExit):
	    print '\n...Program Stopped Manually!'
	    raise

# # test sending ir packet
# ircode_dir = "/home/pi/ir_codes/"
# f=open(ircode_dir+"TV_ok.txt", "r")
# ir_packet =f.read()
# print "send ir packet"
# devices[0].send_data(ir_packet)