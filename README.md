# 🖥️ ServidorWeb — Sistema de Mensajería con RabbitMQ

> **Proyecto académico** que implementa un sistema de mensajería distribuida utilizando **RabbitMQ** y **Python** para simular la gestión de eventos de seguridad, auditoría y métricas de rendimiento de servidores web.

## 📌 Descripción del Proyecto

**ServidorWeb** es un sistema de mensajería asíncrona que simula la infraestructura de monitoreo y seguridad de servidores web. El proyecto demuestra cómo implementar los **tres patrones de intercambio (exchange)** de RabbitMQ:

| Patrón | Exchange | Propósito |
|--------|----------|-----------|
| 🎯 **Direct** | `sec_direct_exchange` | Alertas de seguridad críticas (Inyección SQL, etc.) |
| 📢 **Fanout** | `audit_fanout_exchange` | Difusión de eventos de auditoría a todos los consumidores |
| 🔍 **Topic** | `performance_topic_exchange` | Métricas de rendimiento filtradas por servidor (Quito) |

Todo el tráfico fluye a través del **Virtual Host** `/servidores_web` en RabbitMQ.

---

## 🗂️ Estructura del Proyecto

```
ServidorWeb/
│
├── producer.py                # Productor: genera y envía todos los eventos
├── consumer_operaciones.py    # Consumidor 1: Seguridad y Auditoría
└── consumer_performance.py    # Consumidor 2: Métricas de Rendimiento (Quito)
```

---

## 📁 Descripción de Archivos

### `producer.py` — El Productor 🚀

Se encarga de:

1. **Conectarse** al Virtual Host `/servidores_web` en RabbitMQ (puerto `5672`, usuario `guest`).
2. **Enviar eventos por Direct Exchange** (`sec_direct_exchange`):
   - Routing key: `security.critical`
   - Payload ejemplo: `{"evento": "Intento de Inyección SQL", "ip": "192.168.1.50", "estado": "BLOQUEADO"}`
3. **Enviar eventos por Fanout Exchange** (`audit_fanout_exchange`):
   - Difunde mensajes de auditoría a **todas** las colas enlazadas.
4. **Enviar eventos por Topic Exchange** (`performance_topic_exchange`):
   - Routing key con patrón: `servers.quito.*`
   - Payload ejemplo con datos de CPU/Memoria de servidores en Quito.


### `consumer_operaciones.py` — Consumidor de Seguridad y Auditoría 🛡️

Este script es el **Consumidor 1**. Escucha dos colas simultáneamente:

| Cola | Exchange | Tipo de Mensaje |
|------|----------|-----------------|
| `security_critical_queue` | `sec_direct_exchange` | Alertas de seguridad críticas |
| `audit_general_queue` | `audit_fanout_exchange` | Registros generales de auditoría |


### `consumer_performance.py` — Consumidor de Métricas 📊

Este script es el **Consumidor 2**. Monitorea métricas de rendimiento de los servidores de la ciudad de **Quito**.

| Cola | Exchange | Filtro |
|------|----------|--------|
| `quito_performance_queue` | `performance_topic_exchange` | Topic: `servers.quito.*` |


## 🏗️ Arquitectura del Sistema

```
                          ┌─────────────────────────────────┐
                          │        RabbitMQ Broker           │
                          │   Virtual Host: /servidores_web  │
                          │                                  │
  ┌─────────────┐         │  ┌──────────────────────────┐   │
  │             │──DIRECT─►  │   sec_direct_exchange     │──► security_critical_queue ──┐
  │             │         │  └──────────────────────────┘   │                           │
  │ producer.py │         │                                  │                           ▼
  │             │─FANOUT──►  ┌──────────────────────────┐   │              ┌─────────────────────────┐
  │             │         │  │  audit_fanout_exchange    │──► audit_general_queue     │ consumer_     │
  │             │         │  └──────────────────────────┘   │              │ operaciones.py          │
  │             │─TOPIC───►  ┌──────────────────────────┐   │              └─────────────────────────┘
  └─────────────┘         │  │ performance_topic_exchange│──► quito_performance_queue──►consumer_     │
                          │  └──────────────────────────┘   │                           performance.py│
                          └─────────────────────────────────┘

## ▶️ Cómo Ejecutar el Proyecto

> ⚠️ **Importante**: RabbitMQ debe estar corriendo antes de ejecutar cualquier script.

### Terminal 1 — Iniciar Consumidor de Operaciones (Seguridad y Auditoría)

```bash
python consumer_operaciones.py
```

### Terminal 2 — Iniciar Consumidor de Performance (Métricas)

```bash
python consumer_performance.py
```

### Terminal 3 — Ejecutar el Productor (envía todos los eventos)

```bash
python producer.py
```


## 🔄 Flujo Completo de Mensajes

```
producer.py
    │
    ├──[DIRECT]──► sec_direct_exchange ──► security_critical_queue ──► consumer_operaciones.py
    │                (routing_key)                     └── callback_seguridad()
    │
    ├──[FANOUT]──► audit_fanout_exchange ──► audit_general_queue ──► consumer_operaciones.py
    │               (sin routing key)                                   └── callback_auditoria()
    │
    └──[TOPIC]──► performance_topic_exchange ──► quito_performance_queue ──► consumer_performance.py
                   (routing_key)                              └── callback_performance()


