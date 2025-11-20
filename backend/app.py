from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import joblib
import numpy as np
import sqlite3
from datetime import datetime
import os

app = Flask(__name__, static_folder='../frontend', static_url_path='')
CORS(app)

# Load the trained model
model = None
try:
    model = joblib.load('student_performance_model.pkl')
    print("Model loaded successfully")
except FileNotFoundError:
    print("Model not found. Please run train_model.py first")

# Initialize SQLite database
def init_db():
    conn = sqlite3.connect('predictions.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            attendance REAL,
            study_hours REAL,
            internal_marks REAL,
            assignments_submitted INTEGER,
            activities INTEGER,
            prediction TEXT,
            confidence REAL,
            timestamp DATETIME
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    return send_from_directory('../frontend', 'index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        if model is None:
            return jsonify({'error': 'Model not loaded'}), 500
        
        data = request.json
        
        # Extract features
        features = [
            float(data['attendance']),
            float(data['study_hours']),
            float(data['internal_marks']),
            int(data['assignments_submitted']),
            int(data['activities'])
        ]
        
        # Make prediction
        prediction = model.predict([features])[0]
        confidence = max(model.predict_proba([features])[0])
        
        # Store in database
        conn = sqlite3.connect('predictions.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO predictions 
            (attendance, study_hours, internal_marks, assignments_submitted, activities, prediction, confidence, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (*features, prediction, confidence, datetime.now()))
        conn.commit()
        conn.close()
        
        return jsonify({
            'prediction': prediction,
            'confidence': round(confidence * 100, 2)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/history', methods=['GET'])
def get_history():
    try:
        conn = sqlite3.connect('predictions.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM predictions ORDER BY timestamp DESC LIMIT 10')
        rows = cursor.fetchall()
        conn.close()
        
        history = []
        for row in rows:
            history.append({
                'id': row[0],
                'attendance': row[1],
                'study_hours': row[2],
                'internal_marks': row[3],
                'assignments_submitted': row[4],
                'activities': row[5],
                'prediction': row[6],
                'confidence': row[7],
                'timestamp': row[8]
            })
        
        return jsonify(history)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy', 'model_loaded': model is not None})

if __name__ == '__main__':
    app.run(debug=False, port=5000, use_reloader=False)