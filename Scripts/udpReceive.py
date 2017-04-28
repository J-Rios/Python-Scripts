# -*- coding: utf-8 -*-
#
# Author: Jose Miguel Rios Rubio
# Description: Basic UDP Socket communication
# Creation Date: 29/04/2017
# Last modified Date: 29/04/2017
##############################################

# Modules
import socket

##############################################

# Constants
UDP_IP = ""
UDP_PORT = 8585

##############################################

# Main Function
def main():
	# Create, open and bind datagram based (UDP) socket
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock.bind((UDP_IP, UDP_PORT))
	print "Port " + str(UDP_PORT) + " opened"

	# Infinite loop
	while True:
		data, addr = sock.recvfrom(1024) # Receive message (max size 1024 bytes)
		print "Message received: ", data # Show the received message
		if data == "CMD_HELLO": # If message is "CMD_HELLO"
			sock.sendto("Hello command received", addr) # Send a response

##############################################

# Main Function call
if __name__ == "__main__":
	main()
