# This is the main script

import Text2Voice
import Voice2Text
import openai




OPENAI_API_KEY=""
LLM = "gpt-3.5-turbo"


def TTS(speaker, text):
    """
    this function serves for generating the audio from text
    :param speaker: string, the spoken person.
    :param text: string, the generated audio
    :return:
    """
    model = Text2Voice.SpeechT5()   # initialize the model
    audio = model.audio_generator(text)   # generating the audio
    speaker = "../temp/" + speaker + ".wav"
    model.write_wav(speaker, audio)


def _chat(message, model):
    """
    this function servers for request response from chatgpt model.
    :param message: list
    :param model: string
    :return: response from
    """
    response = openai.ChatCompletion.create(
        model      = model,
        messages   = message,
        max_tokens = 256
    )

    response = {"role": "assistant", "content": response['choices'][0]['message']['content']}
    return response


def full_chat(message, model):
    """
    This function servers for take full conversation
    :param message: list
    :param model:
    :return: alice response, stable diffusion description
    """
    alice_response = _chat(message, model)
    message.append(alice_response)


    return alice_response


def main():
    """
    this is the main function
    :return:
    """
    openai.api_key = OPENAI_API_KEY # set up your key

    #set up the background info and individual character.
    with open( "../character/alice.txt", "r") as f:
        background = f.read()  # because the quote problem, it conflict with the quote sign that in the background.
        message = [{"role": "system", "content": background}]
    # it will take info either from text or from voice.


    # take the response from alice
    alice_response, sd_description = full_chat(message, model = LLM)

    # generate audio
    print(sd_description["content"])
    print("new_line" + alice_response['content'])
    TTS(speaker="alice", text = alice_response["content"])

    # generate picture





if __name__ == '__main__':
    main()


