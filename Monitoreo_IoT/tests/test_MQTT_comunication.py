import paho.mqtt.client as mqtt
import pytest
import time
import json
import random

# Configuración del Broker MQTT (se corre localhost para pruebas)
MQTT_BROKER = "localhost"
MQTT_PORT = 1883
TEST_TOPIC = "test/topic/integration"

@pytest.fixture(scope="module")
def mqtt_client_publisher():
    """Fixture para un cliente MQTT que publica mensajes."""
    client_id = f"test_publisher_{random.randint(1000, 9999)}"
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, client_id)
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.loop_start() # Inicia el loop en un hilo separado
    yield client
    client.loop_stop()
    client.disconnect()

@pytest.fixture(scope="module")
def mqtt_client_subscriber():
    """Fixture para un cliente MQTT que se suscribe a mensajes."""
    client_id = f"test_subscriber_{random.randint(1000, 9999)}"
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, client_id)
    client.received_messages = [] # Lista para almacenar mensajes recibidos

    def on_message(cl, userdata, msg):
        cl.received_messages.append({"topic": msg.topic, "payload": msg.payload.decode()})

    client.on_message = on_message
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.loop_start() # Inicia el loop en un hilo separado
    yield client
    client.loop_stop()
    client.disconnect()

def test_mqtt_publish_subscribe_flow(mqtt_client_publisher, mqtt_client_subscriber):
    """
    Verifica que un mensaje publicado por un cliente es recibido por otro cliente
    a través del broker MQTT.
    """
    message_payload = {"test_data": "Hola MQTT desde Pytest", "value": 123}
    json_message = json.dumps(message_payload)

    # Suscribir el cliente receptor al tema de prueba
    mqtt_client_subscriber.subscribe(TEST_TOPIC)
    time.sleep(0.5) # Dar tiempo para que la suscripción se establezca

    # Publicar el mensaje
    mqtt_client_publisher.publish(TEST_TOPIC, json_message)
    time.sleep(1) # Dar tiempo para que el mensaje se propague y sea recibido

    # Verificar que el mensaje fue recibido
    assert len(mqtt_client_subscriber.received_messages) > 0, "No se recibió ningún mensaje"
    received = mqtt_client_subscriber.received_messages[0]

    assert received["topic"] == TEST_TOPIC
    assert received["payload"] == json_message

    print(f"\n--- Prueba de MQTT Exitosa ---")
    print(f"Mensaje Enviado: {json_message}")
    print(f"Mensaje Recibido: {received['payload']} en el tema {received['topic']}")

def test_mqtt_multiple_messages(mqtt_client_publisher, mqtt_client_subscriber):
    """
    Verifica que se pueden enviar y recibir múltiples mensajes.
    """
    mqtt_client_subscriber.received_messages = [] # Limpiar mensajes previos
    mqtt_client_subscriber.subscribe(TEST_TOPIC)
    time.sleep(0.5)

    messages_to_send = [
        {"id": 1, "data": "First message"},
        {"id": 2, "data": "Second message"},
        {"id": 3, "data": "Third message"}
    ]

    for msg in messages_to_send:
        mqtt_client_publisher.publish(TEST_TOPIC, json.dumps(msg))
        time.sleep(0.2) # Pequeño delay entre publicaciones

    time.sleep(1) # Dar tiempo para que todos los mensajes se reciban

    assert len(mqtt_client_subscriber.received_messages) == len(messages_to_send), "No se recibieron todos los mensajes esperados"

    received_data = [json.loads(m["payload"]) for m in mqtt_client_subscriber.received_messages]
    for msg in messages_to_send:
        assert msg in received_data, f"Mensaje {msg} no encontrado en los recibidos"

    print(f"\n--- Prueba de Múltiples Mensajes MQTT Exitosa ---")
    print(f"Mensajes Enviados: {messages_to_send}")
    print(f"Mensajes Recibidos: {received_data}")