#!/usr/bin/env python3

import bluetooth
import os
from rmq_param import *
import pika
import sys
import time
import pymongo

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
    
mongodb = pymongo.MongoClient()[rmq_params['exchange']]
for q in rmq_params['queues']:
    col = mongodb[q]
    col.drop()

print("[Checkpoint 01] Connected to database ", rmq_params['exchange'], " on MongoDB server localhost")

creds = pika.PlainCredentials(rmq_params['username'],
                              rmq_params['password'])
connectparams = pika.ConnectionParameters(host=sys.argv[2],
                                          virtual_host=rmq_params['vhost'],
                                          credentials=creds)
connection = pika.BlockingConnection(connectparams)
print("[Checkpoint 02] Connected to vhost ", rmq_params['vhost'], 'on RMQ server at ',
      sys.argv[2], ' as user ', rmq_params['username'])
chan = connection.channel()

# checkpoint 03 create rfcomm bleutooth socket on port 1

# wait for connections?

# if connected
# checkpoint 04 accept rfcomm bluetooth connection from (address, port)
chan.basic_publish(exchange=rmq_params['exchange'],
                   routing_key=rmq_params['status_queue'],
                   body='green')
print("[Checkpoint p-01] Published message with routing_key: ", rmq_params['status_queue'])
print("[Checkpoint p-02] Message: green")
# checkpoint 05 sending exchange and queue names
# send the exchange and queue names to bluetooth device

# if received command
# checkpoint 06 received rfcomm bluetooth data: command

# if command is p
# check if queue is correct and queue is not master or status
chan.basic_publish(exchange=rmq_params['exchange'],
                   routing_key=rmq_params['status_queue'],
                   body='purple')
print("[Checkpoint p-01] Published message with routing_key: ", rmq_params['status_queue'])
print("[Checkpoint p-02] Message: purple")
# publish message
# store document in mongodb
# msgid = "26$" + time.time()
# doc = {"Action": "p", "Place": rmq_params['exchange'], "MsgID": msgid, "Subject": queue, "Message": message}

# if command is c
# check if queue is correct and queue is not master or status
chan.basic_publish(exchange=rmq_params['exchange'],
                   routing_key=rmq_params['status_queue'],
                   body='yellow')
print("[Checkpoint p-01] Published message with routing_key: ", rmq_params['status_queue'])
print("[Checkpoint p-02] Message: yellow")
# consume message from queue
# store document in mongodb
msgid = "26$" + time.time()
# doc = {"Action": "p", "Place": rmq_params['exchange'], "MsgID": msgid, "Subject": queue, "Message": message}

# if command is h
# check if queue is correct and queue is not master or status
chan.basic_publish(exchange=rmq_params['exchange'],
                   routing_key=rmq_params['status_queue'],
                   body='blue')
print("[Checkpoint p-01] Published message with routing_key: ", rmq_params['status_queue'])
print("[Checkpoint p-02] Message: blue")
# print history of commands for queue

# if disconnected
print("[Checkpoint 07] RFCOMM Bluetooth client disconnected.")
chan.basic_publish(exchange=rmq_params['exchange'],
                   routing_key=rmq_params['status_queue'],
                   body='red')
print("[Checkpoint p-01] Published message with routing_key: ", rmq_params['status_queue'])
print("[Checkpoint p-02] Message: red")