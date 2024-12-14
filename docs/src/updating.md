# Updating

## Model training

The `xtts_v2_pt_colab_pro_notebook.ipynb` notebook is a comprehensive script designed for fine-tuning and training the XTTS (Extended Text-to-Speech) model. It is structured for execution in Google Colab or locally, leveraging a dataset in the LJSpeech format and integrating with the Coqui TTS framework for model training and management.

## Dataset Format

The XTTS training process requires the dataset to be structured following the **LJSpeech format**, adapted for single-speaker audio data. Below is a detailed explanation of the format and its requirements.

### Directory Structure

The dataset should follow this structure:

```
dataset
├── metadata.csv
└── wavs
    ├── audio_0.wav
    ├── audio_1.wav
    ├── audio_2.wav
    ├── audio_3.wav
    ├── audio_4.wav
    ├── audio_5.wav
    ├── audio_6.wav
    ├── audio_7.wav
    ├── audio_8.wav
    ├── audio_9.wav
    └── audio_N.wav
```

### Components

1. **`metadata.csv`**
   - A CSV file that maps each audio file to its corresponding text transcription.
   - Format: Each row contains:
     - `filename` (without extension): The name of the audio file.
     - `transcription`: The text spoken in the audio file.
     - `normalizer transcription`: The text spoken in the audio file.
     - Example:
       ```csv
       audio_0|Hello, welcome to the XTTS training system.|Hello, welcome to the XTTS training system.
       audio_1|This is an example of a training sentence with numbers 12345.| This is an example of a training sentence with numbers one two three four five.
       audio_n|High-quality audio is essential for better results.|High-quality audio is essential for better results.
       ```
   - The delimiter is a pipe (`|`).

2. **`wavs/` Directory**
   - Contains all audio files in **WAV format**.
   - Requirements:
     - Sampling rate: **22,050 Hz** (recommended).
     - Single-channel (mono) audio.
     - Bit depth: **16-bit** PCM encoding.

### <span style="color:RED">Requirements for Training </span>

- The dataset must consist of:
  - <span style="color:RED">**Single Speaker**</span>: All audio recordings must originate from the same speaker to ensure consistency in the model's output.
  - **Clear Transcriptions**: Text transcriptions should accurately match the spoken content in the audio files. Any incorrectly text matched will "Poison" the model.
- Audio file naming should correspond to the `filename` column in the `metadata.csv` file.

### Example Dataset Entry

For the dataset structure shown above, the `metadata.csv` might look like this:

```csv
audio_0|Hello, welcome to the XTTS training system.|Hello, welcome to the XTTS training system.
audio_1|This is an example of a training sentence with numbers 12345.| This is an example of a training sentence with numbers one two three four five.
audio_n|High-quality audio is essential for better results.|High-quality audio is essential for better results.
```

### Notes

- Ensure all filenames and paths are consistent between `metadata.csv` and the audio files.
- Verify the audio quality and transcriptions for best results during training.
- If using a dataset in another format, preprocess it into this structure before starting training.


## File Structure and Execution Flow

### 1. **Environment Setup**
   - **Dependency Installation**:
     - Installs necessary tools:
       - `espeak-ng`: For phoneme generation in Portuguese.
       - `ffmpeg`: For audio processing.
     - Clones and installs the Coqui TTS repository to provide training utilities.
     - Ensures all dependencies are installed with pip.
   - **Environment Variables**:
     - Defines key dataset and model paths:
       ```python
       DATASET_URL = "http://mayorx.xyz/Media/agentifai/podcast_dataset.zip"
       DATASET_PATH = "podcast_dataset.zip"
       DATASET_DIR = "dataset/"
       DATASET_NAME = "bitalk_podcast"
       DATASET_LANG = "pt"
       ```

### 2. **Dataset Management**
   - **Dataset Download and Preparation**:
     - Fetches the dataset from a predefined URL and extracts it into a structured directory.
     - Supports single-speaker datasets formatted similarly to LJSpeech:
       - WAV audio files.
       - Corresponding metadata with text transcripts.
   - **Input Voice Configuration**:
     - Allows downloading or setting input voices for use during fine-tuning.
   - Commands used:
     ```bash
     wget $DATASET_URL -O $DATASET_PATH
     unzip $DATASET_PATH
     rm $DATASET_PATH
     ```

### 3. **Model Configuration**
   - **Trainer Setup**:
     - Imports and configures `Trainer` and `TrainerArgs` from Coqui TTS to manage the training process.
     - Defines `BaseDatasetConfig` to specify dataset properties.
   - **Logging and Checkpoints**:
     - Logs training progress using TensorBoard.
     - Saves model checkpoints to a defined directory.

   - Sample Configuration:
     ```python
     RUN_NAME = "XTTS_FineTuned"
     PROJECT_NAME = "XTTS_trainer"
     DASHBOARD_LOGGER = "tensorboard"
     CHECKPOINT_DIR = "./checkpoints"
     ```

### 4. **Training Execution**
   - Executes the training loop with Coqui TTS, fine-tuning the model based on the specified dataset.
   - Allows flexibility in hyperparameters for optimization.

### 5. **Output**
   - **Model Artifacts**:
     - Fine-tuned XTTS model saved in the checkpoint directory.
   - **Logs**:
     - Training metrics and progress logged for monitoring via TensorBoard.

---

## Prerequisites

### Hardware
- **GPU Required**: A CUDA-enabled GPU is strongly recommended for efficient training.

### Software
- Python 3.x.
- Necessary Python packages installed:
  - `espeak-ng`
  - `ffmpeg`
  - `torch`, `numpy`, and other dependencies via Coqui TTS.

### Dataset
- A dataset formatted similarly to LJSpeech:
  - Audio files in WAV format.
  - A metadata file containing transcripts for each audio file.

---

## Usage Instructions

1. **Setup Environment**:
   - Install the required dependencies by running the notebook's initial cells.

2. **Download Dataset**:
   - Provide a dataset URL or manually place your dataset in the `dataset/` directory.

3. **Configure Training**:
   - Adjust the training parameters in the notebook as needed:
     - Dataset path.
     - Checkpoint directory.
     - Logging options.

4. **Run Training**:
   - Execute the training cells sequentially.

5. **Monitor Progress**:
   - Use TensorBoard to visualize training metrics.

6. **Save and Deploy**:
   - Use the final model checkpoint for deployment or further evaluation.
