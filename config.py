import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Model settings
MODEL_SIZE = os.getenv('MODEL_SIZE')
DEVICE = os.getenv('DEVICE')
COMPUTE_TYPE = os.getenv('COMPUTE_TYPE')

# Output settings
SHOW_TIMESTAMPS = os.getenv('SHOW_TIMESTAMPS', 'false').lower() == 'true'

# Determine output file path
if os.getenv('OUTPUT_FILE'):
    # Use environment variable if set
    OUTPUT_FILE = os.getenv('OUTPUT_FILE')
else:
    # This will be set after we get the input file
    OUTPUT_FILE = None

# Transcription settings
BEAM_SIZE = int(os.getenv('BEAM_SIZE', '5')) 