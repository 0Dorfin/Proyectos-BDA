import requests
import time
import random
import sys

ORION_URL = "http://localhost:1026/v2"
HEADERS = {
    "Content-Type": "application/json",
}

SENSORES = {
    "sensor_temperatura_1": {
        "temperatura": {
            "type": "Number", 
            "rango": (18.0, 30.0)
            },
        "humedad": {
            "type": "Number",
            "rango": (30.0, 50.0)
            }
    },
    "sensor_co2_1": {
        "co2": {
            "type": "Number",
            "rango": (400, 1000)
            }
    },
    "sensor_calidad_agua_1": {
        "ph": {
            "type": "Number",
            "rango": (6.5, 8.0)
               },
        "chlorine": {
            "type": "Number",
            "rango": (0.5, 1.5)
            }
    }
}

NUM_ACTUALIZACIONES = 400

def cargar_datos():
    print(f"Cargando {NUM_ACTUALIZACIONES} actualizaciones para cada sensor")
    
    for i in range(1, NUM_ACTUALIZACIONES + 1):
        
        for sensor_id, atributos in SENSORES.items():
            peticion_payload = {}
            
            for attr_nombre, info in atributos.items():
                min_val, max_val = info["rango"]
                
                if attr_nombre == "co2":
                    nuevo_valor = random.randint(min_val, max_val)
                else:
                    nuevo_valor = round(random.uniform(min_val, max_val), 2)
                    
                peticion_payload[attr_nombre] = {
                    "value": nuevo_valor,
                    "type": info["type"]
                }
            
            url = f"{ORION_URL}/entities/{sensor_id}/attrs"
            
            try:
                response = requests.patch(url, headers=HEADERS, json=peticion_payload)

                if response.status_code != 204:
                    print(f"Error en {sensor_id}: {response.status_code} {response.text}")

            except requests.exceptions.ConnectionError as e:
                print(f"Error de conexión")
                sys.exit(1)
                
        time.sleep(0.5) 

    print("Carga de datos terminada")

if __name__ == "__main__":
    cargar_datos()
