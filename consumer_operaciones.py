import pika
import json

credenciales = pika.PlainCredentials('guest', 'guest')
parametros = pika.ConnectionParameters(host='localhost', virtual_host='/servidores_web', credentials=credenciales)
connection = pika.BlockingConnection(parametros)
channel = connection.channel()

print(' [*] Consumidor 1 (Seguridad y Auditoría) en línea. Esperando mensajes...')

def callback_seguridad(ch, method, properties, body):
    data = json.loads(body)
    print(f" [ALERT - DIRECT] Alerta Crítica en IP: {data['ip']} | Acción: {data['evento']}")
    ch.basic_ack(delivery_tag=method.delivery_tag)

def callback_auditoria(ch, method, properties, body):
    data = json.loads(body)
    print(f" [AUDIT - FANOUT] Registro guardado en historial: {data['mensaje']}")
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_consume(queue='security_critical_queue', on_message_callback=callback_seguridad)
channel.basic_consume(queue='audit_general_queue', on_message_callback=callback_auditoria)

channel.start_consuming()