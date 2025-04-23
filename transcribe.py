import os
import sys
import time
from faster_whisper import WhisperModel
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
    Transcribe an audio file using Whisper model.
    
    Args:
        input_file: Path to the input audio file
    
    Returns:
        str: Path to the generated transcript file
    """
    # Initialize model with config settings
    model = WhisperModel(MODEL_SIZE, device=DEVICE, compute_type=COMPUTE_TYPE)

    # Print language info to console
    segments, info = model.transcribe(input_file, beam_size=BEAM_SIZE)
    console.print(f"\n🌐 [bold blue]Detected language:[/bold blue] {info.language} (probability: {info.language_probability:.2f})")
    console.print("\n📝 [bold blue]Transcription progress:[/bold blue]")

    # Determine output file path
    if OUTPUT_FILE:
        output_file = OUTPUT_FILE
    else:
        input_path = Path(input_file)
        output_file = str(input_path.with_suffix('.txt'))

    # Open file for writing with unbuffered I/O
    with open(output_file, "w", encoding="utf-8", buffering=1) as f:
        # Write language information
        f.write(f"Detected language: {info.language} (probability: {info.language_probability:.2f})\n\n")
        os.fsync(f.fileno())  # Force write to disk

        # Process each segment with progress bar
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            console=console
        ) as progress:
            task = progress.add_task("Transcribing...", total=len(list(segments)))
            
            for i, segment in enumerate(segments, 1):
                # Format the segment text based on timestamp setting
                if SHOW_TIMESTAMPS:
                    segment_text = f"[{segment.start:.2f}s -> {segment.end:.2f}s] {segment.text}"
                else:
                    segment_text = segment.text
                
                # Write to file immediately
                f.write(f"{segment_text}\n")
                os.fsync(f.fileno())  # Force write to disk
                
                # Update progress
                progress.update(task, advance=1)
                
                # Print the segment text after processing
                console.print(f"\n{segment_text}")
                
                # Small delay to ensure file system updates
                time.sleep(0.1)

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