import os

def validate_and_create_abs_file_path(working_directory, file_path):
    if not isinstance(file_path, str) or len(file_path) == 0 or file_path.isspace():
        raise Exception(f'"{file_path}" is not a valid string')
    
    working_dir_abs = os.path.abspath(working_directory)
    target_file_abs = os.path.normpath(os.path.join(working_dir_abs, file_path))
    valid_target_file_path = os.path.commonpath([working_dir_abs, target_file_abs]) == working_dir_abs
    if valid_target_file_path == False:
        raise Exception(f'Cannot read "{file_path}" as it is outside the permitted working directory')
    if not os.path.isfile(target_file_abs):
        raise Exception(f'File not found or is not a regular file "{file_path}"')
    return target_file_abs