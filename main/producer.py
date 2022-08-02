import json
import pika


URI = "amqps://qscnqhyo:iF8ZqaUXGydARjYQAvjT36mf7ke1wpNG@mustang.rmq.cloudamqp.com/qscnqhyo"
params = pika.URLParameters(URI)
connection = pika.BlockingConnection(params)
channel = connection.channel()


def publish(method, body):
    properties = pika.BasicProperties(method)
    body = json.dumps(body)
    channel.basic_publish(exchange="", routing_key="admin", body=body, properties=properties)
