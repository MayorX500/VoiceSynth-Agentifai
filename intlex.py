# intlex.py

import torch

## This exists in the requirements.txt file, but the linting is not recognizing it
from TTS.api import TTS # type: ignore


# Get device
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Running on {device}")

# List available 🐸TTS models
# print(TTS().list_models())

# Init TTS with the target model name
tts = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2", progress_bar=False).to(device)

# Run TTS
tts.tts_to_file(text="Susie suddenly lashes out, sending the cereal bowl flying from the counter out into kitchen space. It smashes to pieces against a side cupboard and lays silent on the floor in thick white shards. “Turn it off,” she shouts. “Yes, Miss Susie.” The grey woman on the grey beach vanishes and there …", file_path="outputs/generated.wav", speaker_wav="inputs/voices/eng_morgan_freeman.mp3", language = "en")