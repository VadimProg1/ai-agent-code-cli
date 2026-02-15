import os

def get_files_info(working_directory, directory="."):
    if not isinstance(directory, str) or len(directory) == 0 or directory.isspace():
        f'Error: "{directory}" is not a valid string'
    
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
        if valid_target_dir == False:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'
        
        formatted_contents_list = []
        for item_name in os.listdir(target_dir):
            abs_path_of_item = os.path.join(target_dir, item_name)
            file_size_formatted_str = f"file_size={os.path.getsize(abs_path_of_item)} bytes"
            is_dir_formatted_str = f"is_dir={os.path.isdir(abs_path_of_item)}"
            formatted_contents_list.append(f"- {item_name}: {file_size_formatted_str}, {is_dir_formatted_str}")
        return "\n".join(formatted_contents_list)
    except Exception as e:
        return f'Error: {e}'

    
