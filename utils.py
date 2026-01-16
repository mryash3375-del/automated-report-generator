import os
import datetime

def ensure_dir(directory):
    """Ensures that a directory exists."""
    if not os.path.exists(directory):
        os.makedirs(directory)

def get_timestamp_filename(prefix="report", extension="pdf"):
    """Generates a filename with a timestamp."""
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{prefix}_{timestamp}.{extension}"

def validate_file_extension(filename, allowed_extensions={'csv', 'xlsx', 'xls', 'json'}):
    """Validates if the file has an allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions
