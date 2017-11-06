#!/usr/bin/env python3
import socket
import os
import sys

RMQserv = '127.0.0.1'
MDBport = 27017
RMQport = 5672
btMAC = 'F8:CF:C5:D1:4F:3E' #MAC Address of Jacob's cellular device with bluetooth capability
port = 3
backlog = 1
size = 1024

try:
    s = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
    #s.connect((btMAC, port))
    print('[Checkpoint 01] Created socket at 0.0.0.0 on port ', port)
    s.bind((btMAC, port))
    s.listen(backlog)
    print('[Checkpoint 02] Listening for client connections')
    client, address = s.accept()
    while 1:
        data = client.recv(size)
        if data:
            print(data)
            client.send(data)
except socket.error as message:
    if s:
        s.close()
    print("Could not open socket: " + str(message))
    sys.exit(1)
    
while 1:
    input = raw_input()
    if input == "quit":
        break
    s.send(input)
sock.close()

if len(sys.argv) > 1:
    if (sys.argv[1] == '-s'):    serv = int(sys.argv[2])
    
