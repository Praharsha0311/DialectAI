import pandas as pd
import pickle
import os

# Load both dialect CSVs from model folder
chittoor = pd.read_csv('chittoor_dialect.csv')
east_godavari = pd.read_csv('east_godavari_dialect.csv')

# Mapping from Dialect (in English letters) to Standard Telugu
dialect_to_std = {}

# Map Chittoor dialect
for _, row in chittoor.iterrows():
    dialect = str(row['Dialect Telugu']).strip().lower()
    standard = str(row['Standard Telugu']).strip()
    dialect_to_std[dialect] = standard

# Map East Godavari dialect
for _, row in east_godavari.iterrows():
    dialect = str(row['Dialect Telugu']).strip().lower()
    standard = str(row['Standard Telugu']).strip()
    dialect_to_std[dialect] = standard

# Save the trained model as a pickle file
os.makedirs('model', exist_ok=True)
with open('model/dialect_model.pkl', 'wb') as f:
    pickle.dump(dialect_to_std, f)

print("✅ Model trained and saved as model/dialect_model.pkl")
