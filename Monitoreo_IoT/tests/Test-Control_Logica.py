import paho.mqtt.client as mqtt
import pytest
import time
import json
import random
from unittest.mock import MagicMock, patch

# Configuración del Broker MQTT (se pone en localhost para las pruebas)
MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC_TEMP = "home/sensors/temperature"
MQTT_TOPIC_FAN_CONTROL = "home/actuators/fan"
TEMP_THRESHOLD = 25.0 # Debe coincidir con controlador_logica.py

@pytest.fixture(scope="module")
def mqtt_test_client():
    """Fixture para un cliente MQTT de prueba que publica y suscribe."""
    client_id = f"test_client_{random.randint(1000, 9999)}"
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, client_id)
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.loop_start() # Inicia el loop en un hilo separado
    yield client
    client.loop_stop()
    client.disconnect()

@pytest.fixture(scope="function")
def fan_control_subscriber():
    """
    Fixture para un cliente que se suscribe al tema de control del ventilador
    y captura los mensajes.
    """
    client_id = f"fan_monitor_{random.randint(1000, 9999)}"
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, client_id)
    client.received_fan_commands = []

    def on_message(cl, userdata, msg):
        if msg.topic == MQTT_TOPIC_FAN_CONTROL:
            client.received_fan_commands.append(json.loads(msg.payload.decode()))

    client.on_message = on_message
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.loop_start()
    client.subscribe(MQTT_TOPIC_FAN_CONTROL)
    time.sleep(0.5) # Dar tiempo para la suscripción
    yield client
    client.loop_stop()
    client.disconnect()

def create_temp_message(temperature, device_id="sensor_test"):
    """Crea un mensaje MQTT de temperatura en formato JSON."""
    payload = {"device_id": device_id, "temperature": temperature, "timestamp": time.time()}
    return json.dumps(payload)

def test_fan_turns_on_above_threshold(mqtt_test_client, fan_control_subscriber):
    """
    Verifica que el ventilador se enciende cuando la temperatura está por encima del umbral.
    Asume que 'controlador_logica.py' está corriendo.
    """
    high_temp = TEMP_THRESHOLD + 1.0 # Una temperatura por encima del umbral
    
    # Publicar un mensaje de alta temperatura
    mqtt_test_client.publish(MQTT_TOPIC_TEMP, create_temp_message(high_temp))
    time.sleep(1.5) # Dar tiempo al controlador para procesar y publicar

    # Verificar que se recibió un comando de "ON" para el ventilador
    assert len(fan_control_subscriber.received_fan_commands) > 0, "No se recibió ningún comando del ventilador"
    last_command = fan_control_subscriber.received_fan_commands[-1]
    
    assert last_command["status"] == "ON"
    assert "reason" in last_command
    print(f"\n--- Prueba de ventilador ON Exitosa ---")
    print(f"Temperatura simulada: {high_temp}°C. Comando recibido: {last_command}")


def test_fan_turns_off_below_threshold(mqtt_test_client, fan_control_subscriber):
    """
    Verifica que el ventilador se apaga cuando la temperatura está por debajo del umbral.
    Asume que 'controlador_logica.py' está corriendo.
    """
    low_temp = TEMP_THRESHOLD - 1.0 # Una temperatura por debajo del umbral
    
    # Publicar un mensaje de baja temperatura
    mqtt_test_client.publish(MQTT_TOPIC_TEMP, create_temp_message(low_temp))
    time.sleep(1.5) # Dar tiempo al controlador para procesar y publicar

    # Verificar que se recibió un comando de "OFF" para el ventilador
    assert len(fan_control_subscriber.received_fan_commands) > 0, "No se recibió ningún comando del ventilador"
    last_command = fan_control_subscriber.received_fan_commands[-1]
    
    assert last_command["status"] == "OFF"
    assert "reason" in last_command
    print(f"\n--- Prueba de ventilador OFF Exitosa ---")
    print(f"Temperatura simulada: {low_temp}°C. Comando recibido: {last_command}")

def test_fan_status_at_threshold(mqtt_test_client, fan_control_subscriber):
    """
    Verifica el comportamiento del ventilador exactamente en el umbral.
    el 'controlador_logica.py' debe de estar corriendo.
    """
    # Probar justo en el umbral (debería estar OFF si el operador es <=)
    temp_at_threshold = TEMP_THRESHOLD
    
    mqtt_test_client.publish(MQTT_TOPIC_TEMP, create_temp_message(temp_at_threshold))
    time.sleep(1.5)
    
    assert len(fan_control_subscriber.received_fan_commands) > 0, "No se recibió ningún comando del ventilador"
    last_command = fan_control_subscriber.received_fan_commands[-1]
    
    assert last_command["status"] == "OFF"
    print(f"\n--- Prueba de ventilador en Umbral (OFF) Exitosa ---")
    print(f"Temperatura simulada: {temp_at_threshold}°C. Comando recibido: {last_command}")