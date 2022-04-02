import json
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()


def log(method, body):
    properties = pika.BasicProperties(method)
    channel.basic_publish(exchange='', routing_key='log',
                              body=json.dumps(body).encode(), properties=properties)
    # print('x->>>>>', x)
