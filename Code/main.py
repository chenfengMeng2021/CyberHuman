# This is the main script

from Text2Voice import speak_out
from Voice2Text import WhisperModel
from LLMcore import ChatBot
import openai

import tkinter as tk
import threading
from getVoice import AudioRecorder





class ConversationBot():
    def __init__(self, openai_api_key):
        self.srm = WhisperModel()
        self.chat = ChatBot(openai_api_key)
    def conversation(self):
        text = self.srm.generate_text()
        response = self.chat.response(text)
        speak_out(response)
        return text, response


def get_openai_api():
    # Create a top-level window for the input dialog
    openai_api_key = ""
    input_win = tk.Tk()
    input_win.title("Enter the OPENAI key")

    lbl_prompt = tk.Label(input_win, text="Enter your Openai API key:")
    lbl_prompt.pack(pady=10)

    entry_input = tk.Entry(input_win)
    entry_input.pack(pady=10)

    # This function will set the value and close the window
    def submit():
        nonlocal openai_api_key
        openai_api_key = entry_input.get()
        input_win.destroy()

    btn_submit = tk.Button(input_win, text="Submit", command=submit)
    btn_submit.pack(pady=10)

    input_win.mainloop()

    return openai_api_key



def main():
    api_key = get_openai_api()

    recorder = AudioRecorder()
    chatmodel = ConversationBot(api_key)

    def on_keypress(event):
        if not recorder.is_recording:
            threading.Thread(target=recorder.start_recording).start()
            lbl.config(text="Recording...")

    def on_keyrelease(event):
        if recorder.is_recording:  # To ensure this function doesn't run after stopping recording and before starting a new one
            recorder.stop_recording()
            lbl.config(text="Recording Stopped. Saving...")
            recorder.save_audio()
            lbl.config(text="Audio saved as output.wav. Press space to record again.")
            # call the chatbot
            user_speech, assistant_response = chatmodel.conversation()

            #Temporarily change the Text widget to normal state.
            txt_history.config(state=tk.NORMAL)

            # insert and returned strings into the Text widget
            txt_history.insert(tk.END, "User:" + user_speech + "\n")
            txt_history.insert(tk.END, "Assistant:" + assistant_response + "\n")
            txt_history.see(tk.END)

            # Set the Text widget back to DISABLED state to make it read-only
            txt_history.config(state=tk.DISABLED)

    root = tk.Tk()
    root.title("CyberHuman Project")

    # Set window size
    width = 600  # window width
    height = 400  # window height
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Calculate position
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    root.geometry('%dx%d+%d+%d' % (width, height, x, y))

    #pack the history of talk
    txt_history = tk.Text(root, height = 10, width = 50)
    txt_history.config(state=tk.DISABLED)
    txt_history.pack(pady=10)

    lbl = tk.Label(root, text="Press the spacebar to start recording.")
    lbl.pack(pady=10)



    root.bind("<KeyPress-space>", on_keypress)
    root.bind("<KeyRelease-space>", on_keyrelease)


    root.mainloop()

    recorder.close()


if __name__ == "__main__":
    main()
