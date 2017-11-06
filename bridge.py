#!/usr/bin/env python3

import bluetooth
import os
from rmq_param import *
import pika
import sys
import time
import pymongo

def msgConsume(ch, method, properties, body):
    print("[Checkpoint c-01] Consumed a message published with rouying key: ", method.routing_key)
    print("[Checkpoint c-02] Message: ", body)
    print("[Checkpoint c-03] Sending to RFCOMM bluetooth client")
    client.send(body)
          
          
RMQserv = '192.168.1.19'
MDBport = 27017
RMQport = 5672
btMAC = 'F8:CF:C5:D1:4F:3E' #MAC Address of Jacob's cellular device with bluetooth capability
port = 1
backlog = 1
size = 1024




if len(sys.argv) > 1:
    if (sys.argv[1] == '-s'):   RMQserv = sys.argv[2]
    
mongodb = pymongo.MongoClient()[rmq_params['exchange']]
for q in rmq_params['queues']:
    col = mongodb[q]
    #col.drop()

print("[Checkpoint 01] Connected to database ", rmq_params['exchange'], " on MongoDB server localhost")

creds = pika.PlainCredentials(rmq_params['username'],
                              rmq_params['password'])
connectparams = pika.ConnectionParameters(host=RMQServ,
    virtual_host=rmq_params['vhost'],
    credentials=creds)
connection = pika.BlockingConnection(connectparams)
print("[Checkpoint 02] Connected to vhost ", rmq_params['vhost'], 'on RMQ server at ',
    sys.argv[2], ' as user ', rmq_params['username'])
chan = connection.channel()

# checkpoint 03 create rfcomm bleutooth socket on port 1
s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
s.bind(("", port))
print('[Checkpoint 03] Created RFCOMM Bluetooth socket on port ', port)
s.listen(backlog)
try:
    client, address = s.accept()
    print('[Checkpoint 04] Accepted RFCOMM bluetooth connection from ', address)


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
    client.send("Communicating on exchange: ", rmq_params['exchange'])
    client.send("Available queues:")
    for n in rmq_params['queues']:
        client.send(n)

    # if received command
    # checkpoint 06 received rfcomm bluetooth data: command
    while 1:
        data = client.recv(size)
        print("[Checkpoint 06] ", data)
        command = data[2]
        data[3] = ' '
        backSlash = data.find('\\')
        data[backSlash] = ' '
        dataList = data.split(' ')
        q = dataList[1]
        msg = dataList[2]

        # if command is p
        # check if queue is correct and queue is not master or status
        if (command == 'p'):
            command == ' '
            if (q != "master_queue" and q != "status_queue"):

                chan.basic_publish(exchange=rmq_params['exchange'],
                    routing_key=rmq_params['status_queue'],
                    body='purple')
                print("[Checkpoint p-01] Published message with routing_key: ", rmq_params['status_queue'])
                print("[Checkpoint p-02] Message: purple")
                chan.basic_publish(exchange=rmq_params['exchange'],
                    routing_key=q,
                    body=msg)
                print("[Checkpoint p-01] Published message with routing_key: ", q)
                print("[Checkpoint p-02] Message: ", msg)

                # publish message
                # store document in mongodb
                msgid = "26$" + time.time()
                doc = {"Action": "p", "Place": rmq_params['exchange'], "MsgID": msgid, "Subject": q, "Message": msg}
                col=mongodb[q]
                col.insert(doc)

        if (command == 'c'):
            command == ' '
            if (q != "master_queue" and q != "status_queue"):

                # if command is c
                # check if queue is correct and queue is not master or status
                chan.basic_publish(exchange=rmq_params['exchange'],
                    routing_key=rmq_params['status_queue'],
                    body='yellow')
                print("[Checkpoint p-01] Published message with routing_key: ", rmq_params['status_queue'])
                print("[Checkpoint p-02] Message: yellow")
                chan.basic_consume(msgConsume, queue = q)

                # consume message from queue
                # store document in mongodb
                msgid = "26$" + time.time()
                # doc = {"Action": "p", "Place": rmq_params['exchange'], "MsgID": msgid, "Subject": queue, "Message": message}

                msgid = "26$" + time.time()
                doc = {"Action": "c", "Place": rmq_params['exchange'], "MsgID": msgid, "Subject": q, "Message": ''}
                col=mongodb[q]
                col.insert(doc)

        if (command == 'h'):
            command == ' '
            if (q != "master_queue" and q != "status_queue"):
                print("[Checkpoint h-01] Printing history of Collection '", q ,"' in MongoDB database '", rmq_params['exchange'], "'")
                print("[Checkpoint h-02] Collection: ", q)
                collection = mongodb[q]
                cur = collection.find({})
                for document in cur:
                    print(document)
                # if command is h
                # check if queue is correct and queue is not master or status
                chan.basic_publish(exchange=rmq_params['exchange'],
                                   routing_key=rmq_params['status_queue'],
                                   body='blue')
                print("[Checkpoint p-01] Published message with routing_key: ", rmq_params['status_queue'])
                print("[Checkpoint p-02] Message: blue")
                # print history of commands for queue

    # if disconnected
except:
    print("Error occured, closing Socket")
    client.close()
    s.close()
    print("[Checkpoint 07] RFCOMM Bluetooth client disconnected.")
    chan.basic_publish(exchange=rmq_params['exchange'],
                       routing_key=rmq_params['status_queue'],
                       body='red')
    print("[Checkpoint p-01] Published message with routing_key: ", rmq_params['status_queue'])
    print("[Checkpoint p-02] Message: red")

                          
                          
                         
