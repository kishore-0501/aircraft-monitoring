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
conn.execute('''
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
''')
conn.commit()
conn.close()

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/upload', methods=['POST'])
def upload_data():
    data = request.json
    conn = get_conn()
    conn.execute('''
        INSERT INTO engine_data 
        (temperature, vibration, rpm, fuel_flow, pressure, vibration_alert, engine_load, failure_warning)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (data["temperature"], data["vibration"], data["rpm"], data["fuel_flow"], data["pressure"],
          data["vibration_alert"], data["engine_load"], data["failure_warning"]))
    conn.commit()
    conn.close()
    return {"status": "success"}

@app.route('/api/data')
def api_data():
    conn = get_conn()
    rows = conn.execute('SELECT * FROM engine_data ORDER BY id DESC LIMIT 100').fetchall()
    conn.close()
    data = [dict(row) for row in reversed(rows)]
    return jsonify(data)

#if __name__ == "__main__":
 #   app.run(host='0.0.0.0', port=8080, debug=True)