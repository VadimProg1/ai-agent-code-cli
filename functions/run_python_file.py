import os
import subprocess

def run_python_file(working_directory, file_path, args=None):
    if not isinstance(file_path, str) or len(file_path) == 0 or file_path.isspace():
        f'Error: "{file_path}" is not a valid string'
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file_abs = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_target_file_path = os.path.commonpath([working_dir_abs, target_file_abs]) == working_dir_abs
        if valid_target_file_path == False:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_file_abs):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not target_file_abs.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", target_file_abs]
        if args != None and len(args) > 0:
            command.extend(args)
        process = subprocess.run(command, cwd=working_dir_abs, capture_output=True, text=True, timeout=30)

        result = ""
        if process.returncode != 0:
            result += f"Process exited with code {process.returncode}\n"
        
        if len(process.stdout) > 0:
            result += f'STDOUT: {process.stdout}\n'
        else:
            result += "STDOUT: No output produced\n"

        if len(process.stderr) > 0:
            result += f'STDERR: {process.stderr}'
        else:
            result += "STDERR: No output produced"
        return result
    except Exception as e:
        return f"Error: executing Python file: {e}"
        