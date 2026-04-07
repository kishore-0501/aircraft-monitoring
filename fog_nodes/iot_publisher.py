import json
import time
import os
from awscrt import mqtt
from awsiot import mqtt_connection_builder
from sensors.sensor_sim import generate_sensor_data

ENDPOINT = "a1fwdgnq21uvs8-ats.iot.us-east-1.amazonaws.com"
CLIENT_ID = "engine-simulator-client"

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PATH_TO_CERT = os.path.join(BASE_DIR, "certs", "certificate.pem.crt")
PATH_TO_KEY = os.path.join(BASE_DIR, "certs", "private.pem.key")
PATH_TO_ROOT = os.path.join(BASE_DIR, "certs", "AmazonRootCA1.pem")

TOPIC = "engine/data"

def fog_node_process(sensor_data):
    processed = {}
    processed["id"] = f"reading-{int(time.time() * 1000)}"
    processed["timestamp"] = int(time.time() * 1000)
    processed["temperature"] = sensor_data["temperature"]
    processed["vibration"] = sensor_data["vibration"]
    processed["rpm"] = sensor_data["rpm"]
    processed["fuel_flow"] = sensor_data["fuel_flow"]
    processed["pressure"] = sensor_data["pressure"]
    processed["vibration_alert"] = sensor_data["vibration"] > 4
    processed["engine_load"] = (sensor_data["rpm"] / 15000) * 100
    processed["failure_warning"] = (
        processed["temperature"] > 850 or processed["vibration_alert"]
    )
    return processed

mqtt_connection = mqtt_connection_builder.mtls_from_path(
    endpoint=ENDPOINT,
    cert_filepath=PATH_TO_CERT,
    pri_key_filepath=PATH_TO_KEY,
    ca_filepath=PATH_TO_ROOT,
    client_id=CLIENT_ID,
    clean_session=True,
    keep_alive_secs=30,
)

print("Connecting to AWS IoT Core...")
connect_future = mqtt_connection.connect()
connect_future.result()
print("Connected!")

try:
    while True:
        sensor_data = generate_sensor_data()
        processed = fog_node_process(sensor_data)

        mqtt_connection.publish(
            topic=TOPIC,
            payload=json.dumps(processed),
            qos=mqtt.QoS.AT_LEAST_ONCE
        )

        print("Published:", processed)
        time.sleep(2)

except KeyboardInterrupt:
    print("Stopping publisher...")

finally:
    disconnect_future = mqtt_connection.disconnect()
    disconnect_future.result()
    print("Disconnected.")