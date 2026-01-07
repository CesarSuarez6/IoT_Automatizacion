import paho.mqtt.client as mqtt
import time
import random
import json
import threading

# Configuración del Broker MQTT
MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_BASE_TOPIC = "home/load_test/sensor/" # Cada sensor tendrá un topic único
NUM_SENSORS = 50 # Número de sensores a simular
MESSAGE_INTERVAL_SEC = 1 # Intervalo de publicación por sensor
DURATION_SEC = 30 # Duración total de la prueba de carga

def sensor_client_thread(sensor_id):
    client_id = f"load_sensor_{sensor_id}_{random.randint(1000, 9999)}"
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, client_id)
    
    # client.on_connect = lambda client, userdata, flags, rc: print(f"[{client_id}] Connected with result code {rc}")
    # client.on_disconnect = lambda client, userdata, rc: print(f"[{client_id}] Disconnected with result code {rc}")

    try:
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
        client.loop_start()

        topic = f"{MQTT_BASE_TOPIC}{sensor_id}/temperature"
        start_time = time.time()
        
        while time.time() - start_time < DURATION_SEC:
            temperature = round(random.uniform(20.0, 30.0), 2)
            payload = {"device_id": client_id, "temperature": temperature, "timestamp": time.time()}
            client.publish(topic, json.dumps(payload))
            # print(f"[{client_id}] Publicado: {temperature}°C a {topic}")
            time.sleep(MESSAGE_INTERVAL_SEC)
            
    except Exception as e:
        print(f"[{client_id}] Error: {e}")
    finally:
        if client.is_connected():
            client.loop_stop()
            client.disconnect()
        # print(f"[{client_id}] Desconectado.")

def run_load_test():
    print(f"Iniciando prueba de carga con {NUM_SENSORS} sensores durante {DURATION_SEC} segundos...")
    print("Asegúrate de que el broker Mosquitto esté corriendo en localhost:1883.")

    threads = []
    for i in range(NUM_SENSORS):
        thread = threading.Thread(target=sensor_client_thread, args=(i,))
        threads.append(thread)
        thread.start()
        
        time.sleep(0.05) 

    for thread in threads:
        thread.join()

    print(f"\nPrueba de carga finalizada. {NUM_SENSORS} sensores simularon enviar datos cada {MESSAGE_INTERVAL_SEC} segundo(s) por {DURATION_SEC} segundo(s).")
    print("Revisa los logs del broker Mosquitto para más detalles sobre la carga manejada.")


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        try:
            NUM_SENSORS = int(sys.argv[1])
            if len(sys.argv) > 2:
                DURATION_SEC = int(sys.argv[2])
        except ValueError:
            print("Uso: python load_test_mqtt.py [num_sensores] [duracion_seg]")
            sys.exit(1)
    
    run_load_test()