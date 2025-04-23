# Voice Models

A Python project for efficient speech-to-text transcription using the Whisper model.

## Overview

This project utilizes [faster-whisper](https://github.com/SYSTRAN/faster-whisper), an optimized implementation of OpenAI's Whisper model, to perform high-quality speech recognition. It's designed to run efficiently on both CPU and GPU environments.

## Features

- Fast and accurate speech-to-text transcription
- Support for multiple languages
- GPU acceleration with FP16 and INT8 precision options
- Timestamp generation for transcribed segments
- Language detection with probability scores
- Interactive input file selection
- Configurable through environment variables

## Prerequisites

- Python 3.10 or higher
- CUDA-compatible GPU (optional, for GPU acceleration)
- [uv](https://github.com/astral-sh/uv) package manager

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/voice-models.git
cd voice-models
```

2. Create and activate the virtual environment using uv:
```bash
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
uv pip install -e .
```

## Configuration

The project uses a `.env` file for configuration. Create a `.env` file with the following settings:

```env
# Model settings
MODEL_SIZE=large-v3
DEVICE=cpu
COMPUTE_TYPE=int8

# Output settings
SHOW_TIMESTAMPS=false
# OUTPUT_FILE=./path/to/custom/output.txt

# Transcription settings
BEAM_SIZE=5
```

### Configuration Options

- `MODEL_SIZE`: Whisper model size ("tiny", "base", "small", "medium", "large-v1", "large-v2", "large-v3")
- `DEVICE`: Processing device ("cpu" or "cuda")
- `COMPUTE_TYPE`: Computation precision ("int8", "float16", or "int8_float16")
- `SHOW_TIMESTAMPS`: Whether to show timestamps in output (true/false)
- `OUTPUT_FILE`: Optional custom output file path
- `BEAM_SIZE`: Beam size for transcription (default: 5)

## Usage

1. Run the script:
```bash
uv run main.py
```

2. When prompted, enter the full path to your audio file:
```
Please enter the full path to the input audio file: /path/to/your/audio.mp3
```

3. The script will:
   - Transcribe the audio file
   - Show progress in real-time
   - Create the transcript in the same directory as the input file (unless OUTPUT_FILE is specified)
   - Display the detected language and probability

## Output

The transcription will be saved to a text file in the same directory as the input file (with .txt extension) unless a custom output path is specified in the .env file.

Example output format:
```
Detected language: en (probability: 0.95)

[0.00s -> 2.50s] First segment text
[2.50s -> 5.00s] Second segment text
...
```

## License

[Add your license here]

## Contributing

[Add contribution guidelines here]
