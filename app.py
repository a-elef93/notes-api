import os
from flask import Flask, request, jsonify
import redis

app = Flask(__name__)
cache = redis.Redis(
    host=os.environ.get("REDIS_HOST", "redis"),
    port=6379,
    decode_responses=True,
)

@app.route("/notes", methods=["POST"])
def add_note():
    data = request.get_json(silent=True) or {}
    text = data.get("text")
    if not text:
        return jsonify(error="text is required"), 400
    cache.rpush("notes", text)
    return jsonify(message="saved"), 201

@app.route("/notes", methods=["GET"])
def list_notes():
    return jsonify(notes=cache.lrange("notes", 0, -1))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
