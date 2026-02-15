import os
from config import MAX_CHARS_TO_READ

def get_file_content(working_directory, file_path):
    if not isinstance(file_path, str) or len(file_path) == 0 or file_path.isspace():
        f'Error: "{file_path}" is not a valid string'
    
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file_abs = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_target_file_path = os.path.commonpath([working_dir_abs, target_file_abs]) == working_dir_abs
        if valid_target_file_path == False:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if os.path.isdir(target_file_abs):
            return f'File not found or is not a regular file "{file_path}"'
        
        file_content = ""
        with open(target_file_abs, "r") as f:
            file_content = f.read(MAX_CHARS_TO_READ)
            if len(f.read(1)) > 0:
                file_content += f'[...File "{file_path}" truncated at {MAX_CHARS_TO_READ} characters]'
        return file_content 
    except Exception as e:
        return f'Error: {e}'