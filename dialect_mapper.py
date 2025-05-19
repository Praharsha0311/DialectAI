import csv

def load_dialect_dict(csv_path):
    mapping = {}
    with open(csv_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            mapping[row[list(row.keys())[0]].strip()] = row['Standard Telugu'].strip()
    return mapping

chittoor_dict = load_dialect_dict('dialect_data/chittoor_dialect.csv')
east_dict = load_dialect_dict('dialect_data/east_godavari_dialect.csv')

def detect_dialect_and_translate(sentence):
    words = sentence.strip().split()

    chittoor_score = sum([1 for w in words if w in chittoor_dict])
    east_score = sum([1 for w in words if w in east_dict])

    detected = "Chittoor" if chittoor_score > east_score else "East Godavari"
    dialect_dict = chittoor_dict if detected == "Chittoor" else east_dict

    translated_words = [dialect_dict.get(w, w) for w in words]
    standard_telugu = ' '.join(translated_words)

    return standard_telugu, detected
