import pika
import json

# 1. Parámetros de conexión explícitos para el Virtual Host /servidores_web
credenciales = pika.PlainCredentials('guest', 'guest')
parametros = pika.ConnectionParameters(
    host='localhost',
    port=5672,
    virtual_host='/servidores_web',  # <--- Tu VHost real
    credentials=credenciales
)

connection = pika.BlockingConnection(parametros)
channel = connection.channel()

print(" [x] Conectado al Virtual Host '/servidores_web'. Enviando eventos...")

# --- 1. ENVÍO DIRECT (Seguridad Crítica) ---
payload_seguridad = {"evento": "Intento de Inyección SQL", "ip": "192.168.1.50", "estado": "BLOQUEADO"}
channel.basic_publish(
    exchange='sec_direct_exchange',
    routing_key='security.critical',  # clave
    body=json.dumps(payload_seguridad)
)
print(" [✓] Mensaje Direct enviado a 'sec_direct_exchange'")

# --- 2. ENVÍO FANOUT (Auditoría General) ---
payload_auditoria = {"modulo": "Autenticación", "mensaje": "Usuario administrador inició sesión"}
channel.basic_publish(
    exchange='audit_fanout_exchange',
    routing_key='',  # no hay clave
    body=json.dumps(payload_auditoria)
)
print(" [✓] Mensaje Fanout enviado a 'audit_fanout_exchange'")

# --- 3. ENVÍO TOPIC (Rendimiento de Servidores) ---
payload_metricas = {"servidor": "UIO-WEB-01", "componente": "CPU", "uso": "89%"}
channel.basic_publish(
    exchange='perf_topic_exchange',
    routing_key='quito.nodo01.cpu',  # clave
    body=json.dumps(payload_metricas)
)
print(" [✓] Mensaje Topic enviado a 'perf_topic_exchange'")

connection.close()