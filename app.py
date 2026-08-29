from flask import Flask, jsonify, request

app = Flask(__name__)

users_db = [
    {"id": 101, "name": "Martina Plantijn", "role": "admin"},
    {"id": 102, "name": "John Doe", "role": "user"},
]


@app.route("/users", methods=["GET"])
def get_users():
    return jsonify(users_db), 200


@app.route("/users", methods=["POST"])
def create_user():
    if not request.is_json:
        return jsonify({"error": "Malformed Data!"}), 400

    data = request.get_json()
    if "name" not in data or "role" not in data:
        return jsonify({"error": "Validation Failed"}), 400

    new_id = users_db[-1]["id"] + 1 if users_db else 101
    new_user = {"id": new_id, "name": data["name"], "role": data["role"]}
    users_db.append(new_user)
    return jsonify({"message": "User created", "user": new_user}), 201


@app.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    if not request.is_json:
        return jsonify({"error": "Must be JSON"}), 400

    data = request.get_json()
    user = next((u for u in users_db if u["id"] == user_id), None)
    if not user:
        return jsonify({"error": "User Not Found"}), 404

    user["name"] = data.get("name", user["name"])
    user["role"] = data.get("role", user["role"])
    return jsonify({"message": "User updated", "user": user}), 200


@app.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    global users_db

    user = next((u for u in users_db if u["id"] == user_id), None)
    if not user:
        return jsonify({"error": "User Not Found"}), 404

    users_db = [u for u in users_db if u["id"] != user_id]
    return "", 204


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)