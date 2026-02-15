import os

def write_file(working_directory, file_path, content):
    if not isinstance(file_path, str) or len(file_path) == 0 or file_path.isspace():
        f'Error: "{file_path}" is not a valid string'
    
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file_abs = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_target_file_path = os.path.commonpath([working_dir_abs, target_file_abs]) == working_dir_abs
        if valid_target_file_path == False:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        if os.path.isdir(target_file_abs):
            return f'Error: Cannot write to "{file_path}" as it is a directory'
        
        dir_of_target_file = os.path.normpath(os.path.join(target_file_abs, ".."))
        os.makedirs(dir_of_target_file, exist_ok=True)
        with open(target_file_abs, "w") as f:
            f.write(content)
            return (f'Successfully wrote to "{file_path}" ({len(content)} characters written)')
    except Exception as e:
        return f'Error: {e}'