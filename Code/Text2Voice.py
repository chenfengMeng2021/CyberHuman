'''Introduction: this is a script for generating Voice based on Text info'''


import subprocess
import pyaudio
import wave
import time



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




def speak_out(alice_speech):

    alice_speech = alice_speech.replace("\n", " ")
    media_create = f"edge-tts --text \"{alice_speech}\" --write-media ../temp/assistant_speech.mp3  --write-subtitles ../temp/assistant_speech.vtt"
    subprocess.run(media_create, shell=True)
    format_change = f"ffmpeg -i ../temp/assistant_speech.mp3 -y ../temp/assistant_speech.wav "
    subprocess.run(format_change, shell=True)
    player = AudioPlayer()
    player.play('../temp/assistant_speech.wav')
    player.close()


