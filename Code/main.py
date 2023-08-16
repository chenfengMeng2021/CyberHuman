# This is the main script



from Voice2Text import WhisperModel
from LLMcore import ChatBot
from Text2Voice import df, speak_out
from tkinter import ttk
import tkinter as tk
import threading
from getVoice import AudioRecorder
from PIL import Image, ImageTk
from Text2Image import ImageGenerator
import os

positive_prompt = "1 girl, solo, smiling, light blue eyes, sugar pink hair, white beanie, pink cloth, white mini skirt, knee length socks, hearts, cute, sparkly, holding cat, chibi, (pastel pink), glitter"
negative_prompt = "NG_DeepNegative_V1_75T, EasyNegativeV2,  extra fingers, fewer fingers, lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality, normal quality, jpeg artifacts, signature, watermark, username, blurry, (worst quality, low quality:1.4), Negative2, (low quality, worst quality:1.4), (bad anatomy), (inaccurate limb:1.2), bad composition, inaccurate eyes, extra digit,fewer digits, (extra arms:1.2), (bad-artist:0.6), bad-image-v2-39000,"
loras = []
style = "animation"


ckptmodeldict = {"realistic":"chilloutmix_NiCkpt.safetensors",
                 "animation1":"ghostmix_v20Bakedvae.safetensors",
                 "animation2":"AnythingV5Ink_ink.safetensors",
                 "cute_animation":"cuteyukimixAdorable_neochapter3.safetensors",
                 "2.5D":"dreamshaper_8.safetensors"}




class ConversationBot():
    def __init__(self, openai_api_key, voice, character_path, translator_path):
        language = voice[0:2]
        self.srm = WhisperModel(language)
        self.chat = ChatBot(openai_api_key, language, translator_path, character_path)
    def conversation(self):
        text = self.srm.generate_text()
        response = self.chat.response(text)
        return text, response


def initial():
    # Create a top-level window for the input dialog
    openai_key = ""
    voice      = ""

    input_win = tk.Tk()
    input_win.title("Initial Setting")

    file_path = "../prompt/characters"
    characters = os.listdir(file_path)
    print(characters)


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
            response = "你好，很高兴认识你"
        elif language == "en":
            response = "Hi, Nice to meet you"
        speak_out(response, name_var.get())


    def submit():
        nonlocal openai_key
        nonlocal voice
        openai_key = key_input.get()
        voice = name_var.get()
        input_win.destroy()

    lbl_label = tk.Label(input_win, text="Enter your Openai API key:")
    lbl_label.grid(row=0, column=1, padx=10, pady=10)

    key_input = tk.Entry(input_win)
    key_input.grid(row=0, column=2, padx=10, pady=10)

    # Sound bar
    voice_label = tk.Label(input_win, text="Voice: ")
    voice_label.grid(row=1, column=0, padx=10, pady=10)

    language_label = tk.Label(input_win, text="Language")
    language_label.grid(row=1, column=1, padx=10, pady=10)

    language_var = tk.StringVar()
    language_dropdown = ttk.Combobox(input_win, textvariable=language_var, values=df['Language'].unique().tolist())
    language_dropdown.bind('<<ComboboxSelected>>', on_language_change)
    language_dropdown.grid(row=1, column=2, padx=10, pady=10)

    gender_label = tk.Label(input_win, text="Gender")
    gender_label.grid(row=2, column=1, padx=10, pady=10)

    gender_var = tk.StringVar()
    gender_dropdown = ttk.Combobox(input_win, textvariable=gender_var)
    gender_dropdown.bind('<<ComboboxSelected>>', on_gender_change)
    gender_dropdown.grid(row=2, column=2, padx=10, pady=10)

    timbre_label = tk.Label(input_win, text="Timbre")
    timbre_label.grid(row=3, column=1, padx=10, pady=10)

    name_var = tk.StringVar()
    name_dropdown = ttk.Combobox(input_win, textvariable=name_var)
    name_dropdown.bind('<<ComboboxSelected>>', on_voice_chosen)
    name_dropdown.grid(row=3, column=2, padx=10, pady=10)

    #Prompt dropdown
    prompt_label = tk.Label(input_win, text="Prompt setting")
    prompt_label.grid(row=4, column=0, padx=10, pady=10)

    character_label = tk.Label(input_win, text="Character Selection")
    character_label.grid(row=4, column=1, padx=10, pady=10)

    character_var = tk.StringVar()
    character_dropdown = ttk.Combobox(input_win, textvariable=character_var)
    character_dropdown['values'] = characters
    character_dropdown.grid(row=4, column=2, padx=10, pady=10)

    #Picture dropdown
    picture_label = tk.Label(input_win, text="Picture setting ")
    picture_label.grid(row=5, column=0, padx=10, pady=10)

    style_label = tk.Label(input_win, text="style selection: ")
    style_label.grid(row=5, column=1, padx=10, pady=10 )

    style_var = tk.StringVar()
    style_dropdown = ttk.Combobox(input_win, textvariable=style_var)
    style_dropdown['values'] = ["animation", "realistic", "photographic", "2.5D"]
    style_dropdown.grid(row=5, column=2, padx=10, pady=10)

    submit_button = ttk.Button(input_win, text="Submit", command=submit)
    submit_button.grid(row=10, column=1, padx=10, pady=10, columnspan=3)

    input_win.mainloop()
    character_path = f'../prompt/characters/{character_var.get()}'
    print(style_var.get())
    return voice, openai_key, character_path, style_var.get()



def main():
    voice, api_key, character_path, style = initial()
    recorder = AudioRecorder()
    translator_path = "../prompt/utilities/translator.txt"
    chatmodel = ConversationBot(api_key, voice, character_path, translator_path)
    
    model = ImageGenerator(ckptmodeldict["cute_animation"])


    def toggle_fullscreen(event=None):
        """Function to toggle between fullscreen and windowed mode."""
        root.attributes("-fullscreen", not root.attributes("-fullscreen"))
        return "break"  # To prevent the propagation of the event

    def end_fullscreen(event=None):
        """Function to end fullscreen mode."""
        root.attributes("-fullscreen", False)
        return "break"  # To prevent the propagation of the event

    def on_keypress(event):
        if not recorder.is_recording:
            threading.Thread(target=recorder.start_recording).start()
            lbl.config(text="Recording...")

    def load_and_resize_image(image_path, width, height):
        """Load and resize an image to the specified dimensions."""
        img = Image.open(image_path)
        img_resized = img.resize((width, height), Image.ANTIALIAS)
        return ImageTk.PhotoImage(img_resized)


    def on_keyrelease(event):
        if recorder.is_recording:  # To ensure this function doesn't run after stopping recording and before starting a new one
            recorder.stop_recording()
            recorder.save_audio()
            lbl.config(text="waiting for response")

            # call the chatbot
            user_speech, assistant_response = chatmodel.conversation()
            lbl.config(text="drawing")

            #generate picture
            image = model.generate(style, positive_prompt, negative_prompt, loras, width//2, height//2)

            # Reload and resize the background image
            #bg_image = load_and_resize_image("../temp/output.png", 1920, 1080)
            img_resized = image.resize((width, height), Image.ANTIALIAS)
            bg_image = ImageTk.PhotoImage(img_resized)

            bg_label.configure(image=bg_image)
            bg_label.image = bg_image

            #Temporarily change the Text widget to normal state.
            txt_history.config(state=tk.NORMAL)
            # insert and returned strings into the Text widget
            txt_history.insert(tk.END, "User:" + user_speech + "\n")
            txt_history.insert(tk.END, "Assistant:" + assistant_response + "\n")
            txt_history.see(tk.END)
            # Set the Text widget back to DISABLED state to make it read-only
            txt_history.config(state=tk.DISABLED)

            # speak out assistant response
            threading.Thread(target=speak_out, args=(assistant_response, voice)).start()

            #set the lbl again
            lbl.config(text = "Press the spacebar to start recording. ")


    root = tk.Tk()
    root.title("CyberHuman Project")
    root.attributes("-fullscreen", True)
    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()


    # Initially load and resize the background image
    bg_image = load_and_resize_image("../temp/output.png", width, height)
    bg_label = tk.Label(root, image=bg_image)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    #pack the history of talk
    txt_history = tk.Text(root, height = 10, width = 50)
    txt_history.config(state=tk.DISABLED)
    txt_history.place(relx=0.5, rely=0.9, anchor='center')

    lbl = tk.Label(root, text="Press the spacebar to start recording.")
    lbl.place(relx=0.5, rely=0.95, anchor='center')


    root.bind("<KeyPress-space>", on_keypress)
    root.bind("<KeyRelease-space>", on_keyrelease)

    # Bind the F11 key to toggle fullscreen mode
    root.bind("<F11>", toggle_fullscreen)
    # Bind the Escape key to end fullscreen mode
    root.bind("<Escape>", end_fullscreen)

    root.mainloop()
    recorder.close()


if __name__ == "__main__":
    main()
