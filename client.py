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

introMessage = {"type": "hello",
				"northeastern_username": args.Northeastern_username}
s.sendall(json.dumps(introMessage).encode('utf-8') + b"\n")

print(introMessage)

# Get game ID from start message
startData = s.recv(2000)
print(startData)
message = startData.decode("utf-8")
print(b"Welcome message" + startData)

print("Recieved message %s" % message)

startMessage = json.loads(message)
gameID = startMessage['id']
print(gameID)

alphabet_string = string.ascii_lowercase
aList = list(alphabet_string)

# List that stores correct letters for final answer
answerList= []
# Map that stores the correct letter positioning for the final answer
answerMap = {}

# main loop
guessing = True
while guessing:
	for letter in aList:
		s.sendall(json.dumps({"type": "guess",
					"id": gameID,
					"word": "adieu"}).encode('utf-8') + b"\n")
		guessResponse = s.recv(2000)
		print(guessResponse)
		guessData = guessResponse['guesses']
		print(guessData)
		i = 0
		while i < WordSize:
			if guessResponse[i] == 2:
				answerMap[i] = letter
			i+=1
		if len(answerMap.keys) == 5:
			guessing = False

s.sendall(json.dumps({"type": "guess",
			"id": gameID,
			"word": answerMap.get(1) + answerMap.get(2) + 
			answerMap.get(3) + answerMap.get(4) + answerMap.get(5)}).encode('utf-8') + b"\n")

guessResponse = s.recv(2000)
guessData = guessResponse['guesses']

if guessData['type'] == "bye":
	print(guessData['flag'])


		

