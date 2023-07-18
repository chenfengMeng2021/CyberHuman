'''Introduction: this is a script for generating Voice based on Text info'''

from bark import SAMPLE_RATE, generate_audio, preload_models
from scipy.io.wavfile import write as write_wav

from transformers import SpeechT5Processor, SpeechT5ForTextToSpeech, SpeechT5HifiGan
import torch
from datasets import load_dataset
import re

from fairseq.checkpoint_utils import load_model_ensemble_and_task_from_hf_hub
from fairseq.models.text_to_speech.hub_interface import TTSHubInterface
import IPython.display as ipd

# if the models using small models or not.
SUNO_USE_SMALL_MODELS=True


class Text2Voice:
    def __init__(self):
        self.SAMPLERATE = SAMPLE_RATE
        self.TEXTPROMPT = "Hello, I am a cyber human, Do you want to talk with me? "

    def write_wav(self, location, speech, rate=SAMPLE_RATE):
        '''

        :param location: the place where the radio stored
        :param speech: radio file,wav format
        :return:
        '''
        write_wav(location, rate=rate, data=speech)

    def Textspliter(self, text):
        return re.split('[.?!;]', text)




class BarkModel(Text2Voice):
    # you want to write a special prompt for bark
    def __init__(self, smallmodel = True):
        """
        Initialize the setting of Bark Model
        :param smallmodel: Booler, if your VARM is smaller than 12gb, you should make it True.
        """
        preload_models(SUNO_USE_SMALL_MODELS=smallmodel)

    def audio_genorator(self, text_prompt="Hello, My name is Alice. Is there anything I can help you? "):
        """
        this method will generate audio info from bark
        :param self:
        :return:
        """
        speech = generate_audio(text_prompt= text_prompt)

        return speech




class TTSOriginalModel(Text2Voice):
    def __init__(self):
        self.processor = SpeechT5Processor.from_pretrained("microsoft/speecht5_tts")
        self.model = SpeechT5ForTextToSpeech.from_pretrained("microsoft/speecht5_tts")
        self.vocoder = SpeechT5HifiGan.from_pretrained("microsoft/speecht5_hifigan")

    def audio_generator(self, text_prompt = "Hello, My name is Alice. Is there anything I can help you? "):
        # this number is setting arbitrary, feel free to change it later
        if len(text_prompt) > 100:
            text_prompts = TTSOriginalModel.text_spliter(text_prompt)

        inputs = self.processor(text=text_prompt, return_tensors="pt")

        # load xvector containing speaker's voice characteristics from a dataset
        embeddings_dataset = load_dataset("Matthijs/cmu-arctic-xvectors", split="validation")
        speaker_embeddings = torch.tensor(embeddings_dataset[7306]["xvector"]).unsqueeze(0)

        speech = self.model.generate_speech(inputs["input_ids"], speaker_embeddings, vocoder=self.vocoder)
        TTSOriginalModel.write_wav()
        return speech.numpy()


class FastSpeech2(Text2Voice):
    def __init__(self):

        models, self.cfg, self.task = load_model_ensemble_and_task_from_hf_hub(
            "facebook/fastspeech2-en-ljspeech",
            arg_overrides={"vocoder": "hifigan", "fp16": False}
        )
        self.model = models[0]
        TTSHubInterface.update_cfg_with_data_cfg(self.cfg, self.task.data_cfg)
        self.generator = self.task.build_generator(self.model, self.cfg)

    def audio_generator(self, text_prompt = "Hello, this is a test run."):

        sample = TTSHubInterface.get_model_input(self.task, text_prompt)
        wav, rate = TTSHubInterface.get_prediction(self.task, self.model, self.generator, sample)

        ipd.Audio(wav, rate=rate)




