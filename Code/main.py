# This is the main script

from Text2Voice import speak_out
from Voice2Text import WhisperModel
from LLMcore import ChatBot
from Text2Voice import df, speak_out
from tkinter import ttk
import tkinter as tk
import threading
from getVoice import AudioRecorder




class ConversationBot():
    def __init__(self, openai_api_key, voice):
        language = voice[0:2]
        self.srm = WhisperModel(language)
        self.chat = ChatBot(openai_api_key, language)
        self.voice = voice
    def conversation(self):
        text = self.srm.generate_text()
        response = self.chat.response(text)
        speak_out(response, self.voice)
        return text, response


def initial():
    # Create a top-level window for the input dialog
    openai_key = ""
    voice      = ""

    input_win = tk.Tk()
    input_win.title("Initial Setting")


    def on_language_change(event):
        language = language_var.get()
        available_genders = df[df['Language'] == language]['Gender'].unique().tolist()
        gender_dropdown['values'] = available_genders
        gender_var.set('')

    def on_gender_change(event):
        language = language_var.get()
        gender = gender_var.get()
        available_names = df[(df['Language'] == language) & (df['Gender'] == gender)]['Name'].tolist()
        name_dropdown['values'] = available_names
        name_var.set('')

    def on_voice_chosen(event):
        language = language_var.get()
        if language == "zh":
            response = "你好，很高兴为你服务"
        elif language == "en":
            response = "Hi, as your service"
        speak_out(response, name_var.get())

    def submit():
        nonlocal openai_key
        nonlocal voice
        openai_key = key_input.get()
        voice = name_var.get()
        input_win.destroy()

    lbl_prompt = tk.Label(input_win, text="Enter your Openai API key:")
    lbl_prompt.grid(row=0, column=0, padx=10, pady=10)

    key_input = tk.Entry(input_win)
    key_input.grid(row=0, column=1, padx=10, pady=10)

    language_prompt = tk.Label(input_win, text="Language")
    language_prompt.grid(row=1, column=0, padx=10, pady=10)

    language_var = tk.StringVar()
    language_dropdown = ttk.Combobox(input_win, textvariable=language_var, values=df['Language'].unique().tolist())
    language_dropdown.bind('<<ComboboxSelected>>', on_language_change)
    language_dropdown.grid(row=1, column=1, padx=10, pady=10)

    gender_prompt = tk.Label(input_win, text="Gender")
    gender_prompt.grid(row=2, column=0, padx=10, pady=10)

    gender_var = tk.StringVar()
    gender_dropdown = ttk.Combobox(input_win, textvariable=gender_var)
    gender_dropdown.bind('<<ComboboxSelected>>', on_gender_change)
    gender_dropdown.grid(row=2, column=1, padx=10, pady=10)

    voice_prompt = tk.Label(input_win, text="Voice")
    voice_prompt.grid(row=3, column=0, padx=10, pady=10)

    name_var = tk.StringVar()
    name_dropdown = ttk.Combobox(input_win, textvariable=name_var)
    name_dropdown.bind('<<ComboboxSelected>>', on_voice_chosen)
    name_dropdown.grid(row=3, column=1, padx=10, pady=10)

    submit_button = ttk.Button(input_win, text="Submit", command=submit)
    submit_button.grid(row=4, column=0, padx=10, pady=10, columnspan=3)

    input_win.mainloop()

    return voice, openai_key



def main():
    voice, api_key = initial()
    recorder = AudioRecorder()
    chatmodel = ConversationBot(api_key, voice)

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
