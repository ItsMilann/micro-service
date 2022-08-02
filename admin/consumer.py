import json, os, django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'admin.settings')
django.setup()

import pika
from products.models import Product
from products.producer import URI



params = pika.URLParameters(URI)
connection = pika.BlockingConnection(params)
channel = connection.channel()

channel.queue_declare(queue='admin')

def callback(ch, method, properties, body):
    id = json.loads(body)
    product = Product.objects.get(id=id)
    product.likes += 1
    product.save()
    print("Products new likes: ", product.likes)



channel.basic_consume(queue='admin', on_message_callback=callback, auto_ack=True)
print("START CONSUMING")
channel.start_consuming()
channel.close()