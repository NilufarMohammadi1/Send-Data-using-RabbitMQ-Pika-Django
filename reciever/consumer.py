import json
import pika
from sys import path
from os import environ
import psycopg2

# path.append('../../RabbitAPI/RabbitAPI/settings.py')
# environ.setdefault('DJANGO_SETTINGS_MODULE', 'RabbitAPI.settings')
# django.setup()


connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='log')

conn = psycopg2.connect(database='Rabbit_db', user="postgres", password="postgres", host="127.0.0.1", port="5432")
cursor = conn.cursor()
print("Opened database successfully")


def recieve_log(ch, method, properties, body):
    print("Received log...")
    print(body)
    data = json.loads(body)
    print(data)

    if properties.content_type == 'log':
        print("log recived")

        postgres_insert_query = """ INSERT INTO public."UserLoginLogs" (username, password, email, user_ip, user_agent ) VALUES (%s,%s,%s,%s,%s)"""
        record_to_insert = (data['username'], data['password'], data['email'], data['user_ip'], data['user_agent'],)
        print(postgres_insert_query)
        print(record_to_insert)
        cursor.execute(postgres_insert_query, record_to_insert)
        conn.commit()


channel.basic_consume(queue='log', on_message_callback=recieve_log, auto_ack=True)
print("Started Consuming...")
channel.start_consuming()
