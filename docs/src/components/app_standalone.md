## Intlex Standalone Module

The Intlex Module serves as the standalone implementation of the text-to-speech system, allowing users to directly process text and generate audio files without using the microservices architecture. It provides flexibility for single-instance use cases.

### Usage

To use the Intlex Module, you can run the following command:

```bash
python intlex.py [TEXT] [CONFIG] --output [OUTPUT] --lang [LANG] --kwargs [KWARGS]
```

The output will be saved in the output file if provided, otherwise it will be stored in the default output file.

#### Arguments and Options

- `TEXT`: Text to be synthesized (required)
- `CONFIG`: Configuration file (optional)
- `OUTPUT`: Output file (optional)
- `LANG`: Language [pt, en] (optional)
- `KWARGS`: Additional arguments (optional)

#### Options:

##### Configuration File

The configuration file contains the settings for the synthesis process, such as the voice to clone, model information and configuration. If not provided, the default configuration will be used.

```json
{
  "normalization_config": "config/normalization_rules.toml",
  "audio_path": {
    "pt": "inputs/voices/marcelo.wav",
    "en": "inputs/voices/eng_morgan_freeman.wav"
  },
  "storage_directory": "inputs/voices",
  "xtts_config": "model/training/GPT_XTTS_Finetuned/config.json",
  "model": {
    "checkpoint_dir": null,
    "eval": true,
    "strict": true,
    "speaker_file_path": null,
    "checkpoint_path": "model/training/GPT_XTTS_Finetuned/best_model.pth",
    "vocab_path": "model/training/XTTS_v2.0_original_model_files/vocab.json",
    "use_deepspeed": false
  }
}
```

Each field in the configuration file is described below:

- `normalization_config`: Path to the normalization configuration file to be used by the model

- `audio_path`: Default input voices for conversion, the field is a dictionary with the keys being the voices' languages and the values being the paths to the audio files

  - `pt`: Path to the Portuguese reference audio file
  - `en`: Path to the English reference audio file

- `storage_directory`: Path to the folder where the reference audio files are stored

- `xtts_config`: Path to the XTTS configuration file to be used by the trained model

- `model`: Model configuration to be used for conversion, the fields are according to the trained model to facilitate configuration
  - `checkpoint_dir`: Path to the directory where the model checkpoints are stored
  - `eval`: Whether the model is in evaluation mode
  - `strict`: Whether to strictly enforce the model configuration
  - `speaker_file_path`: Path to the file containing the speaker information
  - `checkpoint_path`: Path to the model checkpoint file
  - `vocab_path`: Path to the vocabulary file
  - `use_deepspeed`: Whether to use DeepSpeed for training

##### Language

The language option allows the user to specify the language of the text to be synthesized. The available languages are:

- `pt`: Portuguese
- `en`: English

The model suports more languages, but the available voices are only in Portuguese and English. If the user wants to use another language, they must provide the voice file and update the configuration file accordingly.

##### Additional Arguments for the voice synthesis

The `kwargs` option allows the user to specify additional arguments for the voice synthesis process. The available arguments are:

- `length_penalty`: Length penalty for the synthesis process
- `repetition_penalty`: Repetition penalty for the synthesis process
- `top_k`: Top k tokens to consider for the synthesis process
- `top_p`: Top p tokens to consider for the synthesis process
- `do_sample`: Whether to sample the tokens
- `temperature`: Temperature for the sampling process

The default values for the additional arguments are:

```json
{
  "length_penalty": 1.0,
  "repetition_penalty": 2.5,
  "top_k": 40,
  "top_p": 0.5,
  "do_sample": true,
  "temperature": 0.7
}
```

The format for the `kwargs` option is a dictionary with the keys being the argument names and the values being the argument values.

```bash
py intlex.py TEXT --kwargs '{"temperature":0.01,"top_p":0.4,"top_k":60}'
```

This will set the temperature to 0.01, top_p to 0.4 and top_k to 60.

### Example

To synthesize the text "Hello, World!" in English, you can run the following command:

```bash
python intlex.py "Hello, World!" --lang en
```

This will generate an audio file with the synthesized speech in English.

