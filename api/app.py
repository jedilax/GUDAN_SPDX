from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(
        host="db-dev" if "dev" in request.host else "db-test",
        user="admin",
        password="password",
        database="usersdb"
    )

@app.route("/users", methods=["GET"])
def get_users():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(users)

@app.route("/users", methods=["POST"])
def add_user():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (name, age) VALUES (%s, %s)", (data["name"], data["age"]))
    conn.commit()
    cursor.close()
    conn.close()
    return {"status": "user added"}, 201
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)