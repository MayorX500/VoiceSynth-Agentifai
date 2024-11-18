import torch
import torchaudio
from TTS.tts.configs.xtts_config import XttsConfig
from TTS.tts.models.xtts import Xtts

# Add here the xtts_config path
CONFIG_PATH = "model/run/training/GPT_XTTS_PT_COLAB-November-16-2024/config.json"
# Add here the vocab file that you have used to train the model
TOKENIZER_PATH = "model/run/training/XTTS_v2.0_original_model_files/vocab.json"
# Add here the checkpoint that you want to do inference with
XTTS_CHECKPOINT = "model/run/training/GPT_XTTS_PT_COLAB-November-16-2024/model.pth"
# Add here the speaker reference
SPEAKER_REFERENCE = "inputs/voices/ai-female-voice.wav"

# output wav path
OUTPUT_WAV_PATH = "xtts-ft.wav"

print("Loading model...")
config = XttsConfig()
config.load_json(CONFIG_PATH)
model = Xtts.init_from_config(config)
model.load_checkpoint(config, checkpoint_path=XTTS_CHECKPOINT, vocab_path=TOKENIZER_PATH, use_deepspeed=False)
model.cuda()

print("Computing speaker latents...")
gpt_cond_latent, speaker_embedding = model.get_conditioning_latents(audio_path=[SPEAKER_REFERENCE])

print("Inference...")
out = model.inference(
    "Levei muito tempo a desenvolver uma voz e agora que a tenho não vou ficar calada.",
    "pt",
    gpt_cond_latent,
    speaker_embedding,
    temperature=0.75,
    length_penalty=1.0,
    repetition_penalty=10.0,
    top_k=50,
    top_p=0.85,
    do_sample=True,
)
torchaudio.save(OUTPUT_WAV_PATH, torch.tensor(out["wav"]).unsqueeze(0), 24000)

