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
	
		#Size of data, doesnt need to be large.
		self.size = 256
		
		#Buffers for incoming data and outgoing data
		self.outgoingData = bytearray(self.size)
		self.incomingData = bytearray(self.size)
	

		sys.stdout.write("")

		# Thread control
		self.running = 1
	def run(self):
		while self.running:
			try:		
				# Not sure if we have to set this here
				#self.client.settimeout(25.0)
				
				# Receive data and number of bytes read
				bytes = self.client.recv_into(self.incomingData, self.size)
			
				# self.incomingData
				while bytes < (self.incomingData[0]):
					# Get chunk of data
					chunk = self.client.recv(self.size)
					
					self.incomingData.extend(chunk)
					
					# Append to bytes counter
					bytes = bytes + len(chunk)
					
					# If we received 0 bytes, connection is closed, stop thread
					if len(chunk) == 0:
						self.running = 0
						break
					
				
				# Check that the connecting client nows our passphrase
				if chr(self.incomingData[1]) == "!" and chr(self.incomingData[2]) == "#":
					# We know this client
					
					for i in range(0, 5):
						if( i == 1 or i == 2):
							print "#{}: {}".format(i, chr(self.incomingData[i]))
						else:
							print "#{}: {}".format(i, self.incomingData[i])
					# Get the action code
					action_code = self.incomingData[3]
					print action_code
					# Action code:
					# * 1 Run movie
					# Byte 4 len of share folder name
					if action_code == 1: 
						message = "Welcome client"
						self.outgoingData[0] = len(message)# Number of bytes to send
						for i in range(1, len(message)):
							self.outgoingData[i] = ord(message[i - 1])
						self.client.send(self.outgoingData)
						
						count = 0
						for data in self.outgoingData:
							print data
							count ++
							if count > self.outgoingData[0]:
								break
						
					elif action_code == 2:
						self.client.send("Nice to meet you<EOF>")
				else:
					sys.stdout.write('Error: Unknown SocketType, close()\n')
					self.running = 0
			except socket.error, msg:

				sys.stdout.write('Error in socket program')
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
