#!/usr/bin/env python3

import bluetooth
import os
import sys

RMQserv = '127.0.0.1'
MDBport = 27017
RMQport = 5672
btMAC = 'F8:CF:C5:D1:4F:3E' #MAC Address of Jacob's cellular device with bluetooth capability
port = 1
backlog = 1
size = 1024

s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
#s.connect((btMAC, port))
print('[Checkpoint 01] Created socket at 0.0.0.0 on port ', port)
s.bind(("", port))
s.listen(backlog)
print('[Checkpoint 02] Listening for client connections')
try:
    client, address = s.accept()
    print('Accepted connection from ', address)
    while 1:
        data = client.recv(size)
        if data:
            print(data)
            client.send(data)
except:
    print("Error occured, closing Socket")
    client.close()
    s.close()

if len(sys.argv) > 1:
    if (sys.argv[1] == '-s'):    serv = int(sys.argv[2])
    
