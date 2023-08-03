'''Introduction: this is a script for generating Voice based on Text info'''


import subprocess

def speak_out(alice_speech):
    command = "edge-playback --text "
    command = command + "\"" + alice_speech +"\""
    subprocess.run(command, shell=True)


speak_out("Hello world")
