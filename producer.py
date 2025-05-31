#installer les dependances nécessaires :
#  python -m pip install kafka-python

import json
import time
from datetime import datetime, timedelta
from kafka import KafkaProducer
import random

# Configuration du producer Kafka
producer = KafkaProducer( bootstrap_servers='kafka:9092', value_serializer=lambda v: json.dumps(v).encode('utf-8'))

# Liste des capteurs et localisations possibles
sensors = ["S123", "S124", "S125", "S126", "S127"]
locations = ["Usine Paris", "Usine New-York", "Usine Tokyo"]

# Fonction pour générer un message JSON
def generate_sensor_data(sensor_id, timestamp):
    return {
        "sensor_id": sensor_id,
        "timestamp": timestamp.strftime('%Y-%m-%dT%H:%M:%SZ'),
        "temperature": round(random.uniform(20.0, 60.0), 1),  # Température entre 20 et 60
        "humidity": round(random.uniform(50.0, 80.0), 1),    # Humidité entre 50 et 80
        "location": random.choice(locations)                 # Localisation aléatoire
    }

# Générer et envoyer des données en continu
def produce_iot_data():
    start_time = datetime(2025, 5, 30, 14, 30, 0)  # Point de départ : 2025-05-30T14:30:00Z
    interval = 5  # Intervalle en secondes entre les messages
    try:
        while True:
            for sensor in sensors:
                # Générer un message pour chaque capteur
                message = generate_sensor_data(sensor, start_time)
                # Envoyer le message au topic 'iot-topic'
                producer.send('iot-topic', value=message)
                print(f"Sent: {message}")
                # Attendre un court instant
                time.sleep(interval)
            # Incrémenter le timestamp pour le prochain lot
            start_time += timedelta(seconds=len(sensors) * interval)
    except KeyboardInterrupt:
        print("Stopping producer...")
        producer.flush()
        producer.close()

# Exécuter le producer
if __name__ == "__main__":
    produce_iot_data()