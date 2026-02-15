from config import MAX_CHARS_TO_READ
from functions.utils import validate_and_create_abs_file_path

def get_file_content(working_directory, file_path):    
    try:
        target_file_abs = validate_and_create_abs_file_path(working_directory, file_path)
        file_content = ""
        with open(target_file_abs, "r") as f:
            file_content = f.read(MAX_CHARS_TO_READ)
            if len(f.read(1)) > 0:
                file_content += f'[...File "{file_path}" truncated at {MAX_CHARS_TO_READ} characters]'
        return file_content 
    except Exception as e:
        return f'Error: {e}'