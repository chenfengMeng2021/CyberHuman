""""This is a modules for storing the Large language model and method"""

import openai



def read_background(language, path):
    if language == "zh":
        with open(path, encoding='utf-8') as f:
            background = f.read()

    elif language == 'en':
        with open(path, "r") as f:
            background = f.read()
    return background


class _Translator():
    def __init__(self, openai_api_key, translator_path):
        openai.api_key = openai_api_key

        with open(translator_path, "r") as f:
            translate_description = f.read()
        self.message = [
            {"role": "system", "content": translate_description}
        ]

    def tranlate(self, user_speech):
        self.message.append({"role": "user", "content": f"{user_speech}"})

        openai_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=self.message,
            temperature=0
        )
        assistant_response = {"role": "assistant",
                              "content":
                                  openai_response['choices'][0]['message']['content']}
        self.message.append(assistant_response)
        return assistant_response['content']


class ChatBot():
    def __init__(self, openai_api_key, language, translator_path,  character_path):
        openai.api_key = openai_api_key

        background = read_background(language, character_path)

        # initial translator
        self.translator = _Translator(openai_api_key, translator_path)

        self.message = [
            {"role": "system", "content": background}
        ]

    def response(self, user_speech):
        # send the message to the translator to corract it at first.
        user_speech = self.translator.tranlate(user_speech)

        # append the corrected one to message
        self.message.append({"role": "user", "content": f"{user_speech}"})
        openai_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=self.message
        )

        assistant_response = {"role": "assistant",
                              "content":
                                  openai_response['choices'][0]['message']['content']}
        self.message.append(assistant_response)

        return assistant_response['content']
