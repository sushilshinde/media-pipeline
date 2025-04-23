# Voice Transcription Pipeline

A powerful and flexible pipeline for transcribing audio and video files using the faster-whisper library. This project provides a complete solution from file discovery to transcription, with support for various input formats and configuration options.

## Features

- **Multi-format Support**: Handles various audio and video formats (MP3, WEBM, WAV, etc.)
- **Automatic Format Conversion**: Converts non-MP3 files to MP3 format using ffmpeg
- **GPU Acceleration**: Supports CUDA for faster transcription
- **Interactive Input**: User-friendly file selection
- **Configurable Output**: Flexible output file location and format
- **Progress Tracking**: Real-time transcription progress display with fancy progress bars
- **Language Detection**: Automatic language detection with confidence scores
- **Timestamp Support**: Optional timestamps in the transcript
- **Modular Design**: Separate components for discovery, conversion, and transcription

## Prerequisites

- Python 3.10 or higher
- ffmpeg (for format conversion)
- CUDA-compatible GPU (optional, for faster processing)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/voice-models.git
   cd voice-models
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -e .
   ```

4. Install ffmpeg:
   - On macOS: `brew install ffmpeg`
   - On Ubuntu: `sudo apt-get install ffmpeg`
   - On Windows: Download from [ffmpeg.org](https://ffmpeg.org/download.html)

## Configuration

The project can be configured using a `.env` file. Create a `.env` file in the project root with the following options:

```env
# Model settings
MODEL_SIZE=large-v2  # Options: tiny, base, small, medium, large-v1, large-v2
DEVICE=cuda  # Options: cpu, cuda
COMPUTE_TYPE=float16  # Options: float16, float32, int8, int8_float16

# Output settings
SHOW_TIMESTAMPS=true  # Options: true, false
OUTPUT_FILE=/path/to/output.txt  # Optional, defaults to input file directory
BEAM_SIZE=5  # Higher values may improve accuracy but slow down processing
```

## Usage

### Running the Complete Pipeline

To transcribe an audio/video file:

```bash
python pipeline.py [input_file]
```

If no input file is provided, you'll be prompted to enter the path.

The pipeline will show detailed progress for each step:
```
🔍 Discovering file...
✅ File discovered: /path/to/input.webm (format: webm)

🔄 Converting WEBM to MP3...
[████████████████████████████████████████] 100%
✅ Conversion complete: /path/to/input.mp3

🎤 Starting transcription...
Detected language: en (probability: 0.95)
[████████████████████████████████████████] 100%
✅ Transcription complete: /path/to/input.txt
```

### Running Individual Components

1. **Discover Task**:
   ```bash
   python discover.py
   ```

2. **Convert Task**:
   ```bash
   python convert.py input_file format
   ```

3. **Transcribe Task**:
   ```bash
   python transcribe.py input_file
   ```

## Output

The pipeline generates a transcript file in the same directory as the input file (unless specified otherwise in the `.env` file). The output includes:

- Detected language and confidence score
- Transcription with optional timestamps
- Progress updates during processing

Example output:
```
Detected language: en (probability: 0.95)

[0.00s -> 2.50s] Hello, this is a test recording.
[2.50s -> 5.00s] I'm testing the transcription pipeline.
```

## Project Structure

```
voice-models/
├── pipeline.py      # Main pipeline orchestrator
├── discover.py      # File discovery and validation
├── convert.py       # Format conversion
├── transcribe.py    # Transcription using faster-whisper
├── config.py        # Configuration management
├── .env            # Environment variables (optional)
└── README.md       # This file
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
