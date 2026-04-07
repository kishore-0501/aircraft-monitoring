import requests
import time
from sensors.sensor_sim import generate_sensor_data

CLOUD_ENDPOINT = "http://fog-env.eba-9uvt5trc.us-east-1.elasticbeanstalk.com/upload"

def fog_node_process(sensor_data):
    processed = {}
    processed["temperature"] = sensor_data["temperature"]
    processed["vibration"] = sensor_data["vibration"]
    processed["rpm"] = sensor_data["rpm"]
    processed["fuel_flow"] = sensor_data["fuel_flow"]
    processed["pressure"] = sensor_data["pressure"]

    processed["vibration_alert"] = sensor_data["vibration"] > 4
    processed["engine_load"] = (sensor_data["rpm"] / 15000) * 100
    processed["failure_warning"] = processed["temperature"] > 850 or processed["vibration_alert"]

    return processed

def main():
    while True:
        sensor_data = generate_sensor_data()
        processed = fog_node_process(sensor_data)

        try:
            response = requests.post(
                CLOUD_ENDPOINT,
                json=processed,
                headers={"Content-Type": "application/json"},
                timeout=10
            )

            print("Status code:", response.status_code)
            print("Response body:", response.text)
            print("Payload sent:", processed)
            print("-" * 60)

        except Exception as e:
            print("Error sending data:", e)

        time.sleep(2)

if __name__ == "__main__":
    main()