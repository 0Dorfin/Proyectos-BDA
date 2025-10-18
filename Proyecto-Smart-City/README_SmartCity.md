# SMART CITY

**Objetivo:**  Simular una ciudad inteligente. Capturaremos datos de sensores de temperatura, CO2 y calidad del agua, los procesaremos en tiempo real y crearemos un panel de control para monitorizar la "salud" de la ciudad.

## Tareas

### Tarea 1. Creacion de entidades

``` json
{
    "sensores": [
        {
            "id": "Sensor de temperatura - 1",
            "tipo": "sensor_temperatura",
            "atributos": {
                "temperatura": {
                    "valor": 22,
                    "unidade": "°C"
                },
                "humedad": {
                    "valor": 40,
                    "unidad": "%"
                },
                "ubicacion": {
                    "latitud": 51.5074,
                    "longitud": -0.1278
                }
            }
        },
            {
            "id": "Sensor de co2 - 1",
            "tipo": "sensor_co2",
            "atributos": {
                "co2": {
                    "valor": 600,
                    "unidad": "ppm"
                },
                "ubicacion": {
                    "latitud": 35.6895,
                    "longitud": 139.6917
                }
            }
            },
            {
            "id": "Sensor de calidad de agua - 1",
            "tipo": "sensor_calidad_agua",
            "atributos": {
                "ph": {
                    "valor": 7
                },
                "chlorine": {
                    "valor": 0.6,
                    "unidad": "mg/L"
                },
                "ubicacion": {
                    "latitud": -33.8688,
                    "longitud": 151.2093
                }
            }
        }
    ]
}
```
