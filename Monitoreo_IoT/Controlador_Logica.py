import paho.mqtt.client as mqtt
import time
import json
import random

# Configuración del Broker MQTT
MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC_TEMP = "home/sensors/temperature"
MQTT_TOPIC_HUMIDITY = "home/sensors/humidity"
MQTT_TOPIC_FAN_CONTROL = "home/actuators/fan"
CLIENT_ID = f"controlador_logica_{random.randint(1000, 9999)}"

# Umbral de temperatura para activar el ventilador
TEMP_THRESHOLD = 25.0 # Grados Celsius

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"[{CLIENT_ID}] Conectado al broker MQTT exitosamente.")
        # Suscribirse a los temas de los sensores
        client.subscribe(MQTT_TOPIC_TEMP)
        print(f"[{CLIENT_ID}] Suscrito a {MQTT_TOPIC_TEMP}")
        client.subscribe(MQTT_TOPIC_HUMIDITY)
        print(f"[{CLIENT_ID}] Suscrito a {MQTT_TOPIC_HUMIDITY}")
    else:
        print(f"[{CLIENT_ID}] Fallo al conectar, código: {rc}")

def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode())
        topic = msg.topic
        
        # Procesar mensaje de temperatura
        if topic == MQTT_TOPIC_TEMP:
            temperature = payload.get("temperature")
            device_id = payload.get("device_id", "Unknown")
            if temperature is not None:
                print(f"[{CLIENT_ID}] Datos recibidos de {device_id} - Temperatura: {temperature}°C")
                
                # Lógica de control del ventilador
                if temperature > TEMP_THRESHOLD:
                    fan_status = "ON"
                    print(f"[{CLIENT_ID}] Temperatura ({temperature}°C) > Umbral ({TEMP_THRESHOLD}°C). Enviando comando: VENTILADOR {fan_status}")
                    client.publish(MQTT_TOPIC_FAN_CONTROL, json.dumps({"status": fan_status, "reason": "high_temp"}))
                else:
                    fan_status = "OFF"
                    print(f"[{CLIENT_ID}] Temperatura ({temperature}°C) <= Umbral ({TEMP_THRESHOLD}°C). Enviando comando: VENTILADOR {fan_status}")
                    client.publish(MQTT_TOPIC_FAN_CONTROL, json.dumps({"status": fan_status, "reason": "normal_temp"}))

        # Procesar mensaje de humedad (en este ejemplo, solo se imprime)
        elif topic == MQTT_TOPIC_HUMIDITY:
            humidity = payload.get("humidity")
            device_id = payload.get("device_id", "Unknown")
            if humidity is not None:
                print(f"[{CLIENT_ID}] Datos recibidos de {device_id} - Humedad: {humidity}%")
        
    except json.JSONDecodeError:
        print(f"[{CLIENT_ID}] Error al decodificar JSON del mensaje en el tema {msg.topic}: {msg.payload}")
    except Exception as e:
        print(f"[{CLIENT_ID}] Error inesperado al procesar mensaje: {e}")

def run_controller():
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, CLIENT_ID)
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.loop_forever() # Bloquea y procesa los mensajes entrantes

if __name__ == "__main__":
    run_controller()