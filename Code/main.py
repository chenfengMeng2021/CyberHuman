# This is the main script

import Text2Voice
import Voice2Text





def main():
    # Text2Voice
    Voicemodel = Text2Voice.TTSOriginalModel()
    # I need to find a way that split the speech into smaller part.
    Voice = Voicemodel.audio_generator(text_prompt="Hello, My name is Alice. Is there anything I can help you?")
    Voicemodel.write_wav(location="temp/speech.wav", speech=Voice)

    textmodel = Voice2Text.Whisper()
    text = textmodel.textgenerator("temp/speech.wav")
    print(text)

if __name__ == '__main__':
    main()


