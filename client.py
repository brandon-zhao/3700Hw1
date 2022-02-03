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
	introMessage = {"type": "hello",
					"northeastern_username": args.Northeastern_username}.encode('ascii')
	s.sendall(json.dumps(introMessage) + "\n")
except:
	print(introMessage)
	print('Message send failed')
	sys.exit

print

# Get game ID from start message
startData = b''
stream = True

while stream:
	try:
		startData += s.recv(1500)
	except socket.error as e:
		stream = False


print(startData)
message = startData.decode("ascii")

print("Recieved message %s" % message)

startMessage = json.loads(message)
gameID = startMessage['id']

alphabet_string = string.ascii_lowercase
aList = list(alphabet_string)

# Map that stores the correct letter positioning for the final answer
answerMap = {}

# main loop
while True:
	for letter in aList:
		s.sendall(json.dumps({"type": "guess",
					"id": gameID,
					"word": letter + letter + letter + letter + letter}).encode('utf-8'))
		guessResponse = s.recv(1500)
		guessData = guessResponse['guesses']
		i = 0
		while i < WordSize:
			if guessResponse[i] == 2:
				answerMap[i] = letter
			i+=1
		if len(answerMap.keys) == 5:
			s.sendall(json.dumps({"type": "guess",
						"id": gameID,
						"word": answerMap.get(1) + answerMap.get(2) + 
						answerMap.get(3) + answerMap.get(4) + answerMap.get(5)}).encode('utf-8'))
		if guessData['type'] == "bye":
			print(guessData['flag'])
			break
	break


		

