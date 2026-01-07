import paho.mqtt.client as mqtt
import time
import random
import json

# Configuración del Broker MQTT
MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC_TEMP = "home/sensors/temperature"
MQTT_TOPIC_HUMIDITY = "home/sensors/humidity"
CLIENT_ID = f"sensor_simulado_{random.randint(1000, 9999)}"

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"[{CLIENT_ID}] Conectado al broker MQTT exitosamente.")
    else:
        print(f"[{CLIENT_ID}] Fallo al conectar, código: {rc}")

def on_publish(client, userdata, mid):
    # print(f"[{CLIENT_ID}] Mensaje publicado (MID: {mid})")
    pass

def run_sensor():
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, CLIENT_ID)
    client.on_connect = on_connect
    client.on_publish = on_publish

    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.loop_start() # Inicia un hilo

    print(f"[{CLIENT_ID}] Iniciando simulación de sensor...")

    try:
        while True:
            # Generar datos aleatorios para temperatura y humedad
            temperature = round(random.uniform(15.0, 35.0), 2) # Rango de 15 a 35 grados Celsius
            humidity = round(random.uniform(40.0, 90.0), 2)    # Rango de 40 a 90 por ciento

            # Preparar mensajes JSON
            temp_payload = {"device_id": CLIENT_ID, "temperature": temperature, "timestamp": time.time()}
            humidity_payload = {"device_id": CLIENT_ID, "humidity": humidity, "timestamp": time.time()}

            # Publicar mensajes
            client.publish(MQTT_TOPIC_TEMP, json.dumps(temp_payload))
            client.publish(MQTT_TOPIC_HUMIDITY, json.dumps(humidity_payload))

            print(f"[{CLIENT_ID}] Publicando -> Temp: {temperature}°C, Hum: {humidity}%")

            time.sleep(5) # Publica cada 5 segundos

    except KeyboardInterrupt:
        print(f"[{CLIENT_ID}] Simulación de sensor terminada por el usuario.")
    finally:
        client.loop_stop() # Detiene el hilo
        client.disconnect()
        print(f"[{CLIENT_ID}] Desconectado del broker MQTT.")

if __name__ == "__main__":
    run_sensor()