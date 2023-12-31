import requests
import io
import base64
from PIL import Image

CKPTMODELDICT = {"realistic":"chilloutmix_NiCkpt.safetensors",
                 "animation1":"ghostmix_v20Bakedvae.safetensors",
                 "animation2":"AnythingV5Ink_ink.safetensors",
                 "cute_animation":"cuteyukimixAdorable_neochapter3.safetensors",
                 "2.5D":"dreamshaper_8.safetensors"}

class ImageGenerator:
    def __init__(self, ckptmodel):
        self.url = url = "http://127.0.0.1:7860"
        option_payload = {
            "sd_model_checkpoint": ckptmodel,
            "CLIP_stop_at_last_layers": 2
        }
        requests.post(url=f'{url}/sdapi/v1/options', json=option_payload)


    def generate(self, style, prompt,
                 loras, image_width, image_height):

        for i in range(len(loras)):
            loras[i] = f" <lora:{loras[i]}>"

        loras = ", ".join(loras)
        prompt = prompt + loras
        print(prompt)
        payload = {
            "prompt": prompt,
            "styles": [
                style
            ],
            "width": image_width,
            "height": image_height,
            "steps": 30,
            "cfg_scale": 6,
            "eta": 0,
            "override_settings": {},
            "override_settings_restore_afterwards": True,
            "sampler_index": "DPM++ 2M Karras"
        }

        response = requests.post(url=f'{self.url}/sdapi/v1/txt2img', json=payload)

        r = response.json()
        i = r['images'][0]
        image = Image.open(io.BytesIO(base64.b64decode(i.split(",", 1)[0])))

        return image



