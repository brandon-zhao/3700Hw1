#!/usr/bin/env python3

import string
import socket
import json
import argparse
import ssl
import sys

# Get arguments from command line
parser = argparse.ArgumentParser(description='CS 3700 socket')
parser.add_argument('-p')
parser.add_argument('-s')
parser.add_argument('hostname')
parser.add_argument('Northeastern_username')
args = parser.parse_args()

HOST = args.hostname
WordSize = 5

print(HOST)

PORT = 27993
if args.p is int:
	PORT = args.p


# Establish socket (TCP)
try:
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except:
	print('Failed to create socket')
	sys.exit()

# Establish socket (TCL)
if args.s is not None:
	try:
		s = ssl.wrap_socket(s, ssl_version=ssl.PROTOCOL_TLSv1)
	except:
		print('Failed to create TCL connection')


s.connect((HOST, PORT))

print("Connected to host.")

try: 
	s.sendall(json.dumps({"type": "hello",
					"northeastern_username": args.Northeastern_username}).encode('ascii'))
except:
	print('Message send failed')
	sys.exit


# Get game ID from start message
startData = b''
stream = True

while stream:
	try:
		startData += s.recv(1500)
	except socket.error as e:
		stream = False