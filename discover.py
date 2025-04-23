import os
import sys
from pathlib import Path
from typing import Tuple, Optional
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn

console = Console()

def discover_file(input_file: Optional[str] = None) -> Tuple[str, str]:
    """
    Discover and validate the input file.
    
    Args:
        input_file: Optional path to the input file. If not provided,
                   the user will be prompted to enter it.
    
    Returns:
        Tuple[str, str]: (input_file_path, file_format)
    
    Raises:
        FileNotFoundError: If the file doesn't exist
        ValueError: If the file format cannot be determined
    """
    # If input_file is provided, validate it
    if input_file:
        if not os.path.isfile(input_file):
            raise FileNotFoundError(f"File not found: {input_file}")
    else:
        # Prompt for input file
        input_file = input("Please enter the full path to the input audio/video file: ").strip()
        if not os.path.isfile(input_file):
            raise FileNotFoundError(f"File not found: {input_file}")
    
    # Get file format from extension
    input_path = Path(input_file)
    file_format = input_path.suffix.lower().lstrip('.')
    
    if not file_format:
        raise ValueError(f"Could not determine file format for: {input_file}")
    
    return str(input_file), file_format

def main():
    """Entry point when running this file directly."""
    try:
        input_file, input_format = discover_file()
        console.print(f"✅ [bold green]Discovered file:[/bold green] {input_file} (format: {input_format})")
    except Exception as e:
        console.print(f"❌ [bold red]Error:[/bold red] {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 