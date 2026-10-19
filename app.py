from flask import Flask, request, jsonify, render_template, redirect, url_for, flash
import os
import numpy as np
import face_recognition
from db import insert_person, find_nearest

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret')
DISTANCE_THRESHOLD = float(os.environ.get('DISTANCE_THRESHOLD', 0.6))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/enroll', methods=['POST'])
def enroll_route():
    # supports both form uploads (from UI) and API usage
    name = request.form.get('name') or request.args.get('name')
    file = request.files.get('image')
    if not name or not file:
        if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
            return jsonify({'error': 'missing name or image'}), 400
        flash('Missing name or image', 'danger')
        return redirect(url_for('index'))
    image = face_recognition.load_image_file(file)
    encs = face_recognition.face_encodings(image)
    if not encs:
        if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
            return jsonify({'error': 'no face detected'}), 400
        flash('No face detected in the uploaded image', 'warning')
        return redirect(url_for('index'))
    embedding = np.mean(encs, axis=0).tolist()
    pid = insert_person(name, embedding, metadata={'uploaded_via': 'web'})
    if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
        return jsonify({'id': pid, 'name': name})
    flash(f'Enrolled {name} (id={pid})', 'success')
    return redirect(url_for('index'))

@app.route('/recognize', methods=['POST'])
def recognize_route():
    file = request.files.get('image')
    if not file:
        if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
            return jsonify({'error': 'missing image'}), 400
        flash('Missing image', 'danger')
        return redirect(url_for('index'))
    image = face_recognition.load_image_file(file)
    encs = face_recognition.face_encodings(image)
    if not encs:
        if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
            return jsonify({'error': 'no face detected'}), 400
        flash('No face detected in the uploaded image', 'warning')
        return redirect(url_for('index'))
    enc = encs[0]
    neighbors = find_nearest(enc.tolist(), top_k=5)
    matches = []
    for _id, name, _emb, dist in neighbors:
        matches.append({'id': _id, 'name': name, 'distance': float(dist), 'match': float(dist) <= DISTANCE_THRESHOLD})
    if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
        return jsonify({'matches': matches})
    return render_template('index.html', matches=matches)

if __name__ == '__main__':
    # Development server fallback
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=(os.environ.get('FLASK_ENV') == 'development'))
