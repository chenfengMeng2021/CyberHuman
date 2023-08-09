'''Introduction: this is a script for generating Voice based on Text info'''


import subprocess
import pyaudio
import wave
import time
import pandas as pd


# Executing the provided DataFrame construction code

data = {
    "Language": ['zh', 'zh', 'zh', 'zh', 'zh', 'zh', 'zh', 'zh', 'zh', 'zh', 'zh', 'zh', 'zh', 'zh', 'en', 'en', 'en', 'en', 'en', 'en', 'en', 'en', 'en', 'en', 'en', 'en', 'en', 'en', 'en', 'en', 'en', 'en', 'en', 'en', 'en', 'en', 'en', 'en', 'en', 'en', 'en', 'en', 'en', 'en', 'en', 'en', 'en', 'en', 'en', 'en', 'en', 'en'],
    "Gender": ['Female', 'Female', 'Male', 'Male', 'Male', 'Male', 'Female', 'Female', 'Female', 'Female', 'Male', 'Female', 'Female', 'Male', 'Female', 'Male', 'Female', 'Male', 'Female', 'Female', 'Male', 'Female', 'Male', 'Male', 'Female', 'Male', 'Female', 'Female', 'Female', 'Male', 'Female', 'Male', 'Male', 'Female', 'Male', 'Female', 'Male', 'Female', 'Female', 'Female', 'Male', 'Female', 'Male', 'Male', 'Female', 'Female', 'Male', 'Male', 'Female', 'Female', 'Male', 'Male'],
    "Name": ['zh-CN-XiaoxiaoNeural', 'zh-CN-XiaoyiNeural', 'zh-CN-YunjianNeural', 'zh-CN-YunxiNeural', 'zh-CN-YunxiaNeural', 'zh-CN-YunyangNeural', 'zh-CN-liaoning-XiaobeiNeural', 'zh-CN-shaanxi-XiaoniNeural', 'zh-HK-HiuGaaiNeural', 'zh-HK-HiuMaanNeural', 'zh-HK-WanLungNeural', 'zh-TW-HsiaoChenNeural', 'zh-TW-HsiaoYuNeural', 'zh-TW-YunJheNeural', 'en-AU-NatashaNeural', 'en-AU-WilliamNeural', 'en-CA-ClaraNeural', 'en-CA-LiamNeural', 'en-GB-LibbyNeural', 'en-GB-MaisieNeural', 'en-GB-RyanNeural', 'en-GB-SoniaNeural', 'en-GB-ThomasNeural', 'en-HK-SamNeural', 'en-HK-YanNeural', 'en-IE-ConnorNeural', 'en-IE-EmilyNeural', 'en-IN-NeerjaExpressiveNeural', 'en-IN-NeerjaNeural', 'en-IN-PrabhatNeural', 'en-KE-AsiliaNeural', 'en-KE-ChilembaNeural', 'en-NG-AbeoNeural', 'en-NG-EzinneNeural', 'en-NZ-MitchellNeural', 'en-NZ-MollyNeural', 'en-PH-JamesNeural', 'en-PH-RosaNeural', 'en-SG-LunaNeural', 'en-SG-WayneNeural', 'en-TZ-ElimuNeural', 'en-TZ-ImaniNeural', 'en-US-AnaNeural', 'en-US-AriaNeural', 'en-US-ChristopherNeural', 'en-US-EricNeural', 'en-US-GuyNeural', 'en-US-JennyNeural', 'en-US-MichelleNeural', 'en-US-RogerNeural', 'en-US-SteffanNeural', 'en-ZA-LeahNeural']
}

df = pd.DataFrame(data)


"""
-----------------------------------------------------------------------------------------------------
class and function
"""

class AudioPlayer:
    def __init__(self):
        self.p = pyaudio.PyAudio()

    def play(self, filename):
        wf = wave.open(filename, 'rb')

        def callback(in_data, frame_count, time_info, status):
            data = wf.readframes(frame_count)
            return (data, pyaudio.paContinue)

        stream = self.p.open(format=self.p.get_format_from_width(wf.getsampwidth()),
                             channels=wf.getnchannels(),
                             rate=wf.getframerate(),
                             output=True,
                             stream_callback=callback)

        stream.start_stream()

        while stream.is_active():
            time.sleep(0.1)

        stream.stop_stream()
        stream.close()
        wf.close()

    def close(self):
        self.p.terminate()


def speak_out(assistant_response, name):

    assistant_response = assistant_response.replace("\n", " ")
    media_create = f"edge-tts --voice {name} --text \"{assistant_response}\" --write-media ../temp/assistant_speech.mp3  --write-subtitles ../temp/assistant_speech.vtt"
    subprocess.run(media_create, shell=True)
    format_change = f"ffmpeg -i ../temp/assistant_speech.mp3 -y ../temp/assistant_speech.wav "
    subprocess.run(format_change, shell=True)
    player = AudioPlayer()
    player.play('../temp/assistant_speech.wav')
    player.close()





