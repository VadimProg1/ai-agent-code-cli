from config import MAX_CHARS_TO_READ
from functions.utils import validate_and_create_abs_file_path
from google.genai import types

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Gets contents of a file in a specified file path relative to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path of the file to get contents from. Relative to the working directory",
            ),
        },
        required=["file_path"]
    ),
)

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