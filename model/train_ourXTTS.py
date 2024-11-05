import os

import torch
from trainer import Trainer, TrainerArgs
from TTS.config.shared_configs import BaseDatasetConfig
from TTS.tts.datasets import load_tts_samples
from TTS.tts.layers.xtts.trainer.gpt_trainer import GPTArgs, GPTTrainer, GPTTrainerConfig, XttsAudioConfig
from TTS.utils.manage import ModelManager

# Logging parameters
RUN_NAME = "GPT_XTTS_PT_PT_FT"
PROJECT_NAME = "XTTS_trainer_PT_PT"
DASHBOARD_LOGGER = "tensorboard"
LOGGER_URI = None

# Set the path that the checkpoints will be saved
OUT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "run", "training")

# Training Parameters
OPTIMIZER_WD_ONLY_ON_WEIGHTS = True
START_WITH_EVAL = True
BATCH_SIZE = 1
GRAD_ACUMM_STEPS = 300  # Adjust to a higher number

# Define the PT-PT dataset
config_dataset = BaseDatasetConfig(
    formatter="ljspeech",  # Adjust if needed, or if you have a custom formatter for your metadata
    dataset_name="ptpt_dataset",  # Name of your PT-PT dataset
    path="../datasets/train_ep/",  # Path to your dataset directory
    meta_file_train="metadata.txt",  # Path to metadata file
    language="pt-pt", # Language of the dataset
)

# Add the dataset to the list
DATASETS_CONFIG_LIST = [config_dataset]

# Define where XTTS files will be downloaded
CHECKPOINTS_OUT_PATH = os.path.join(OUT_PATH, "XTTS_v1.1_original_model_files/")
os.makedirs(CHECKPOINTS_OUT_PATH, exist_ok=True)

# Define where DVAE files and model checkpoints are located (unchanged)
DVAE_CHECKPOINT_LINK = "https://coqui.gateway.scarf.sh/hf-coqui/XTTS-v1/v1.1.2/dvae.pth"
MEL_NORM_LINK = "https://coqui.gateway.scarf.sh/hf-coqui/XTTS-v1/v1.1.2/mel_stats.pth"

DVAE_CHECKPOINT = os.path.join(CHECKPOINTS_OUT_PATH, DVAE_CHECKPOINT_LINK.split("/")[-1])
MEL_NORM_FILE = os.path.join(CHECKPOINTS_OUT_PATH, MEL_NORM_LINK.split("/")[-1])

if not os.path.isfile(DVAE_CHECKPOINT) or not os.path.isfile(MEL_NORM_FILE):
    print(" > Downloading DVAE files!")
    ModelManager._download_model_files([MEL_NORM_LINK, DVAE_CHECKPOINT_LINK], CHECKPOINTS_OUT_PATH, progress_bar=True)

# XTTS Checkpoints
TOKENIZER_FILE_LINK = "https://coqui.gateway.scarf.sh/hf-coqui/XTTS-v1/v1.1.2/vocab.json"
XTTS_CHECKPOINT_LINK = "https://coqui.gateway.scarf.sh/hf-coqui/XTTS-v1/v1.1.2/model.pth"

TOKENIZER_FILE = os.path.join(CHECKPOINTS_OUT_PATH, TOKENIZER_FILE_LINK.split("/")[-1])
XTTS_CHECKPOINT = os.path.join(CHECKPOINTS_OUT_PATH, XTTS_CHECKPOINT_LINK.split("/")[-1])

if not os.path.isfile(TOKENIZER_FILE) or not os.path.isfile(XTTS_CHECKPOINT):
    print(" > Downloading XTTS v1.1 files!")
    ModelManager._download_model_files([TOKENIZER_FILE_LINK, XTTS_CHECKPOINT_LINK], CHECKPOINTS_OUT_PATH, progress_bar=True)

# Training sentences generations (Portuguese example)
SPEAKER_REFERENCE = None  # Not needed if each audio corresponds to a different speaker
LANGUAGE = config_dataset.language

torch.cuda.empty_cache()

def main():
    # Initialize model arguments and config
    model_args = GPTArgs(
        max_conditioning_length=132300,
        min_conditioning_length=66150,
        max_wav_length=255995,
        max_text_length=200,
        mel_norm_file=MEL_NORM_FILE,
        dvae_checkpoint=DVAE_CHECKPOINT,
        xtts_checkpoint=XTTS_CHECKPOINT,
        tokenizer_file=TOKENIZER_FILE,
        gpt_num_audio_tokens=8194,
        gpt_start_audio_token=8192,
        gpt_stop_audio_token=8193,
    )
    
    # Define audio configuration
    audio_config = XttsAudioConfig(sample_rate=22050, dvae_sample_rate=22050, output_sample_rate=24000)

    # Training parameters config
    config = GPTTrainerConfig(
        output_path=OUT_PATH,
        model_args=model_args,
        run_name=RUN_NAME,
        project_name=PROJECT_NAME,
        audio=audio_config,
        batch_size=BATCH_SIZE,
        batch_group_size=48,
        eval_batch_size=BATCH_SIZE,
        num_loader_workers=8,
        eval_split_max_size=256,
        print_step=50,
        plot_step=100,
        log_model_step=1000,
        save_step=10000,
        save_n_checkpoints=1,
        save_checkpoints=True,
        phoneme_language="pt-PT",
        phonemizer="espeak",
        use_phonemes=True,
        optimizer="AdamW",
        optimizer_wd_only_on_weights=OPTIMIZER_WD_ONLY_ON_WEIGHTS,
        optimizer_params={"betas": [0.9, 0.96], "eps": 1e-8, "weight_decay": 1e-2},
        lr=5e-06,
        lr_scheduler="MultiStepLR",
        lr_scheduler_params={"milestones": [50000 * 18, 150000 * 18, 300000 * 18], "gamma": 0.5},
    )

    # Load training samples from metadata.txt
    train_samples, eval_samples = load_tts_samples(
        DATASETS_CONFIG_LIST,
        eval_split=True,
        eval_split_max_size=config.eval_split_max_size,
        eval_split_size=config.eval_split_size,
    )

    # Assign unique speaker IDs to each audio file
    for i, sample in enumerate(train_samples):
        sample['speaker_id'] = f"speaker_{i + 1}"

    # Initialize the model
    model = GPTTrainer.init_from_config(config)

    trainer = Trainer(
    TrainerArgs(
        restore_path=None,
        skip_train_epoch=False,
        start_with_eval=START_WITH_EVAL,
        grad_accum_steps=GRAD_ACUMM_STEPS,  # Accumulate gradients
    ),
    config,
    output_path=OUT_PATH,
    model=model,
    train_samples=train_samples,
    eval_samples=eval_samples,
    )


    # Start training
    trainer.fit()

if __name__ == "__main__":
    main()
