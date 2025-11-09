import requests
import json
import sys

ORION_URL = "http://localhost:1026/v2/entities"
HEADERS = {
    "Content-Type": "application/json",
}

entidades = [
    {
        "id": "sensor_temperatura_1",
        "type": "sensor_temperatura",
        "temperatura": {
            "value": 22,
            "type": "Number",
            "metadata": {
                "unidade": {
                    "value": "°C",
                    "type": "Text"
                }
            }
        },
        "humedad": {
            "value": 40,
            "type": "Number",
            "metadata": {
                "unidad": {
                    "value": "%",
                    "type": "Text"
                }
            }
        },
        "ubicacion": {
            "value": "51.5074, -0.1278",
            "type": "geo:point"
        }
    },
    
    {
        "id": "sensor_co2_1",
        "type": "sensor_co2",
        "co2": {
            "value": 600,
            "type": "Number",
            "metadata": {
                "unidad": {
                    "value": "ppm",
                    "type": "Text"
                }
            }
        },
        "ubicacion": {
            "value": "35.6895, 139.6917",
            "type": "geo:point"
        }
    },
    
    {
        "id": "sensor_calidad_agua_1",
        "type": "sensor_calidad_agua",
        "ph": {
            "value": 7,
            "type": "Number"
        },
        "chlorine": {
            "value": 0.6,
            "type": "Number",
            "metadata": {
                "unidad": {
                    "value": "mg/L",
                    "type": "Text"
                }
            }
        },
        "ubicacion": {
            "value": "-33.8688, 151.2093",
            "type": "geo:point"
        }
    }
]

def creacion_entidades():
    entidades_creadas = 0
    entidades_fallidas = 0

    for entidad in entidades:
        id_entidad = entidad["id"]

        try:
            response = requests.post(ORION_URL, headers=HEADERS, json=entidad)

            if response.status_code == 201:
                print(f"Entidad {id_entidad} creada")
                entidades_creadas += 1
            elif response.status_code == 422:
                print(f"Entidad {id_entidad} ya existe")
                entidades_creadas += 1
            else:
                print(f"Error al crear la entidad {id_entidad}: {response.status_code} {response.text}")
                entidades_fallidas += 1

        except requests.exceptions.ConnectionError:
            print(f"Error de conexión con Orion")
            sys.exit(1)

    print(f"Entidades creadas: {entidades_creadas}")
    print(f"Entidades fallidas: {entidades_fallidas}")

if __name__ == "__main__":
    creacion_entidades()
