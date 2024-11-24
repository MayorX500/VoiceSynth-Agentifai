#!/bin/bash

# Default values
python_script='intlex.py'
laptop='False'
text=''
config=''
lang=''
voice=''
output=''

print_usage() {
  printf "Usage: ./run.sh -t text [-l] [-g language] [-v voice_path] [-o output_path] [-h]\n"
  printf "Options:\n"
  printf "\t  -t text\t\tText to convert to speech (required)\n"
  printf "\t  -c config_path\tConfig path (required)\n"
  printf "\t  -l\t\t\tUse prime-run for laptops with nvidia gpu\n"
  printf "\t  -g language\t\tLanguage code (optional)\n"
  printf "\t  -o output_path\tOutput path (optional)\n"
  printf "\t  -h\t\t\tPrint usage\n"
}

# Parse command line options
while getopts ':lt:c:g:v:o:h' flag; do
  case "${flag}" in
    l) laptop='True' ;;  # Set laptop to True if -l is provided
    t) text="${OPTARG}" ;;  # Text is required, stored in text variable
	c) config="${OPTARG}" ;;  # Config is required, stored in config variable
    g) lang="${OPTARG}" ;;
    v) voice="${OPTARG}" ;;
    o) output="${OPTARG}" ;;
    h) print_usage
       exit 0 ;;
    :) echo "Error: Option -${OPTARG} requires an argument."
       print_usage
       exit 1 ;;
    *) print_usage
       exit 1 ;;
  esac
done

# Ensure that the required text argument is provided
if [ -z "$text" ]; then
  echo "Error: The -t option (text) is required."
  print_usage
  exit 1
fi
# Ensure that the required text argument is provided
if [ -z "$config" ]; then
  echo "Error: The -c option (config) is required."
  print_usage
  exit 1
fi


check_python() {
	## Check if python3 is installed
	if ! command -v python3 &> /dev/null; then
		echo "Python3 is not installed on your system. Please install it and try again."
		exit 1
	fi
}

create_enviroment() {
	## Create a python enviroment and install the required packages
	python3 -m venv .env
	source .env/bin/activate
	pip install -r enviroments/dev_requirements.txt
}



download_file() {
	## Download a file if it doesn't already exist
	local url=$1
	local destination=$2

	if [ -f "$destination" ]; then
		echo "File already exists: $destination"
	else
		echo "Downloading: $url"
		wget -q "$url" -O "$destination"
		if [ $? -eq 0 ]; then
			echo "Downloaded: $destination"
		else
			echo "Failed to download: $url"
		fi
	fi
}

create_dirs() {
	## Create directories if they don't exist
	mkdir -p inputs/voices
	mkdir -p model/run/training/XTTS_v2.0_original_model_files/
	mkdir -p model/run/training/GPT_XTTS_Finetuned/
}

download_files() {
	## Download files required for the model
	download_file "mayorx.xyz/Media/agentifai/input_voice.wav" "inputs/voices/input_voice.wav"
	download_file "https://huggingface.co/coqui/XTTS-v2/resolve/main/vocab.json" "model/run/training/XTTS_v2.0_original_model_files/vocab.json"
	download_file "mayorx.xyz/Media/agentifai/model/config.json" "model/run/training/GPT_XTTS_Finetuned/config.json"
	download_file "mayorx.xyz/Media/agentifai/model/best_model.pth" "model/run/training/GPT_XTTS_Finetuned/best_model.pth"
}

run_model() {

	## If laptop is set to True, run the model with prime-run (for laptops with nvidia gpu)
	if [ $laptop == "True" ]; then
		prime-run python3 "$python_script" "$text" "$config" ${lang:+--lang "$lang"} ${voice:+--voice "$voice"} ${output:+--output "$output"}
	else
		python3 "$python_script" "$text" "$config" ${lang:+--lang "$lang"} ${voice:+--voice "$voice"} ${output:+--output "$output"}
	fi
}



## function args laptop=(True/False Optional), text=(text to convert to speech), lang=(language code/optional), voice=(vocie path/optional), output=(output path/optional)
main() {
	## Check if python is installed
	check_python

	## Create directories
	create_dirs

	## Download files
	download_files

	## Check if the python enviroment exists
	if [ ! -d ".env" ]; then
		create_enviroment
	else
		source .env/bin/activate
	fi

	## Check if gpus are available
	if [ ! -z "$(nvidia-smi -L)" ]; then
		echo "GPU is available"
		export CUDA_VISIBLE_DEVICES=0
	else
		echo "GPU is not available"
	fi

	## Run the model
	run_model
}

main