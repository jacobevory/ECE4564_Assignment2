#!/usr/bin/env python3
import bluetooth
import os
import sys

serv = '127.0.0.1'
btMAC = 'F8:CF:C5:D1:4F:3E'
port = 1
s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
s.connect((btMAC, port))
while 1:
    input = raw_input()
    if input == "quit":
        break
    s.send(input)
sock.close()

if len(sys.argv) > 1:
    if (sys.argv[1] == '-s'):    serv = int(sys.argv[2])
    
