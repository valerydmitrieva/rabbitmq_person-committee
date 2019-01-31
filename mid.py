import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(
    host='localhost'
))

channel = connection.channel()

channel.exchange_declare(exchange='direct_mid', exchange_type='direct')

result = channel.queue_declare(exclusive=True)
queue_name = result.method.queue

binding_key = 'committee_mid_mvd'

channel.queue_bind(exchange='direct_mid',
                   queue=queue_name,
                   routing_key=binding_key)

print(' [*] Waiting for a request from the Committee')


def callback(ch, method, props, body):
    response = "{} {}".format("mid", body.decode())
    print(response)

    ch.basic_publish(exchange='',
                     routing_key='from_mid',
                     properties=pika.BasicProperties(correlation_id=
                                                     props.correlation_id,
                                                     reply_to=props.reply_to),
                     body=str(response))
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_consume(callback, queue=queue_name)

channel.start_consuming()