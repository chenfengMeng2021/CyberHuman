""""This is a modules for storing the Large language model and method"""

import openai



def read_background(language):
    if language == "zh":
        with open("../character/alice.txt", encoding='utf-8') as f:
            background = f.read()

    elif language == 'en':
        with open('../character/alice.txt', "r") as f:
            background = f.read()
    return background



class ChatBot():
    def __init__(self, openai_api_key, language):
        openai.api_key = openai_api_key
        background = read_background(language)

        self.message = [
            {"role": "system", "content": background}
        ]

    def response(self, user_speech):
        self.message.append({"role": "user", "content": f"{user_speech}"})

        openai_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=self.message
        )
        assistant_response = {"role": "assistant", "content": openai_response['choices'][0]['message']['content']}
        self.message.append(assistant_response)
        return assistant_response['content']



