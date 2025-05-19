import whisper

def transcribe_audio(file_path):
    print("📥 Received file:", file_path)
    model = whisper.load_model("base")  # or "tiny" if slow
    result = model.transcribe(file_path)
    print("📄 Transcribed text:", result["text"])
    return result["text"]
