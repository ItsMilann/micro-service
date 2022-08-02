import json
import pika
from main import db, Product
URI = "amqps://qscnqhyo:iF8ZqaUXGydARjYQAvjT36mf7ke1wpNG@mustang.rmq.cloudamqp.com/qscnqhyo"
params = pika.URLParameters(URI)
connection = pika.BlockingConnection(params)
channel = connection.channel()

channel.queue_declare(queue='flask')

def callback(ch, method, properties, body):
    data = json.loads(body)
    print("Received in flask app.", data)

    if properties.content_type == 'product_created':
        product = Product(id=data['id'], title=data['title'], image=data['image'])
        db.session.add(product)
        db.session.commit()
        
    if properties.content_type == 'product_updated':
        product = Product.query.get(data['id'])
        product.title=data['title']
        product.image=data['image']
        db.session.commit()
        
    if properties.content_type == 'product_deleted':
        product = Product.query.get(data)
        db.session.delete(product)
        db.session.commit()


channel.basic_consume(queue='flask', on_message_callback=callback, auto_ack=True)
print("START CONSUMING")
channel.start_consuming()
channel.close()