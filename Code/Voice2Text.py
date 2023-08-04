"""This is a script for speech recognition"""

# whisper model
import whisper

class Whisper:
    def __init__(self, model_size = "base"):
        self.model = whisper.load_model(model_size)
    def textgenerator(self, radio):
        """
        this function servers for generating the text prompt from audio
        :param radio: the location of the radio format, inlcude m4a, wav, mp4
        :return:
        """
        Textprompt = self.model.transcribe(radio)
        return Textprompt['text']


model = whisper.load_model("base")
result = model.transcribe("./temp/speech.wav")
print(result["text"])