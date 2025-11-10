from flask import Flask, request, jsonify
app = Flask(__name__)

@app.route("/api/users", methods=["GET"])
def users():
    return jsonify([{"id":1,"name":"Alice"}])

@app.route("/api/login", methods=["POST"])
def login():
    data = request.json
    if data.get("username") == "admin":
        return jsonify({"token":"dummy"})
    return jsonify({"error":"unauthorized"}), 401
