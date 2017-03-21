#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

Stationserver.py

Author: Erik Söderström
Company: Innoware Development AB
15 apr 2016


version 1.3

New in this version:

	Better defined, all around alarm functions.


A server that can serve mulptiple clients at once

 Server accepts sockConnect and then spawns a Client thread

"""
import select
import socket
import sys
import threading
from client import Client
import netifaces as ni

class Server:
	def __init__(self):
		ni.ifaddresses('eth0')
		ip = ni.ifaddresses('wlan0')[2][0]['addr']
		self.host = ip
		self.port = 9999
		
		self.backlog = 5
		self.size = 128
		self.server = None
		self.threads = []

	def open_socket(self):
		try:
			self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
			self.server.bind((self.host,self.port))
			self.server.listen(5)
		except socket.error, (value,message):
			if self.server:
				self.server.close()
			sys.stdout.write("\nCould not open socket: " + message)
			sys.exit(1)
	def run(self):
		self.open_socket()
		input = [self.server]
		running = 1
		
		
		# Write an welcome message to output
		sys.stdout.write('---[***Welcome to piMovie Server***]---\n')
		sys.stdout.write('Server is listening for attempts to connect...\n')
		# Flush output
		sys.stdout.flush()
	
		
		while running:
			inputready,outputready,exceptready = select.select(input,[],[])
			for s in inputready:
				if s == self.server:
					self.server.settimeout(30.0)
					
					c = Client(self.server.accept())
					c.start()
					self.threads.append(c)
		self.server.close()
		for c in self.threads:
			c.CancelThread()