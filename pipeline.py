import sys
import time
from typing import Optional
from discover import discover_file
from convert import convert_to_mp3
from transcribe import transcribe_audio
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from datetime import datetime, timedelta

console = Console()

def format_time(seconds: float) -> str:
    """Format time duration in a human-readable format."""
    duration = timedelta(seconds=seconds)
    hours = duration.seconds // 3600
    minutes = (duration.seconds % 3600) // 60
    seconds = duration.seconds % 60
    milliseconds = duration.microseconds // 1000

    if hours > 0:
        return f"{hours}h {minutes}m {seconds}s"
    elif minutes > 0:
        return f"{minutes}m {seconds}s"
    elif seconds > 0:
        return f"{seconds}.{milliseconds:03d}s"
    else:
        return f"{milliseconds}ms"

def run_pipeline(input_file: Optional[str] = None) -> str:
    """
    Run the complete pipeline: Discover -> Convert -> Transcribe.
    
    Args:
        input_file: Optional path to the input file. If not provided,
                   the user will be prompted to enter it.
    
    Returns:
        str: Path to the generated transcript file
    """
    pipeline_start = time.time()
    
    # Task 1: Discover file
    console.print("\n🔍 [bold blue]Discovering file...[/bold blue]")
    discover_start = time.time()
    input_file, input_format = discover_file(input_file)
    discover_time = time.time() - discover_start
    console.print(f"✅ [bold green]File discovered:[/bold green] {input_file} (format: {input_format})")
    console.print(f"⏱️  [bold yellow]Time taken:[/bold yellow] {format_time(discover_time)}")
    
    # Task 2: Convert to MP3 if needed
    convert_time = 0
    if input_format.lower() != 'mp3':
        console.print("\n🔄 [bold blue]Converting to MP3...[/bold blue]")
        convert_start = time.time()
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            console=console
        ) as progress:
            task = progress.add_task("Converting...", total=100)
            mp3_file = convert_to_mp3(input_file, input_format)
            progress.update(task, completed=100)
        convert_time = time.time() - convert_start
        console.print(f"✅ [bold green]Conversion complete:[/bold green] {mp3_file}")
        console.print(f"⏱️  [bold yellow]Time taken:[/bold yellow] {format_time(convert_time)}")
    else:
        mp3_file = input_file
    
    # Task 3: Transcribe
    console.print("\n🎤 [bold blue]Starting transcription...[/bold blue]")
    try:
        transcribe_start = time.time()
        transcript_file = transcribe_audio(mp3_file)
        transcribe_time = time.time() - transcribe_start
        
        # Calculate total pipeline time
        total_time = time.time() - pipeline_start
        
        # Print timing summary
        console.print("\n📊 [bold blue]Pipeline Summary:[/bold blue]")
        console.print(f"├── Discovery: {format_time(discover_time)}")
        if convert_time > 0:
            console.print(f"├── Conversion: {format_time(convert_time)}")
        console.print(f"├── Transcription: {format_time(transcribe_time)}")
        console.print(f"└── [bold green]Total Time: {format_time(total_time)}[/bold green]")
        
        console.print(f"\n✅ [bold green]Pipeline completed. Transcript saved to:[/bold green] {transcript_file}")
        return transcript_file
    except Exception as e:
        console.print(f"❌ [bold red]Error during transcription:[/bold red] {e}")
        raise

if __name__ == "__main__":
    # Get input file from command line if provided
    input_file = sys.argv[1] if len(sys.argv) > 1 else None
    run_pipeline(input_file) 