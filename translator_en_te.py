from transformers import MarianMTModel, MarianTokenizer

# Use the English -> Telugu model
model_name = 'Helsinki-NLP/opus-mt-en-te'

tokenizer = MarianTokenizer.from_pretrained(model_name)
model = MarianMTModel.from_pretrained(model_name)

def translate_en_to_te(text):
    if not text.strip():
        return "Input text is empty."

    # Prepare batch for translation
    batch = tokenizer.prepare_seq2seq_batch([text], return_tensors="pt")

    # Generate translation output IDs
    translated = model.generate(**batch)

    # Decode the generated IDs to Telugu string
    output = tokenizer.decode(translated[0], skip_special_tokens=True)
    return output

# Example test
if __name__ == "__main__":
    en_input = "I am hungry"
    print("Telugu Translation:", translate_en_to_te(en_input))
