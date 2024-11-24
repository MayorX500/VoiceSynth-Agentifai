import sys
import os

import torch
import argparse as ap
import torchaudio
from TTS.tts.configs.xtts_config import XttsConfig
from TTS.tts.models.xtts import Xtts
import json  

def clear_memory():
    print("Clearing memory...")
    torch.cuda.empty_cache()


class Model():
    config: dict[str, str]
    model: Xtts
    xtts_config: XttsConfig
    base_voice: str
    gpt_cond_latent: None
    speaker_embedding: None

    def __init__(self, config_file: str):
        print("Loading model...")
        with open(config_file, "r") as f:
            self.config = json.load(f)
        self.xtts_config = XttsConfig()
        self.xtts_config.load_json(self.config.get("xtts_config", None))
        self.model = Xtts.init_from_config(self.xtts_config)
        self.base_voice = self.config.get("base_voice", None)
        conf_file = self.config.get("model", None)
        if conf_file is not None:
            self.model.load_checkpoint(self.xtts_config, **conf_file)
            if torch.cuda.is_available():
                print("CUDA available, running on GPU")
                self.model.cuda()
            else :
                print("CUDA not available, running on CPU")
        else: 
            print("No checkpoint file provided")
            exit(1)

    def get_conditioning_latents(self):
        print("Computing speaker latents...")
        self.gpt_cond_latent, self.speaker_embedding = self.model.get_conditioning_latents(audio_path=[self.base_voice])
        return self.gpt_cond_latent, self.speaker_embedding

    def inference(self, text, lang = "pt", gpt_cond_latent=None, speaker_embedding=None, **kwargs):
        # Use default values from the object if they are not provided in the method call
        if gpt_cond_latent is None:
            gpt_cond_latent = self.gpt_cond_latent
        if speaker_embedding is None:
            speaker_embedding = self.speaker_embedding
        if kwargs is None:
            kwargs = {"length_penalty":1.0,"repetition_penalty":2.5, "top_k":20, "top_p":0.95, "do_sample":True,"temperature":0.3}
        else:
            kwargs = {**{"length_penalty":1.0,"repetition_penalty":2.5, "top_k":20, "top_p":0.95, "do_sample":True,"temperature":0.3}, **kwargs}
        print("Generating audio...")
        return self.model.inference(text, lang, gpt_cond_latent, speaker_embedding, **kwargs)
    
    def save_audio(self, path, wav):
        print("Saving audio...")
        torchaudio.save(path, torch.tensor(wav).unsqueeze(0), 24000)

    def generate_audio(self, text, lang = "pt", **kwargs):
        # TODO: finish implementing text normalization
        wav = self.inference(text, lang, self.gpt_cond_latent, self.speaker_embedding, **kwargs)
        return wav["wav"]

def main(args):
    model = Model(args.configuration)
    model.get_conditioning_latents()
    wav = model.generate_audio(args.text, args.lang, **args.kwargs)
    ## Save audio to file
    model.save_audio(args.output, wav)
    clear_memory()

if __name__ == "__main__":
    parser = ap.ArgumentParser()
    parser.add_argument("text", type=str, help="Text to be synthesized")
    parser.add_argument("configuration", type=str, help="Path to the model configuration file")
    parser.add_argument("--lang", type=str, choices=["pt","en", "es", "fr", "de"], default="pt", help="Language of the text")   
    parser.add_argument("--output", type=str, default="output.wav", help="Output wav file")
    parser.add_argument("--kwargs", type=dict, default={"length_penalty":1.0,"repetition_penalty":2.5, "top_k":20, "top_p":0.95, "do_sample":True,"temperature":0.5}, help="Inference extra arguments")
    args = parser.parse_args()
    main(args)