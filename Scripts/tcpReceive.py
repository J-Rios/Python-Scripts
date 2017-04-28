# -*- coding: utf-8 -*-
#
# Author: Jose Miguel Rios Rubio
# Description: Basic TCP Socket communication
# Creation Date: 29/04/2017
# Last modified Date: 29/04/2017
##############################################

# Modules
import socket
import sys
import uinput
import time

##############################################

# Constants
TCP_PORT = 8585

##############################################

# Main Function
def main():
	# Create, open and bind stream based (TCP) socket
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_addr = ('localhost', TCP_PORT)
	sock.bind(server_addr)

	# Wait for a client connection
	sock.listen(1)
	print "Waiting for client connection..."
	connection, client_address = sock.accept()
	print "Client conected"

	# Infinite loop
	while True:
		data = connection.recv(1024) # Receive message (max size 1024 bytes)
		print "Message received: ", data # Show the received message

##############################################

# Main Function call
if __name__ == "__main__":
	main()
