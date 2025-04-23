# Voice Transcription Pipeline

A powerful pipeline for transcribing audio and video files using WhisperX, featuring automatic language detection, word-level alignment, and GPU acceleration.

## Features

- 🚀 Fast and accurate transcription using WhisperX
- 🌐 Automatic language detection
- ⚡ GPU acceleration support
- 🎯 Word-level alignment for precise timestamps
- 📝 Interactive input file selection
- 🔄 Automatic format conversion (using ffmpeg)
- 📊 Progress tracking and real-time output

## Prerequisites

- Python 3.8 or higher
- CUDA-capable GPU (recommended)
- ffmpeg installed on your system

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/voice-models.git
cd voice-models
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -e .
```

## Configuration

Create a `.env` file in the project root with the following options:

```env
# Model configuration
MODEL_SIZE=large-v2  # Options: tiny, base, small, medium, large-v1, large-v2
DEVICE=cuda  # Options: cuda, cpu
COMPUTE_TYPE=float16  # Options: float16, float32, int8

# Output settings
SHOW_TIMESTAMPS=true  # Show timestamps in output
OUTPUT_FILE=./transcript.txt  # Optional: specify output file path
BEAM_SIZE=5  # Number of beams for beam search
```

## Usage

Run the complete pipeline:
```bash
python pipeline.py
```

Or run individual tasks:
```bash
# Discover task
python discover.py

# Convert task
python convert.py input_file.webm

# Transcribe task
python transcribe.py input_file.mp3
```

## Output

The transcription will be saved in the same folder as the input file (unless specified otherwise in `.env`). The output format includes:

```
Detected language: en

[0.00s -> 2.50s] This is the first segment of transcribed text.
[2.50s -> 5.00s] This is the second segment of transcribed text.
...
```

## License

MIT License
