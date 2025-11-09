# Proyecto Smart City: Tarea 2 FIWARE

1\. Iniciar el Docker
----------------------------------------

Primero, levantamos todos los servicios (Orion, MongoDB, CrateDB, QuantumLeap y Grafana) definidos en el archivo docker-compose.yml.

```bash
docker compose up -d
```

Comprobamos que todos los contenedores estén corriendo:

<img width="2343" height="1010" alt="docker1" src="https://github.com/user-attachments/assets/40cefde3-ef5f-4e67-adb9-5a965f7e2a0b" />

2\. Creación de Entidades
------------------------------------------------------

Ejecutamos el primer script para crear nuestros 3 sensores.

```bash
python crear_entidades.py
```

Accedemos a la base de datos de MongoDB para ver las entidades recién creadas.

<img width="2772" height="1265" alt="image" src="https://github.com/user-attachments/assets/9ddc1588-3a93-4dd3-bd3d-29b98d7190c0" />

Comprobamos que tienen los datos correctos con:

```bash
db["entities"].find()
```

<img width="1415" height="1702" alt="image" src="https://github.com/user-attachments/assets/1850af0c-1feb-4736-8007-9f5c986f70d4" />

    
3\. Creación de la Suscripción
-----------------------------------------------------------

Ejecutamos el script que le dice a Orion que notifique a QuantumLeap cada vez que los datos de nuestros sensores cambien.

```bash
python crear_suscripcion.py
```
Volvemos a MongoDB para comprobar que la suscripción se ha creado.

<img width="2773" height="1059" alt="image" src="https://github.com/user-attachments/assets/42cb25df-59f7-461c-a187-2259952626c0" />

4\. Carga de 400 Actualizaciones
-----------------------------------------

Ejecutamos el script que enviará 400 actualizaciones para cada sensor.

```bash
python carga_datos.py
```

Este script nos hace dos cosas:

1.  **MongoDB** se actualiza 400 veces pero solo guarda el último valor.
2.  **CrateDB** recibe 400 copias gracias a la suscripción.
    

5\. Verificación de MongoDB y CrateDB
--------------------------------------------

Tras la carga de datos, verificamos ambos puntos.

### 5a. Histórico Completo de CrateDB

Volvemos a la consola de CrateDB ([**http://localhost:4200/**](https://www.google.com/search?q=http://localhost:4200/)) y veremos las 1200 actualizaciones y sus respectivas tablas:

<img width="2782" height="1154" alt="crate1" src="https://github.com/user-attachments/assets/5d966bc5-5e54-4c0e-bc3b-0dd4f70f95a5" />

<img width="2783" height="919" alt="crate2" src="https://github.com/user-attachments/assets/636db85b-eae2-46d9-98dc-2c53b19dace8" />


Si hacemos la siguiente consulta:

```bash
SELECT COUNT(*) FROM etsensor_temperatura;
```

<img width="2776" height="925" alt="image" src="https://github.com/user-attachments/assets/44298851-39c1-4841-a86e-a32c7ebf9ee3" />

Esta devuelve **400**. Esto demuestra que el historial de 400 actualizaciones para el sensor fue recibido y almacenado con éxito.

### 5b. Estado Final de MongoDB

Volvemos a MongoDB para comprobar el **estado final**. Ejecutamos de nuevo el find().

**Resultado:** Vemos las mismas 3 entidades, pero sus atributos ahora tienen los **últimos valores aleatorios** que generó el script.

<img width="1802" height="1708" alt="image" src="https://github.com/user-attachments/assets/9dc4642d-a6f8-405c-a9f3-706256c2ff8b" />
