import os
from flask import Flask, request, jsonify
import pymysql

app = Flask(__name__)

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "devdb")
DB_USER = os.getenv("DB_USER", "db4dev")
DB_PASS = os.getenv("DB_PASS", "devpass")

def get_conn():
    return pymysql.connect(
        host=DB_HOST, user=DB_USER, password=DB_PASS, database=DB_NAME,
        cursorclass=pymysql.cursors.DictCursor, autocommit=True
    )

@app.get("/health")
def health():
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("SELECT 1")
        return {"ok": True}

@app.get("/users")
def list_users():
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("SELECT uid, name, age FROM USERS ORDER BY uid")
        return jsonify(cur.fetchall())

@app.post("/users")
def create_user():
    data = request.get_json(force=True)
    if not data or "name" not in data or "age" not in data:
        return {"error":"name and age required"}, 400
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("INSERT INTO USERS(name, age) VALUES (%s,%s)", (data["name"], data["age"]))
        uid = cur.lastrowid
    return {"uid": uid, "name": data["name"], "age": data["age"]}, 201

@app.get("/users/<int:uid>")
def get_user(uid):
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("SELECT uid, name, age FROM USERS WHERE uid=%s", (uid,))
        row = cur.fetchone()
        return (jsonify(row), 200) if row else ({"error":"not found"}, 404)

@app.put("/users/<int:uid>")
def update_user(uid):
    data = request.get_json(force=True) or {}
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(
            "UPDATE USERS SET name=COALESCE(%s,name), age=COALESCE(%s,age) WHERE uid=%s",
            (data.get("name"), data.get("age"), uid)
        )
        if cur.rowcount == 0:
            return {"error":"not found"}, 404
    return {"uid": uid, "name": data.get("name"), "age": data.get("age")}

@app.delete("/users/<int:uid>")
def delete_user(uid):
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("DELETE FROM USERS WHERE uid=%s", (uid,))
        if cur.rowcount == 0:
            return {"error":"not found"}, 404
    return {"deleted": uid}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
