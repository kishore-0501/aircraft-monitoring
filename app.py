from flask import Flask, render_template, jsonify
import boto3

app = Flask(__name__)

dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
enginedata = dynamodb.Table("engine")

@app.route("/")
def dashboard():
    return render_template("dashboard.html")

@app.route("/api/data")
def api_data():
    try:
        response = enginedata.scan()
        items = response.get("Items", [])

        if not items:
            return jsonify({
                "temperature": 0,
                "vibration": 0,
                "rpm": 0,
                "fuel_flow": 0,
                "pressure": 0,
                "vibration_alert": False,
                "engine_load": 0,
                "failure_warning": False,
                "timestamp": 0
            })

        latest_item = sorted(
            items,
            key=lambda x: float(x.get("timestamp", 0)),
            reverse=True
        )[0]

        return jsonify({
            "temperature": float(latest_item.get("temperature", 0)),
            "vibration": float(latest_item.get("vibration", 0)),
            "rpm": float(latest_item.get("rpm", 0)),
            "fuel_flow": float(latest_item.get("fuel_flow", 0)),
            "pressure": float(latest_item.get("pressure", 0)),
            "vibration_alert": bool(latest_item.get("vibration_alert", False)),
            "engine_load": float(latest_item.get("engine_load", 0)),
            "failure_warning": bool(latest_item.get("failure_warning", False)),
            "timestamp": float(latest_item.get("timestamp", 0))
        })

    except Exception as e:
        print("READ ERROR:", str(e))
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)