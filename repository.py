#!/usr/bin/env python3

from rmq_param import *
import pika

creds = pika.PlainCredentials(rmq_params['username'],
                              rmq_params['password'])
lh = 'localhost'
params = pika.ConnectionParameters(host=lh,
                                   virtual_host=rmq_params['vhost'],
                                   credentials=creds)
connection = pika.BlockingConnection(params)
print("[Checkpoint 01] Connected to vhost ", rmq_params['vhost'], 'on RMQ server at ',
      lh, ' as user ', rmq_params['username'])

chan = connection.channel()
chan.exchange_declare(exchange=rmq_params['exchange'],
                      exchange_type='direct')

chan.queue_declare(queue=rmq_params['master_queue'])
chan.queue_purge(queue=rmq_params['master_queue'])
chan.queue_unbind(queue=rmq_params['master_queue'],
                  exchange=rmq_params['exchange'])
chan.queue_bind(queue=rmq_params['master_queue'],
                exchange=rmq_params['exchange'])

chan.queue_declare(queue=rmq_params["status_queue"])
chan.queue_purge(queue=rmq_params['status_queue'])
chan.queue_unbind(queue=rmq_params['status_queue'],
                  exchange=rmq_params['exchange'])
chan.queue_bind(queue=rmq_params['status_queue'],
                exchange=rmq_params['exchange'])
chan.queue_bind(queue=rmq_params['master_queue'],
                exchange=rmq_params['exchange'],
                routing_key=rmq_params['status_queue'])

for q in rmq_params['queues']:
    chan.queue_declare(queue=q)
    chan.queue_purge(queue=q)
    chan.queue_unbind(queue=q,
                      exchange=rmq_params['exchange'])
    chan.queue_bind(queue=q,
                    exchange=rmq_params['exchange'])
    chan.queue_bind(queue=rmq_params['master_queue'],
                    exchange=rmq_params['exchange'],
                    routing_key=q)


def callback(ch, method, properties, body):
    if method.routing_key == rmq_params['status.queue']:
        print("[Checkpoint l-01] Flashing LED to", body)
    else:
        print("[Checkpoint 03] Consumed a message published with routing_key ", method.routing_key)
        print("[Checkpoint 04] Message: ", body)


chan.basic_consume(callback,
                   queue=rmq_params['master_queue'])

print("[Checkpoint 02] Consuming messages from ", rmq_params['master_queue'], "queue")
chan.start_consuming()