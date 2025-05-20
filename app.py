from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os
from whisper_module import transcribe_audio
from dialect_mapper import detect_dialect_and_translate
from translate_module import translate_to_english
from users_db import init_user_db
import subprocess
import traceback

from flask import Flask, render_template, request, redirect, session, jsonify
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "PPS"

# Database connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",  # Use your MySQL password here if set
    database="users_db"
)
cursor = db.cursor(dictionary=True)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])

        cur = db.cursor()
        cur.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
                    (username, email, password))
        db.commit()
        cur.close()

        return redirect('/login')
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        cur = db.cursor(dictionary=True)
        try:
            cur.execute("SELECT * FROM users WHERE email = %s", (email,))
            user = cur.fetchone()  # ✅ MUST read the result before closing cursor

        finally:
            cur.close()  # ✅ Now it's safe to close

        if user and check_password_hash(user['password'], password):
            session['username'] = user['username']
            return redirect('/index')
        else:
            return render_template('login.html', error="Invalid credentials")

    return render_template('login.html')



@app.route('/index')
def index():
    if 'username' not in session:
        return redirect('/login')
    return render_template('index.html', username=session['username'])

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

# Add your other routes (e.g., /translate, /process_audio) below...

if __name__ == '__main__':
    app.run(debug=True)

app = Flask(__name__)
CORS(app)

# Initialize MySQL user DB (create table if not exists)
init_user_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/record_audio', methods=['POST'])
def record_audio():
    # You would normally record via frontend mic. For now, we use a sample audio
    audio_file = "sample_audio.wav"  # Later replace with real audio capture
    text = transcribe_audio(audio_file)
    return jsonify({'transcribed_text': text})

@app.route('/translate', methods=['POST'])
def translate():
    data = request.get_json()
    dialect_text = data.get("input_text", "")

    standard_telugu, detected_dialect = detect_dialect_and_translate(dialect_text)
    english_translation = translate_to_english(standard_telugu)

    return jsonify({
        'dialect': detected_dialect,
        'standard_telugu': standard_telugu,
        'english_translation': english_translation
    })

import traceback  # Make sure this is at the top of app.py

@app.route('/process_audio', methods=['POST'])
def process_audio():
    print("🔵 /process_audio endpoint hit")

    if 'audio_data' not in request.files:
        print("❌ No audio_data in request.files")
        return jsonify({'error': 'No audio file uploaded'}), 400

    audio = request.files['audio_data']
    file_path = os.path.join("uploads", "recorded.wav")

    try:
        # Ensure uploads folder exists
        os.makedirs("uploads", exist_ok=True)
        audio.save(file_path)
        print("✅ Audio saved at:", file_path)

        # Transcribe using Whisper
        print("🔁 Starting transcription...")
        text = transcribe_audio(file_path)
        print("✅ Transcription result:", text)

        return jsonify({'transcribed_text': text})

    except Exception as e:
        print("❌ Whisper transcription failed")
        traceback.print_exc()  # Shows detailed error
        return jsonify({'error': 'Transcription failed'}), 500


if __name__ == '__main__':
    app.run(debug=True)
