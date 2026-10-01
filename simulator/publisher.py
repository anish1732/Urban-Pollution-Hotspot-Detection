import json
import os
import random
import time
import paho.mqtt.client as mqtt

BROKER = os.getenv("MQTT_BROKER", "localhost")
PORT = int(os.getenv("MQTT_PORT", "1883"))
TOPIC = os.getenv("MQTT_TOPIC", "pollution/data")

# Simulated pollution monitoring locations
sensors = [
    {
        "sensor_id": "S1",
        "lat": 28.6139,
        "lon": 77.2090,
        "name": "Delhi",
        "severity": 1.0
    },
    {
        "sensor_id": "S2",
        "lat": 28.5355,
        "lon": 77.3910,
        "name": "Noida",
        "severity": 0.75
    },
    {
        "sensor_id": "S3",
        "lat": 28.6692,
        "lon": 77.4538,
        "name": "Ghaziabad",
        "severity": 1.15
    },
    {
        "sensor_id": "S4",
        "lat": 28.4744,
        "lon": 77.5040,
        "name": "Greater Noida",
        "severity": 0.60
    },
    {
        "sensor_id": "S5",
        "lat": 28.4089,
        "lon": 77.3178,
        "name": "Faridabad",
        "severity": 0.90
    }
]

client = mqtt.Client()
client.connect(BROKER, PORT, 60)

print("Pollution sensor simulator started...")
print("MQTT broker:", BROKER)
print("Publishing to:", TOPIC)

while True:

    for sensor in sensors:

        severity = sensor["severity"]

        pm25 = max(5, random.gauss(70 * severity, 15))
        pm10 = max(10, random.gauss(130 * severity, 25))
        no2 = max(5, random.gauss(55 * severity, 12))
        o3 = max(5, random.gauss(45 * severity, 10))
        co = max(0.1, random.gauss(1.8 * severity, 0.4))

        temperature = random.uniform(24, 34)
        humidity = random.uniform(35, 75)

        payload = {
            "sensor_id": sensor["sensor_id"],
            "location": sensor["name"],
            "lat": sensor["lat"],
            "lon": sensor["lon"],
            "pm25": round(pm25, 2),
            "pm10": round(pm10, 2),
            "no2": round(no2, 2),
            "o3": round(o3, 2),
            "co": round(co, 2),
            "temperature": round(temperature, 1),
            "humidity": round(humidity, 1)
        }

        client.publish(TOPIC, json.dumps(payload))

        print("Published:", payload)

    time.sleep(2)
