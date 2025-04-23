import os
import sys
import time
import whisperx
import torch
from config import (
    MODEL_SIZE,
    DEVICE,
    COMPUTE_TYPE,
    SHOW_TIMESTAMPS,
    BEAM_SIZE,
    OUTPUT_FILE
)
from pathlib import Path
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn

console = Console()

def transcribe_audio(input_file: str) -> str:
    """
    Transcribe an audio file using WhisperX model.
    
    Args:
        input_file: Path to the input audio file
    
    Returns:
        str: Path to the generated transcript file
    """
    # Initialize model with config settings
    model = whisperx.load_model(
        MODEL_SIZE,
        device=DEVICE,
        compute_type=COMPUTE_TYPE,
        download_root=None
    )

    # Load audio
    audio = whisperx.load_audio(input_file)
    
    # Transcribe with original whisper
    result = model.transcribe(audio, batch_size=BEAM_SIZE)
    language = result["language"]
    
    # Print language info to console
    console.print(f"\n🌐 [bold blue]Detected language:[/bold blue] {language}")
    console.print("\n📝 [bold blue]Transcription progress:[/bold blue]")

    # Load alignment model
    model_a, metadata = whisperx.load_align_model(
        language_code=language,
        device=DEVICE
    )

    # Align whisper output
    result = whisperx.align(
        result["segments"],
        model_a,
        metadata,
        audio,
        DEVICE,
        return_char_alignments=False
    )

    # Determine output file path
    if OUTPUT_FILE:
        output_file = OUTPUT_FILE
    else:
        input_path = Path(input_file)
        output_file = str(input_path.with_suffix('.txt'))

    # Open file for writing with unbuffered I/O
    with open(output_file, "w", encoding="utf-8", buffering=1) as f:
        # Write language information
        f.write(f"Detected language: {language}\n\n")
        os.fsync(f.fileno())  # Force write to disk

        # Process each segment with progress bar
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            console=console
        ) as progress:
            task = progress.add_task("Transcribing...", total=len(result["segments"]))
            
            for i, segment in enumerate(result["segments"], 1):
                # Format the segment text based on timestamp setting
                if SHOW_TIMESTAMPS:
                    segment_text = f"[{segment['start']:.2f}s -> {segment['end']:.2f}s] {segment['text']}"
                else:
                    segment_text = segment['text']
                
                # Write to file immediately
                f.write(f"{segment_text}\n")
                os.fsync(f.fileno())  # Force write to disk
                
                # Update progress
                progress.update(task, advance=1)
                
                # Print the segment text after processing
                console.print(f"\n{segment_text}")
                
                # Small delay to ensure file system updates
                time.sleep(0.1)

    # Clean up GPU memory
    del model
    del model_a
    torch.cuda.empty_cache()

    return output_file

def main():
    """Entry point when running this file directly."""
    # Get input file from command line if provided
    input_file = sys.argv[1] if len(sys.argv) > 1 else None
    
    if not input_file:
        console.print("❌ [bold red]Error:[/bold red] Input file path is required when running transcribe.py directly")
        console.print("Usage: python transcribe.py <input_file>")
        sys.exit(1)
    
    transcribe_audio(input_file)

# Only run main() if this file is executed directly
if __name__ == "__main__":
    main()