#!/bin/bash

# Create necessary directories
mkdir -p inputs/voices
mkdir -p model/run/training/XTTS_v2.0_original_model_files/
mkdir -p model/run/training/GPT_XTTS_Finetuned/

# Function to download a file if it doesn't already exist
download_file() {
	local url=$1
	local destination=$2

	if [ -f "$destination" ]; then
		echo "File already exists: $destination"
	else
		wget -q "$url" -O "$destination"
		if [ $? -eq 0 ]; then
			echo "Downloaded: $destination"
		else
			echo "Failed to download: $url"
		fi
	fi
}

# Download the files
download_file "mayorx.xyz/Media/agentifai/input_voice.wav" "inputs/voices/input_voice.wav"
download_file "https://huggingface.co/coqui/XTTS-v2/resolve/main/vocab.json" "model/run/training/XTTS_v2.0_original_model_files/vocab.json"
download_file "mayorx.xyz/Media/agentifai/model/config.json" "model/run/training/GPT_XTTS_Finetuned/config.json"
download_file "mayorx.xyz/Media/agentifai/model/best_model.pth" "model/run/training/GPT_XTTS_Finetuned/best_model.pth"

source .env/bin/activate

prime-run python intlex.py
