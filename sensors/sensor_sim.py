import random

def generate_sensor_data():
    return {
        "temperature": random.randint(500, 900),
        "vibration": round(random.uniform(0, 5), 2),
        "rpm": random.randint(5000, 15000),
        "fuel_flow": round(random.uniform(200, 800), 2),
        "pressure": round(random.uniform(20, 50), 2)
    }