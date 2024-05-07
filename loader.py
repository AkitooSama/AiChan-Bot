#Importing built-in modules.
from typing import List, Dict
import os
import json

def get_extensions(folder_end_with: str, file_extension: str, directory: str) -> List[str]:
    """
    Get a list of file extensions based on provided file types and directory.

    Args:
    - folder_end_with (str): The folder end-with to filter files in the directory.
    - file_extension (str): The secondary file extension to filter files within directories.
    - directory (str): The path of the main directory containing the folder->files.

    Returns:
    - List[str]: A list of file extensions based on the given criteria.
    """
    initial_extensions: List[str] = []
    
    folders = [folder for folder in os.listdir(directory) if folder.endswith(folder_end_with)]

    for folder in folders:
        folder_dir = os.path.join(directory, folder)
        py_files = [
            filename[:-3] for filename in os.listdir(folder_dir)
            if filename.endswith(file_extension)
        ]

        initial_extensions.extend([f"{folder}.{py_file}" for py_file in py_files])
    return initial_extensions

def load_config(file_path: str) -> Dict:
    """
    Load a JSON configuration file.

    Args:
    - file_path (str): The path of the JSON file to be loaded.

    Returns:
    - Dict: A dictionary containing the loaded JSON data.
    """
    with open(file_path, 'r') as file:
        config: Dict = json.load(file)
    return config

if __name__ == "__main__":
    pass