import json
import requests
import io
import base64
from PIL import Image, PngImagePlugin




class ImageGenerator:
    def __init__(self, ckptmodel):
        self.url = url = "http://127.0.0.1:7860"
        option_payload = {
            "sd_model_checkpoint": ckptmodel,
            "CLIP_stop_at_last_layers": 2
        }
        requests.post(url=f'{url}/sdapi/v1/options', json=option_payload)

    def generate(self, style, prompt, negative_prompt, loras):
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
            "width": 910,
            "height": 540,
            "steps": 30,
            "cfg_scale": 6,
            "negative_prompt": negative_prompt,
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



