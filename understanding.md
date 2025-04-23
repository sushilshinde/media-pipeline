# Project Understanding: Voice Models

## Overview

This project provides a modular pipeline for transcribing audio and video files using [WhisperX](https://github.com/m-bain/whisperX), with support for automatic language detection, word-level alignment, and optional GPU acceleration. The pipeline is designed for flexibility, user interaction, and robust progress reporting.

---

## Main Components

### 1. **discover.py**
- **Purpose:** Handles discovery and validation of the input file (audio/video).
- **Functionality:** 
  - Prompts the user for a file path if not provided.
  - Checks file existence and extracts the file format.

### 2. **convert.py**
- **Purpose:** Converts input files to MP3 format if needed.
- **Functionality:** 
  - Uses `ffmpeg-python` or system ffmpeg to convert various formats to MP3.
  - Skips conversion if already in MP3 format.

### 3. **transcribe.py**
- **Purpose:** Transcribes MP3 audio files using WhisperX.
- **Functionality:** 
  - Loads model configuration from `.env` or `config.py`.
  - Detects language, aligns words, and writes a transcript with optional timestamps.
  - Progress is shown via the `rich` library.

### 4. **pipeline.py**
- **Purpose:** Orchestrates the full pipeline: discover → convert → transcribe.
- **Functionality:** 
  - Runs each step in sequence, reporting progress and errors.
  - Returns the path to the generated transcript.

### 5. **config.py**
- **Purpose:** Loads configuration from environment variables or `.env` file.
- **Key Settings:** 
  - Model size, device, compute type, output file, timestamp display, beam size.

---

## Usage Flow

1. **Input Discovery:** User provides or is prompted for an audio/video file.
2. **Format Conversion:** File is converted to MP3 if not already.
3. **Transcription:** MP3 file is transcribed, with results saved to a text file.
4. **Output:** Transcript includes detected language and (optionally) timestamps.

---

## Key Technologies

- **WhisperX:** Fast, accurate speech-to-text with alignment.
- **PyTorch/TorchAudio:** Backend for model inference.
- **ffmpeg-python:** Audio/video format conversion.
- **rich:** Console output and progress bars.
- **python-dotenv:** Environment variable management.

---

## Configuration

- **.env file:** Used to override model/device/output settings.
- **config.py:** Loads and parses environment variables for use throughout the pipeline.

---

## Example Command

```bash
python pipeline.py /path/to/input/file.wav
```

---

## Output

- Transcript file (default: same name as input, `.txt` extension).
- Includes detected language and optionally timestamps for each segment.

---

## Extensibility

- Modular design: Each step (discover, convert, transcribe) can be run independently.
- Easy to add new formats or processing steps.

---

## References

- See [README.md](README.md) for installation and usage details.