from flask import Flask, render_template, request, redirect, session, url_for, session
from deep_translator import GoogleTranslator
import speech_recognition as sr
import os
import pickle
from flask import Flask
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = 'PPS'

import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="users_db"
)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'users_db'

# Initialize MySQL
mysql = MySQL(app)

cursor = db.cursor()

# Load the trained dialect model
with open('model/dialect_model.pkl', 'rb') as f:
    dialect_model = pickle.load(f)

#Function to normalize a sentence
def normalize_sentence(sentence):
    words = sentence.strip().lower().split()
    normalized_words = []
    detected_dialects = []

    for word in words:
        if word in dialect_model:
            normalized_words.append(dialect_model[word])
            detected_dialects.append(get_dialect(word))
        else:
            normalized_words.append(word)
    standard_sentence = ' '.join(normalized_words)
    detected = detected_dialects[0] if detected_dialects else "Not Detected"
    return standard_sentence, detected

def normalize_sentence(input_text):
    import csv

    # Load CSV data for both dialects
    dialects = {
        'Chittoor': 'chittoor_dialect.csv',
        'East Godavari': 'east_godavari_dialect.csv'
    }

    input_words = input_text.split()
    standard_words = []
    dialect_match_count = {'Chittoor': 0, 'East Godavari': 0}

    # Load all dialect word mappings
    dialect_maps = {}
    for dialect, file in dialects.items():
        with open(file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            # Use a consistent key across dialects, like 'Dialect'
            word_map = {row['Dialect Telugu'].strip().lower(): row['Standard Telugu'].strip()
            for row in reader}

            dialect_maps[dialect] = word_map

    # Suffix-only respect markers
    respect_suffixes = {
        'andi': 'East Godavari',
        'ayya': 'Chittoor',
        'amma': 'Chittoor'
    }

    for word in input_words:
        cleaned_word = word.strip(",.?!").lower()
        found = False

        for dialect, word_map in dialect_maps.items():
            if cleaned_word in word_map:
                standard_words.append(word_map[cleaned_word])
                dialect_match_count[dialect] += 1
                found = True
                break

        if not found:
            # Check if it is a suffix that indicates dialect
            if cleaned_word in respect_suffixes:
                dialect_match_count[respect_suffixes[cleaned_word]] += 1
            standard_words.append(word)

    # Detect dialect based on which one had more matches
    detected_dialect = "Not Detected"
    if max(dialect_match_count.values()) > 0:
        detected_dialect = max(dialect_match_count, key=dialect_match_count.get)

    standard_sentence = " ".join(standard_words)
    return standard_sentence, detected_dialect

# def normalize_sentence(input_text):
#     import csv

#     # Load CSV data for both dialects
#     dialects = {
#         'Chittoor': 'chittoor_dialect.csv',
#         'East Godavari': 'east_godavari_dialect.csv'
#     }

#     input_words = input_text.split()
#     standard_words = []
#     dialect_match_count = {'Chittoor': 0, 'East Godavari': 0}

#     # Load all dialect word mappings
#     dialect_maps = {}
#     for dialect, file in dialects.items():
#         with open(file, 'r', encoding='utf-8') as f:
#             reader = csv.DictReader(f)
#             word_map = {row['Dialect Telugu'].strip().lower(): row['Standard Telugu'].strip()
#                         for row in reader}
#             dialect_maps[dialect] = word_map

#     respect_suffixes = {
#         'andi': 'East Godavari',
#         'ayya': 'Chittoor',
#         'amma': 'Chittoor'
#     }

#     for word in input_words:
#         cleaned_word = word.strip(",.?!").lower()
#         found = False

#         for dialect, word_map in dialect_maps.items():
#             if cleaned_word in word_map:
#                 standard_words.append(word_map[cleaned_word])
#                 dialect_match_count[dialect] += 1
#                 found = True
#                 break

#         if not found:
#             for dialect, word_map in dialect_maps.items():
#                 for dialect_word in word_map:
#                     if cleaned_word in dialect_word:
#                         standard_words.append(word_map[dialect_word])
#                         dialect_match_count[dialect] += 1
#                         found = True
#                         break
#                 if found:
#                     break

#         if not found:
#             if cleaned_word in respect_suffixes:
#                 dialect_match_count[respect_suffixes[cleaned_word]] += 1
#             standard_words.append(word)

#     detected_dialect = "Not Detected"
#     if max(dialect_match_count.values()) > 0:
#         detected_dialect = max(dialect_match_count, key=dialect_match_count.get)

#     standard_sentence = " ".join(standard_words)
    
#     # Debug prints (optional, remove in production)
#     print("Input Words:", input_words)
#     print("Standard Sentence:", standard_sentence)
#     print("Dialect Match Count:", dialect_match_count)
#     print("Detected Dialect:", detected_dialect)

#     return standard_sentence, detected_dialect



def clean_respect_suffixes(translated_text):
    respect_words = {
        'andi': '“andi” is a respectful suffix',
        'Andi': '“andi” is a respectful suffix'

    }

    words = translated_text.split()
    cleaned_words = []
    notes = []

    for word in words:
        if word.lower() in respect_words:
            notes.append(respect_words[word.lower()])
        else:
            cleaned_words.append(word)

    result = ' '.join(cleaned_words)
    if notes:
        result += " (" + ', '.join(notes) + ")"
    return result

# Detect dialect from word
import csv

def get_dialect(word):
    for dialect in ['Chittoor', 'East Godavari']:
        filename = f'model/{dialect.lower().replace(" ", "_")}_dialect.csv'
        if os.path.exists(filename):
            with open(filename, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                for row in reader:
                    if len(row) > 0 and row[0].strip().lower() == word:
                        return dialect
    return "Unknown"

def save_translation_history(user_id, input_type, input_text, output_text):
    query = """
    INSERT INTO translation_history (user_id, input_type, input_text, output_text)
    VALUES (%s, %s, %s, %s)
    """
    cursor.execute(query, (user_id, input_type, input_text, output_text))
    db.commit()



# Google Translate instance
# translator = Translator()

# ---------------- Routes ---------------- #

@app.route('/')
def home():
    if 'username' in session:
        return render_template('index.html', username=session['username'])
    return render_template('home.html')

@app.route('/index')
def index():
    return render_template('index.html')



@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # You can add user-saving logic here
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        user = cursor.fetchone()

        if user:
            session['loggedin'] = True
            session['id'] = user['id']
            session['username'] = user['username']
            session['user_id'] = user['id']  # ✅ Make sure this line exists
            return redirect(url_for('index'))
        else:
            return 'Incorrect username/password!'
    return render_template('login.html')



@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT input_text, output_text, translated_at FROM history WHERE user_id = %s ORDER BY translated_at DESC", (user_id,))
    history = cursor.fetchall()  # List of tuples or dicts based on cursor config
    cursor.close()

    return render_template('index.html', username=session['username'], history=history)


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

@app.route('/translate', methods=['POST'])
def translate():
    if 'username' not in session:
        return redirect(url_for('home'))

    username = session['username']

    # Helper function to get user_id from username
    def get_user_id(username):
        query = "SELECT id FROM users WHERE username = %s"
        cursor.execute(query, (username,))
        result = cursor.fetchone()
        return result[0] if result else None

    user_id = get_user_id(username)
    if not user_id:
        # Handle error if user not found
        return "User not found", 404

    input_text = request.form.get('text_input', '').strip().lower()

    # Normalize sentence from dialect to standard Telugu
    standard_telugu, detected_dialect = normalize_sentence(input_text)

    # Translate Standard Telugu to English using Google Translate
    raw_translation = GoogleTranslator(source='te', target='en').translate(standard_telugu)

    # Clean translation to remove dialect-respect suffixes like "Andi"
    def clean_respect_suffixes(text):
        suffix_words = {
            "andi": "(respect suffix, often used in East Godavari)",
            "ayya": "(respect suffix)",
            "amma": "(respect suffix)"
        }

        words = text.split()
        cleaned_words = []
        removed_notes = []

        for word in words:
            lw = word.lower().strip(",.?!")
            if lw in suffix_words:
                removed_notes.append(f"{word} {suffix_words[lw]}")
                continue
            cleaned_words.append(word)

        cleaned_text = " ".join(cleaned_words)
        if removed_notes:
            cleaned_text += "  [" + "; ".join(removed_notes) + "]"
        return cleaned_text

    english_translation = clean_respect_suffixes(raw_translation)

    # Save translation history to DB
    def save_translation_history(user_id, input_type, input_text, output_text):
        query = """
        INSERT INTO translation_history (user_id, input_type, input_text, output_text)
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (user_id, input_type, input_text, output_text))
        db.commit()

    save_translation_history(user_id, 'text', input_text, english_translation)

    return render_template('index.html',
                           username=username,
                           standard_telugu=standard_telugu,
                           english_translation=english_translation,
                           detected_dialect=detected_dialect)

import MySQLdb.cursors

@app.route('/history')
def history():
    if 'username' not in session:
        return redirect(url_for('login'))
    username = session.get('username')
    user_id = session.get('user_id')
    print("SESSION USER_ID:", user_id)  # Debug line

    if not user_id:
        username = session.get('username')
        print("SESSION USERNAME:", username)  # Debug line

        if not username:
            return redirect(url_for('login'))

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
        res = cursor.fetchone()
        print("LOOKED UP USER_ID:", res)  # Debug line

        if res:
            user_id = res['id']
            session['user_id'] = user_id
        else:
            return redirect(url_for('login'))

    # Fetch translation history
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM translation_history WHERE user_id = %s ORDER BY translated_at DESC", (user_id,))
    translations = cursor.fetchall()
    print("TRANSLATIONS:", translations)  # Debug line

    return render_template('history.html', translations=translations, username=username)

    # Now fetch the translations
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM translation_history WHERE user_id = %s ORDER BY translated_at DESC", (user_id,))
    translation_history = cursor.fetchall()

    return render_template('history.html', translation_history=translation_history)

@app.route('/voice_input', methods=['POST'])
def voice_input():
    # Check user session
    if 'username' not in session:
        return redirect(url_for('home'))

    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        try:
            print("🎤 Listening...")
            # Capture audio
            audio = recognizer.listen(source, timeout=5)
            # Convert speech to text (Telugu)
            text = recognizer.recognize_google(audio, language="te-IN")
            # Redirect with recognized text
            return redirect(url_for('translate_with_voice', text=text))
        except sr.UnknownValueError:
            return "❌ Could not understand audio."
        except sr.RequestError as e:
            return f"❌ Google Speech Recognition error: {e}"
        except sr.WaitTimeoutError:
            return "❌ Listening timed out while waiting for phrase."


@app.route('/translate_with_voice')
def translate_with_voice():
    if 'username' not in session:
        return redirect(url_for('home'))

    input_text = request.args.get('text', '').strip().lower()
    standard_telugu, detected_dialect = normalize_sentence(input_text)
    # english_translation = translator.translate(standard_telugu, src='te', dest='en').text
    english_translation = GoogleTranslator(source='te', target='en').translate(standard_telugu)


    return render_template('index.html',
                           username=session.get('username', 'User'),
                           standard_telugu=standard_telugu,
                           english_translation=english_translation,
                           detected_dialect=detected_dialect)

from flask import Flask, render_template, request, redirect, url_for
# from googletrans import Translator  # Make sure this is installed
@app.route('/eng_to_telugu', methods=['GET', 'POST'])
def eng_to_telugu():
    telugu_output = None
    english_text = None
    if request.method == 'POST':
        english_text = request.form['eng_input'].strip()
        lower_text = english_text.lower()

        # Custom translation for specific input
        if lower_text in ['i am hungry', 'iam hungry', 'iam hundgry']:
            telugu_output = 'నాకు ఆకలిగా ఉంది'
        elif lower_text in['good morning']:
            telugu_output='శుభోదయం'
        else:
            telugu_output = GoogleTranslator(source='en', target='te').translate(english_text)


    return render_template('eng_to_telugu.html', telugu_output=telugu_output, english_text=english_text)

# Run the server
if __name__ == "__main__":
    app.run(debug=True)