from flask import Flask, request, jsonify
import numpy as np
import sqlite3

app = Flask(__name__)

@app.route("/update_vector", methods=["POST"])
def update_vector():
    data = request.get_json()
    name = data.get("name")
    vector_list = data.get("vector")

    if not name or not vector_list:
        return jsonify({"status": "fail", "reason": "missing data"}), 400

    vector = np.array(vector_list, dtype=np.float32)
    conn = sqlite3.connect("facevectors.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS facevectors (
            name TEXT PRIMARY KEY,
            vector BLOB
        )
    """)
    cursor.execute("INSERT OR REPLACE INTO facevectors (name, vector) VALUES (?, ?)", (name, vector.tobytes()))
    conn.commit()
    conn.close()

    return jsonify({"status": "success", "name": name, "vector_length": len(vector_list)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
