""""This is a modules for storing the Large language model and method"""

import openai
import json



class ChatBot():
    def __init__(self):
        OPENAI_API_KEY = ""
        openai.api_key = OPENAI_API_KEY
        self.message = [
            {"role": "system", "content": "your name is alice, and you are a helpful assistant"}
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


