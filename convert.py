import os
import sys
from pathlib import Path
import ffmpeg
from typing import Tuple
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn

console = Console()

def convert_to_mp3(input_file: str, input_format: str) -> str:
    """
    Convert an audio/video file to MP3 format if needed.
    
    Args:
        input_file: Path to the input file
        input_format: Format of the input file (e.g., 'mp3', 'webm', 'wav')
    
    Returns:
        str: Path to the MP3 file (same as input if already MP3)
    
    Raises:
        RuntimeError: If conversion fails
    """
    # If input is already MP3, return the same file
    if input_format.lower() == 'mp3':
        return input_file
    
    # Create output path by changing extension to .mp3
    input_path = Path(input_file)
    output_file = str(input_path.with_suffix('.mp3'))
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        console=console
    ) as progress:
        task = progress.add_task("Converting...", total=100)
        
        try:
            # Try using ffmpeg-python first
            stream = ffmpeg.input(input_file)
            stream = ffmpeg.output(stream, output_file, acodec='libmp3lame', audio_bitrate='192k')
            ffmpeg.run(stream, overwrite_output=True, quiet=True)
            progress.update(task, completed=100)
        except ffmpeg.Error as e:
            console.print(f"⚠️ [bold yellow]ffmpeg-python failed:[/bold yellow] {e.stderr.decode()}")
            # Fallback to system ffmpeg command
            cmd = f'ffmpeg -i "{input_file}" -acodec libmp3lame -ab 192k "{output_file}" -y'
            if os.system(cmd) != 0:
                progress.update(task, completed=0)
                raise RuntimeError("Failed to convert file to MP3 format")
            progress.update(task, completed=100)
    
    return output_file

def main():
    """Entry point when running this file directly."""
    if len(sys.argv) < 3:
        console.print("❌ [bold red]Error:[/bold red] Usage: python convert.py <input_file> <input_format>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    input_format = sys.argv[2]
    convert_to_mp3(input_file, input_format)

if __name__ == "__main__":
    main() 