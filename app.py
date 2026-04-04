from flask import Flask, render_template, jsonify, request
import sqlite3

app = Flask(__name__)

DB = "engine_data.db"

def get_conn():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

# Create table if not exists
conn = get_conn()
conn.execute("""
CREATE TABLE IF NOT EXISTS engine_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    temperature REAL,
    vibration REAL,
    rpm REAL,
    fuel_flow REAL,
    pressure REAL,
    vibration_alert BOOLEAN,
    engine_load REAL,
    failure_warning BOOLEAN
)
""")
conn.commit()
conn.close()

@app.route("/")
def dashboard():
    return render_template("dashboard.html")

@app.route("/upload", methods=["POST"])
def upload_data():
    data = request.get_json()

    if not data:
        return jsonify({"status": "error", "message": "No JSON received"}), 400

    conn = get_conn()
    conn.execute("""
        INSERT INTO engine_data
        (temperature, vibration, rpm, fuel_flow, pressure, vibration_alert, engine_load, failure_warning)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data.get("temperature"),
        data.get("vibration"),
        data.get("rpm"),
        data.get("fuel_flow"),
        data.get("pressure"),
        int(bool(data.get("vibration_alert"))),
        data.get("engine_load"),
        int(bool(data.get("failure_warning")))
    ))
    conn.commit()
    conn.close()

    return jsonify({"status": "success"}), 200

@app.route("/api/data")
def api_data():
    conn = get_conn()
    row = conn.execute("""
        SELECT temperature, vibration, rpm, fuel_flow, pressure,
               vibration_alert, engine_load, failure_warning
        FROM engine_data
        ORDER BY id DESC
        LIMIT 1
    """).fetchone()
    conn.close()

    if row is None:
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

    data = dict(row)
    data["vibration_alert"] = bool(data["vibration_alert"])
    data["failure_warning"] = bool(data["failure_warning"])

    return jsonify(data)

@app.route("/api/history")
def api_history():
    conn = get_conn()
    rows = conn.execute("""
        SELECT id, temperature, vibration, rpm, fuel_flow, pressure,
               vibration_alert, engine_load, failure_warning
        FROM engine_data
        ORDER BY id DESC
        LIMIT 20
    """).fetchall()
    conn.close()

    data = [dict(row) for row in reversed(rows)]

    for item in data:
        item["vibration_alert"] = bool(item["vibration_alert"])
        item["failure_warning"] = bool(item["failure_warning"])

    return jsonify(data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)