from flask import Flask, render_template, jsonify, request
import boto3
from decimal import Decimal
import time

app = Flask(__name__)

dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
enginedata = dynamodb.Table("engine")

@app.route("/")
def dashboard():
    return render_template("dashboard.html")

@app.route("/upload", methods=["POST"])
def upload_data():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"status": "error", "message": "No JSON received"}), 400

        item = {
            "id": "latest",
            "timestamp": str(time.time()),
            "temperature": Decimal(str(data.get("temperature", 0))),
            "vibration": Decimal(str(data.get("vibration", 0))),
            "rpm": Decimal(str(data.get("rpm", 0))),
            "fuel_flow": Decimal(str(data.get("fuel_flow", 0))),
            "pressure": Decimal(str(data.get("pressure", 0))),
            "vibration_alert": data.get("vibration_alert", False),
            "engine_load": Decimal(str(data.get("engine_load", 0))),
            "failure_warning": data.get("failure_warning", False)
        }

        enginedata.put_item(Item=item)

        print("Saved to DynamoDB:", item)

        return jsonify({"status": "success", "message": "Saved to DynamoDB"}), 200

    except Exception as e:
        print("UPLOAD ERROR:", str(e))
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/api/data")
def api_data():
    try:
        response = enginedata.get_item(Key={"id": "latest"})
        item = response.get("Item")

        if not item:
            return jsonify({
                "temperature": 0,
                "vibration": 0,
                "rpm": 0,
                "fuel_flow": 0,
                "pressure": 0,
                "vibration_alert": False,
                "engine_load": 0,
                "failure_warning": False
            })

        return jsonify({
            "temperature": float(item.get("temperature", 0)),
            "vibration": float(item.get("vibration", 0)),
            "rpm": float(item.get("rpm", 0)),
            "fuel_flow": float(item.get("fuel_flow", 0)),
            "pressure": float(item.get("pressure", 0)),
            "vibration_alert": bool(item.get("vibration_alert", False)),
            "engine_load": float(item.get("engine_load", 0)),
            "failure_warning": bool(item.get("failure_warning", False))
        })

    except Exception as e:
        print("READ ERROR:", str(e))
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)