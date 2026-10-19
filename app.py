from flask import Flask, request, jsonify
import numpy as np
import face_recognition
from db import insert_person, find_nearest

app = Flask(__name__)
DISTANCE_THRESHOLD = 0.6


@app.route("/enroll", methods=["POST"])
def enroll_route():
    name = request.form.get("name")
    file = request.files.get("image")
    if not name or not file:
        return jsonify({"error": "missing name or image"}), 400
    image = face_recognition.load_image_file(file)
    encs = face_recognition.face_encodings(image)
    if not encs:
        return jsonify({"error": "no face detected"}), 400
    embedding = np.mean(encs, axis=0).tolist()
    pid = insert_person(name, embedding, metadata={"uploaded_via": "api"})
    return jsonify({"id": pid, "name": name})


@app.route("/recognize", methods=["POST"])
def recognize_route():
    file = request.files.get("image")
    if not file:
        return jsonify({"error": "missing image"}), 400
    image = face_recognition.load_image_file(file)
    encs = face_recognition.face_encodings(image)
    if not encs:
        return jsonify({"error": "no face detected"}), 400
    enc = encs[0]
    neighbors = find_nearest(enc.tolist(), top_k=3)
    if not neighbors:
        return jsonify({"matches": []})
    matches = []
    for _id, name, _emb, dist in neighbors:
        matches.append({"id": _id, "name": name, "distance": float(dist), "match": float(dist) <= DISTANCE_THRESHOLD})
    return jsonify({"matches": matches})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
