# Simulacion de Sistema de Monitoreo IoT (Smart Home/City Component)

## Descripcion del Proyecto

Este proyecto consiste en la simulacion de un sistema de monitoreo basico para un componente de una Smart City o un entorno de Smart Home. Utiliza el protocolo MQTT para la comunicacion entre dispositivos simulados (sensores de temperatura y humedad) y un controlador que reacciona a los datos recibidos (ej. "encender" un ventilador si la temperatura supera un umbral).

El objetivo principal es demostrar la capacidad de dise?ar e implementar pruebas de integracion para sistemas IoT, validando la comunicacion, la logica de control y el manejo de datos en un entorno distribuido.

## Objetivo de las Pruebas

*   **Conectividad MQTT:** Validar la capacidad de los dispositivos para conectarse al broker y enviar/recibir mensajes.
*   **Integridad de Datos:** Asegurar que los datos de los sensores se transmiten correctamente y se procesan sin corrupcion.
*   **Logica de Control:** Verificar que el controlador ejecuta la logica de negocio (ej. activacion del ventilador) de forma precisa segun los umbrales definidos.
*   **Manejo de Fallas:** Evaluar el comportamiento del sistema ante la desconexion o falla de un dispositivo sensor (aunque sea de forma basica).
*   **Rendimiento Basico:** Realizar pruebas de rendimiento para el broker MQTT bajo una carga simulada de multiples dispositivos.

## Tecnologias Utilizadas

*   **Lenguaje:** Python 3
*   **Protocolo:** MQTT (libreria `paho-mqtt` para clientes)
*   **Broker MQTT:** Mosquitto (ejecutado con Docker para facilidad)
*   **Contenedores:** Docker (para orquestar Mosquitto)
*   **Framework de Pruebas:** `pytest` (para pruebas unitarias e integracion)

## Arquitectura del Sistema

El sistema simulado sigue una arquitectura sencilla:
1.  **sensor_simulado.py:** Simula un dispositivo IoT publicando datos aleatorios (temperatura, humedad) en temas MQTT especificos (`home/sensors/temperature`, `home/sensors/humidity`).
2.  **Broker MQTT (Mosquitto):** Es el punto central para el intercambio de mensajes entre el sensor y el controlador.
3.  **controlador_logica.py:** Se suscribe a los temas de los sensores, procesa los datos y publica comandos si es necesario (ej. para un actuador simulado en `home/actuators/fan`).
4.  **Clientes de Prueba (`tests/`):** Automatizan la validacion de la comunicacion y el comportamiento de la logica.
5.  **load_test_mqtt.py:** Simula multiples sensores para generar carga en el broker.


## Instalacion y Ejecucion

Sigue estos pasos para poner en marcha y probar el proyecto:

### 1. Requisitos Previos

*   Python 3.x
*   pip (gestor de paquetes de Python)
*   Docker (para ejecutar Mosquitto)

### 2. Clonar el Repositorio

```bash
git clone https://github.com/CesarSuarez6/IoT_Automatizacion.git
cd Monitoreo_IoT