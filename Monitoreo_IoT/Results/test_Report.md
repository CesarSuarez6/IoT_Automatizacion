\# Informe de Resultados de Pruebas IoT



\## Fecha de Ejecución: \[07/01/2026 y 13:33]



\## Resumen General



Este informe detalla los resultados de las pruebas realizadas en el sistema de monitoreo IoT simulado, cubriendo la comunicación MQTT y la lógica de control.



\## Pruebas de Comunicación MQTT (`test\_mqtt\_comunicacion.py`)



\*   \*\*`test\_mqtt\_publish\_subscribe\_flow`:\*\*

&nbsp;   \*   \*\*Estado:\*\* Pasa / Falla

&nbsp;   \*   \*\*Descripción:\*\* Verifica que un mensaje publicado por un cliente es correctamente recibido por otro cliente a través del broker.

&nbsp;   \*   \*\*Resultados:\*\* Pasa



\*   \*\*`test\_mqtt\_multiple\_messages`:\*\*

&nbsp;   \*   \*\*Estado:\*\* Pasa / Falla

&nbsp;   \*   \*\*Descripción:\*\* Valida la correcta entrega de múltiples mensajes enviados en secuencia.

&nbsp;   \*   \*\*Resultados:\*\* Pasa



\## Pruebas de Lógica de Control (`test\_control\_logica.py`)



\*   \*\*`test\_fan\_turns\_on\_above\_threshold`:\*\*

&nbsp;   \*   \*\*Estado:\*\* Pasa / Falla

&nbsp;   \*   \*\*Descripción:\*\* Confirma que el comando para "encender" el ventilador se envía cuando la temperatura excede el umbral.

&nbsp;   \*   \*\*Resultados:\*\* Pasa



\*   \*\*`test\_fan\_turns\_off\_below\_threshold`:\*\*

&nbsp;   \*   \*\*Estado:\*\* Pasa / Falla

&nbsp;   \*   \*\*Descripción:\*\* Confirma que el comando para "apagar" el ventilador se envía cuando la temperatura cae por debajo del umbral.

&nbsp;   \*   \*\*Resultados:\*\* Pasa



\*   \*\*`test\_fan\_status\_at\_threshold`:\*\*

&nbsp;   \*   \*\*Estado:\*\* Pasa / Falla

&nbsp;   \*   \*\*Descripción:\*\* Verifica el estado del ventilador (OFF) cuando la temperatura es exactamente igual al umbral.

&nbsp;   \*   \*\*Resultados:\*\* Pasa



\## Observaciones Adicionales



El resultado final resulta satisfactorio



---

