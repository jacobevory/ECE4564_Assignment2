#!/usr/bin/env python3
import os
os.system("sudo bluetoothctl")
os.system("connect F8:CF:C5:D1:4F:3E")

serv = 127.000.000.001

if len(sys.argv) > 1:
    if (sys.argv[1] == '-s'):    serv = int(sys.argv[2])
      
