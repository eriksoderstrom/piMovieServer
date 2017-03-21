#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import threading
import socket
import time
import datetime
import random
import os.path


class Client(threading.Thread):
	def __init__(self,(client,address)):
		threading.Thread.__init__(self)
		self.client = client
		self.address = address
		
		#Buffers for incoming data and outgoing data
		outgoingData = bytearray(128)
		incomingData = bytearray(128)
		
		#Size of data, doesnt need to be large.
		size = 128

		sys.stdout.write("")

		# Thread control
		self.running = 1
	def run(self):
		log_timer = time.time() + 30
		while self.running:
			try:		
				# Not sure if we have to set this here
				self.client.settimeout(25.0)
				
				# Receive data and number of bytes read
				bytes = self.client.recv_into(incomingData, size)
			
				# incomingData
				while bytes < (self.incomingData[0]):
					# Get chunk of data
					chunk = self.client.recv(size)
					
					incomingData.extend(byte)
					
					# Append to bytes counter
					bytes = bytes + len(byte)
					
					# If we received 0 bytes, connection is closed, stop thread
					if len(byte) == 0:
						self.running = 0
						break
					
				
				# Check that the connecting client nows our passphrase
				if chr(self.incomingData[1]) == "!" and chr(self.incomingData[2]) == "#":
					# We know this client
			
				else:
					sys.stdout.write('Error: Unknown SocketType, close()\n')
					self.running = 0
			except socket.error, msg:

				sys.stdout.write ('[Thread-id: {}][{}] - Uknown station: Socket error: {} - End client thread after {} loops.\n'.format(self.thread_id, st, msg, self.count))
				sys.stdout.write('Active threads: {}\n'.format(threading.activeCount() - 1))				
				self.running = 0
		# /End While running:
		# Close client socket after we complete While Loop.
		self.client.close()
		# Flush output
		sys.stdout.flush()
	# /End Run()
	def CancelThread(self):
		self.running = 0
