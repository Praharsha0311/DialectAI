# 🎙️ DialectAI

DialectAI is a web-based translator that converts Telugu dialect text or speech (like Chittoor or East Godavari) into **Standard Telugu** and then translates it into **English**.

---

## 🌐 Features

✅ Register/Login System  
✅ Text and Voice Input  
✅ Dialect Detection (Chittoor / East Godavari)  
✅ Dialect → Standard Telugu → English Translation  
✅ Simple & Beautiful Web Interface

---

## 🏗️ Tech Stack

- **Frontend**: HTML, CSS, JavaScript  
- **Backend**: Python (Flask)  
- **Database**: MySQL (for user login/registration)  
- **ML/NLP**: Pre-trained word mapping from CSV files  
- **APIs**:
  - Whisper/Google Speech-to-Text (voice input)
  - Google Translate (text translation)

---

## 📦 Installation Guide

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/Praharsha0311/DialectAI.git
cd DialectAI

2️⃣ Create & Activate Virtual Environment (Recommended)
python -m venv venv
source venv/bin/activate     # Linux/macOS
venv\Scripts\activate        # Windows

3️⃣ Install Required Packages
pip install -r requirements.txt

4️⃣ Set Up Folder Structure
DialectAI/
├── app.py
├── model/
│   ├── dialect_model.pkl
│   ├── chittoor_dialect.csv
│   └── east_godavari_dialect.csv
├── templates/
│   ├── home.html
│   ├── login.html
│   ├── register.html
│   └── index.html
├── static/
│   └── index.css
├── requirements.txt
└── README.md
Make sure dialect_model.pkl is trained and saved using the two CSV files.

🚀 How to Run
python app.py
Then open in your browser:
http://127.0.0.1:5000/

