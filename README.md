Project: Aircraft Engine Monitoring using Fog & Edge Computing

Student: Kishore Ramesh
Student ID: X24236462

Description:
This project simulates aircraft engine sensor data, processes it at a fog node,
and sends it to AWS cloud services using MQTT. The system uses AWS IoT Core,
DynamoDB, EC2, and Elastic Beanstalk for real-time monitoring.

Features:
- 5 sensor simulation (Temperature, Vibration, RPM, Fuel Flow, Pressure)
- Fog processing (engine load, alerts)
- MQTT communication using AWS IoT Core
- Scalable cloud backend (DynamoDB)
- Real-time dashboard (Flask + Chart.js)
- EC2 auto-running service using systemd

How to Run:
1. Install Python dependencies:
   pip install -r requirements.txt

2. Run fog publisher:
   python -m fog_nodes.iot_publisher

3. Run Flask app:
   python app.py

Deployed URL:
http://fog-env.eba-9uvt5trc.us-east-1.elasticbeanstalk.com/

GitHub:
https://github.com/kishore-0501/aircraft-monitoring
