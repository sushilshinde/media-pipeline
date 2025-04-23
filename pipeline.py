import sys
from typing import Optional
from discover import discover_file
from convert import convert_to_mp3
from transcribe import transcribe_audio
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn

console = Console()

def run_pipeline(input_file: Optional[str] = None) -> str:
    """
    Run the complete pipeline: Discover -> Convert -> Transcribe.
    
    Args:
        input_file: Optional path to the input file. If not provided,
                   the user will be prompted to enter it.
    
    Returns:
        str: Path to the generated transcript file
    """
    # Task 1: Discover file
    console.print("\n🔍 [bold blue]Discovering file...[/bold blue]")
    input_file, input_format = discover_file(input_file)
    console.print(f"✅ [bold green]File discovered:[/bold green] {input_file} (format: {input_format})")
    
    # Task 2: Convert to MP3 if needed
    if input_format.lower() != 'mp3':
        console.print("\n🔄 [bold blue]Converting to MP3...[/bold blue]")
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
        console.print(f"✅ [bold green]Conversion complete:[/bold green] {mp3_file}")
    else:
        mp3_file = input_file
    
    # Task 3: Transcribe
    console.print("\n🎤 [bold blue]Starting transcription...[/bold blue]")
    try:
        # Pass the mp3_file directly to transcribe_audio
        transcript_file = transcribe_audio(mp3_file)
        console.print(f"✅ [bold green]Pipeline completed. Transcript saved to:[/bold green] {transcript_file}")
        return transcript_file
    except Exception as e:
        console.print(f"❌ [bold red]Error during transcription:[/bold red] {e}")
        raise

if __name__ == "__main__":
    # Get input file from command line if provided
    input_file = sys.argv[1] if len(sys.argv) > 1 else None
    run_pipeline(input_file) 