import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_input_file():
    """Prompt user for input file path"""
    while True:
        input_file = input("Please enter the full path to the input audio file: ").strip()
        if os.path.isfile(input_file):
            return input_file
        print(f"Error: File not found at '{input_file}'. Please try again.")

# Model settings
MODEL_SIZE = os.getenv('MODEL_SIZE')
DEVICE = os.getenv('DEVICE')
COMPUTE_TYPE = os.getenv('COMPUTE_TYPE')

# Output settings
SHOW_TIMESTAMPS = os.getenv('SHOW_TIMESTAMPS', 'false').lower() == 'true'
INPUT_FILE = get_input_file()

# Determine output file path
if os.getenv('OUTPUT_FILE'):
    # Use environment variable if set
    OUTPUT_FILE = os.getenv('OUTPUT_FILE')
else:
    # Create output in same directory as input file
    input_path = Path(INPUT_FILE)
    OUTPUT_FILE = str(input_path.with_suffix('.txt'))

# Transcription settings
BEAM_SIZE = int(os.getenv('BEAM_SIZE', '5')) 