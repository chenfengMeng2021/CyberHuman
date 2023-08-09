"""This is a script for speech recognition"""

# whisper model
import whisper


class WhisperModel:
    def __init__(self, language):
        if language == "en":
            self.model = whisper.load_model("base.en")
        elif language == "zh":
            self.model = whisper.load_model("base")

    def generate_text(self):
        user_speech = self.model.transcribe("../temp/user_speech.wav")["text"]
        return user_speech


