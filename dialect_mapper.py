# from transformers import BertTokenizer, BertForSequenceClassification
# from googletrans import Translator
# import torch

# # Load Model
# tokenizer = BertTokenizer.from_pretrained("dialect_bert_model")
# model = BertForSequenceClassification.from_pretrained("dialect_bert_model")
# translator = Translator()

# def detect_dialect_and_translate(text):
#     # Simple keyword-based dialect detection
#     if any(word in text for word in ['rayya', 'podaraa', 'aabbaa']):
#         dialect = "Chittoor"
#     else:
#         dialect = "East Godavari"

#     # Convert to standard Telugu
#     inputs = tokenizer(text, return_tensors="pt", truncation=True, padding='max_length', max_length=32)
#     outputs = model(**inputs)
#     predicted_ids = torch.argmax(outputs.logits, dim=1)
#     std_telugu = tokenizer.decode(predicted_ids)

#     # Translate to English
#     translation = translator.translate(std_telugu, src='te', dest='en')
#     return dialect, std_telugu, translation.text

# model_path = "dialect_bert_model"

# tokenizer = BertTokenizer.from_pretrained(model_path)
# model = BertForSequenceClassification.from_pretrained(model_path)

# def predict_dialect(text):
#     inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
#     with torch.no_grad():
#         outputs = model(**inputs)
#     predicted = torch.argmax(outputs.logits, dim=1).item()
#     # Map predicted index to dialect
#     return "Chittoor" if predicted == 0 else "East Godavari"

from transformers import BertTokenizer, EncoderDecoderModel
import torch

# Load the trained model
model_path = "dialect_bert_model"
tokenizer = BertTokenizer.from_pretrained(model_path)
model = EncoderDecoderModel.from_pretrained(model_path)

def detect_dialect_and_translate(input_text):
    inputs = tokenizer(input_text, return_tensors="pt", padding=True, truncation=True)
    with torch.no_grad():
        outputs = model.generate(**inputs, max_length=40)
    translated = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return translated
