import pika
import json

credenciales = pika.PlainCredentials('guest', 'guest')
parametros = pika.ConnectionParameters(host='localhost', virtual_host='/servidores_web', credentials=credenciales)
connection = pika.BlockingConnection(parametros)
channel = connection.channel()

print(' [*] Consumidor 2 (Métricas de Servidores Quito) en línea. Esperando datos...')

def callback_performance(ch, method, properties, body):
    data = json.loads(body)
    print(f" [METRICS - TOPIC] Servidor Local: {data['servidor']} -> Alerta de {data['componente']} al {data['uso']}")
    ch.basic_ack(delivery_tag=method.delivery_tag)

# Suscribirse usando el nombre EXACTO de tu cola de telemetría
channel.basic_consume(queue='quito_performance_queue', on_message_callback=callback_performance)

channel.start_consuming()