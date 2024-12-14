import json
import os

def write_json_file(file_path: str, data: dict) -> None:
    """Writes a dictionary to a JSON file.

    Args:
        file_path (str): The path to the JSON file to be created or overwritten.
        data (dict): The dictionary data to be written to the JSON file.

    Returns:
        None

    Raises:
        TypeError: If 'data' is not a dictionary.
        FileNotFoundError: If the directory of 'file_path' does not exist
        IOError: If there's an error writing to the file.

    Usage:
        >>> my_data = {"name": "John", "age": 30, "city": "New York"}
        >>> write_json_file("data.json", my_data)
        # Creates a 'data.json' file with the JSON representation of my_data.
    """
    if not isinstance(data, dict):
        raise TypeError("Input 'data' must be a dictionary.")

    directory = os.path.dirname(file_path)
    if directory and not os.path.exists(directory):
        raise FileNotFoundError(f"Directory '{directory}' does not exist.")

    try:
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=4)
    except IOError as e:
        raise IOError(f"Error writing to file '{file_path}': {e}")


from pathlib import Path
import yaml


def write_yml_file(file_path: str, data: dict) -> None:
    """Writes a dictionary to a YAML file.

    Args:
        file_path (str): The path to the YAML file to be created or overwritten.
        data (dict): The dictionary data to be written to the YAML file.

    Returns:
        None

    Raises:
        TypeError: If 'data' is not a dictionary.
        FileNotFoundError: If the directory of 'file_path' does not exist
        IOError: If there's an error writing to the file.
        ImportError: If the 'PyYAML' package is not installed.

    Usage:
        >>> my_data = {"name": "Alice", "age": 25, "country": "Canada"}
        >>> write_yml_file("config.yml", my_data)
        # Creates a 'config.yml' file with the YAML representation of my_data.
    """
    if not isinstance(data, dict):
        raise TypeError("Input 'data' must be a dictionary.")
    
    try:
        file_path_obj = Path(file_path)
        if not file_path_obj.parent.exists():
           raise FileNotFoundError(f"Directory {file_path_obj.parent} does not exist")

        with open(file_path, 'w') as file:
            yaml.dump(data, file)
    except ImportError:
         raise ImportError("PyYAML package is not installed. Please install it using 'pip install pyyaml'")
    except FileNotFoundError as e:
        raise e
    except IOError as e:
        raise IOError(f"Error writing to file: {e}")


import toml
import os

def write_toml_file(file_path: str, data: dict) -> None:
    """Writes a dictionary to a TOML file.

    Args:
        file_path (str): The path to the TOML file to be created or overwritten.
        data (dict): The dictionary data to be written to the TOML file.

    Returns:
        None

    Raises:
        TypeError: If 'data' is not a dictionary.
        FileNotFoundError: If the directory of 'file_path' does not exist
        IOError: If there's an error writing to the file.
        ImportError: If the 'toml' package is not installed.

    Usage:
        >>> settings = {"server": {"host": "127.0.0.1", "port": 8080}, "logging": {"level": "INFO"}}
        >>> write_toml_file("settings.toml", settings)
        # Creates a 'settings.toml' file with the TOML representation of settings.
    """
    if not isinstance(data, dict):
        raise TypeError("Input data must be a dictionary.")
    
    try:
      dir_path = os.path.dirname(file_path)
      if dir_path and not os.path.exists(dir_path):
        raise FileNotFoundError(f"Directory '{dir_path}' does not exist.")
      with open(file_path, 'w') as f:
            toml.dump(data, f)
    except ImportError:
        raise ImportError("The 'toml' package is not installed. Please install it using 'pip install toml'.")
    except FileNotFoundError as e:
        raise e
    except IOError as e:
        raise IOError(f"Error writing to file: {e}")
