import speech_recognition as sr
from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate

# Initialize recognizer
r = sr.Recognizer()

# Load audio file
with sr.AudioFile("audio/audio.wav") as source:
    print("🎙️ Listening...")
    audio_data = r.record(source)

    try:
        # Step 1: Recognize Telugu speech using Google API
        telugu_text = r.recognize_google(audio_data, language='te-IN')
        print("📝 Telugu Script Output:")
        print(telugu_text)

        # Step 2: Transliterate Telugu script to English letters (ITRANS format)
        transliterated = transliterate(telugu_text, sanscript.TELUGU, sanscript.ITRANS)
        print("🔤 Transliterated Output (English letters):")
        print(transliterated)

    except sr.UnknownValueError:
        print("❌ Could not understand audio.")
    except sr.RequestError:
        print("❌ API request failed. Check your internet connection.")
