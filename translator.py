# translator.py
import pickle
from deep_translator import GoogleTranslator

with open('model/dialect_model.pkl', 'rb') as f:
    dialect_mapping = pickle.load(f)

def dialect_to_standard(text):
    return dialect_mapping.get(text.lower(), text)

def translate_to_english(standard_text):
    try:
        return GoogleTranslator(source='te', target='en').translate(standard_text)
    except:
        return "Translation failed"

def detect_dialect(input_text):
    for word in input_text.split():
        if word in dialect_mapping:
            if 'chittoor' in dialect_mapping[word].lower():
                return "Chittoor"
            elif 'east' in dialect_mapping[word].lower():
                return "East Godavari"
    return "Not Detected"
