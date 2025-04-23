from faster_whisper import WhisperModel
import sys
import os
import time
from config import (
    MODEL_SIZE,
    DEVICE,
    COMPUTE_TYPE,
    SHOW_TIMESTAMPS,
    INPUT_FILE,
    OUTPUT_FILE,
    BEAM_SIZE
)

# Initialize model with config settings
model = WhisperModel(MODEL_SIZE, device=DEVICE, compute_type=COMPUTE_TYPE)

print("Starting transcription...")
segments, info = model.transcribe(INPUT_FILE, beam_size=BEAM_SIZE)

# Print language info to console
print(f"\nDetected language: {info.language} (probability: {info.language_probability:.2f})")
print("\nTranscription progress:")

# Open file for writing with unbuffered I/O
with open(OUTPUT_FILE, "w", encoding="utf-8", buffering=1) as f:
    # Write language information
    f.write(f"Detected language: {info.language} (probability: {info.language_probability:.2f})\n\n")
    os.fsync(f.fileno())  # Force write to disk

    # Process each segment
    for i, segment in enumerate(segments, 1):
        # Format the segment text based on timestamp setting
        if SHOW_TIMESTAMPS:
            segment_text = f"[{segment.start:.2f}s -> {segment.end:.2f}s] {segment.text}"
        else:
            segment_text = segment.text
        
        # Write to file immediately
        f.write(f"{segment_text}\n")
        os.fsync(f.fileno())  # Force write to disk
        
        # Show progress on console
        sys.stdout.write(f"\rProcessing segment {i}...")
        sys.stdout.flush()
        
        # Print the segment text after processing
        print(f"\n{segment_text}")
        
        # Small delay to ensure file system updates
        time.sleep(0.1)

print(f"\n\nTranscription completed and saved to {OUTPUT_FILE}")