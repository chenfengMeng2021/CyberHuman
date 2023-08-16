'''Introduction: this is a script for generating Voice based on Text info'''


import subprocess
import pandas as pd
import pygame

# Executing the provided DataFrame construction code

DATA = {
    "Language": ['zh', 'zh', 'zh', 'zh', 'zh', 'zh', 'zh', 'zh', 'zh', 'zh', 'zh', 'zh', 'zh', 'zh', 'en', 'en', 'en', 'en', 'en', 'en', 'en', 'en', 'en', 'en', 'en', 'en', 'en', 'en', 'en', 'en', 'en', 'en', 'en', 'en', 'en', 'en', 'en', 'en', 'en', 'en', 'en', 'en', 'en', 'en', 'en', 'en', 'en', 'en', 'en', 'en', 'en', 'en'],
    "Gender": ['Female', 'Female', 'Male', 'Male', 'Male', 'Male', 'Female', 'Female', 'Female', 'Female', 'Male', 'Female', 'Female', 'Male', 'Female', 'Male', 'Female', 'Male', 'Female', 'Female', 'Male', 'Female', 'Male', 'Male', 'Female', 'Male', 'Female', 'Female', 'Female', 'Male', 'Female', 'Male', 'Male', 'Female', 'Male', 'Female', 'Male', 'Female', 'Female', 'Female', 'Male', 'Female', 'Male', 'Male', 'Female', 'Female', 'Male', 'Male', 'Female', 'Female', 'Male', 'Male'],
    "Name": ['zh-CN-XiaoxiaoNeural', 'zh-CN-XiaoyiNeural', 'zh-CN-YunjianNeural', 'zh-CN-YunxiNeural', 'zh-CN-YunxiaNeural', 'zh-CN-YunyangNeural', 'zh-CN-liaoning-XiaobeiNeural', 'zh-CN-shaanxi-XiaoniNeural', 'zh-HK-HiuGaaiNeural', 'zh-HK-HiuMaanNeural', 'zh-HK-WanLungNeural', 'zh-TW-HsiaoChenNeural', 'zh-TW-HsiaoYuNeural', 'zh-TW-YunJheNeural', 'en-AU-NatashaNeural', 'en-AU-WilliamNeural', 'en-CA-ClaraNeural', 'en-CA-LiamNeural', 'en-GB-LibbyNeural', 'en-GB-MaisieNeural', 'en-GB-RyanNeural', 'en-GB-SoniaNeural', 'en-GB-ThomasNeural', 'en-HK-SamNeural', 'en-HK-YanNeural', 'en-IE-ConnorNeural', 'en-IE-EmilyNeural', 'en-IN-NeerjaExpressiveNeural', 'en-IN-NeerjaNeural', 'en-IN-PrabhatNeural', 'en-KE-AsiliaNeural', 'en-KE-ChilembaNeural', 'en-NG-AbeoNeural', 'en-NG-EzinneNeural', 'en-NZ-MitchellNeural', 'en-NZ-MollyNeural', 'en-PH-JamesNeural', 'en-PH-RosaNeural', 'en-SG-LunaNeural', 'en-SG-WayneNeural', 'en-TZ-ElimuNeural', 'en-TZ-ImaniNeural', 'en-US-AnaNeural', 'en-US-AriaNeural', 'en-US-ChristopherNeural', 'en-US-EricNeural', 'en-US-GuyNeural', 'en-US-JennyNeural', 'en-US-MichelleNeural', 'en-US-RogerNeural', 'en-US-SteffanNeural', 'en-ZA-LeahNeural']
}

DF = pd.DataFrame(DATA)


"""
-----------------------------------------------------------------------------------------------------
class and function
"""

class AudioPlayer:
    def __init__(self):
        pygame.mixer.init()

    def play_sound(self, sound_path):
        """Play the sound at the specified path."""
        try:
            pygame.mixer.music.load(sound_path)
            pygame.mixer.music.play()
        except pygame.error as e:
            print(f"Error playing sound: {e}")

    def stop_sound(self):
        """Stop the currently playing sound."""
        pygame.mixer.music.stop()

    def pause_sound(self):
        """Pause the currently playing sound."""
        pygame.mixer.music.pause()

    def unpause_sound(self):
        """Unpause the currently playing sound."""
        pygame.mixer.music.unpause()

    def is_playing(self):
        """Check if a sound is currently playing."""
        return pygame.mixer.music.get_busy()

    def wait_for_completion(self):
        """Block until the currently playing sound completes."""
        while self.is_playing():
            pygame.time.Clock().tick(10)

    def cleanup(self):
        """Clean up resources."""
        pygame.mixer.quit()



def speak_out(assistant_response, name):

    assistant_response = assistant_response.replace("\n", " ")
    media_create = f"edge-tts --voice {name} " \
                   f"--text \"{assistant_response}\" " \
                   f"--write-media ../temp/assistant_speech.mp3 "
    subprocess.run(media_create, shell=True)
    player = AudioPlayer()
    player.play_sound('../temp/assistant_speech.mp3')
    player.wait_for_completion()
    player.cleanup()



