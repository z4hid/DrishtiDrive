import os.path
import sys
import yaml
import base64

from DrishtiDrive.exception import AppException
from DrishtiDrive.logger import logging


def read_yaml_file(file_path: str) -> dict:
    """
    Reads a YAML file from the given file path and returns the parsed contents as a dictionary.

    Args:
        file_path (str): The path to the YAML file.

    Returns:
        dict: The parsed contents of the YAML file.

    Raises:
        AppException: If an exception occurs while reading or parsing the YAML file.
    """
    try:
        # Open the YAML file in binary mode and read its contents
        with open(file_path, "rb") as yaml_file:
            # Log the fact that the YAML file has been read
            logging.info(f"Read yaml file: {file_path}")
            # Parse the YAML contents and return the resulting dictionary
            return yaml.safe_load(yaml_file)

    except Exception as e:
        # If an exception occurs, raise an AppException with the exception and the system details
        raise AppException(e, sys)
    

def write_yaml_file(file_path: str, content: object, replace: bool = False) -> None:
    """
    Writes the given content to a YAML file at the specified file path.

    Args:
        file_path (str): The path of the file to write.
        content (object): The content to write to the file.
        replace (bool, optional): If True, the file will be replaced if it already exists. Defaults to False.

    Returns:
        None

    Raises:
        AppException: If an exception occurs while writing the file.
    """
    try:
        # If replace is True and the file already exists, remove the file
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
        # Create the directory containing the file path if it doesn't already exist
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        # Open the file for writing and write the YAML contents to it
        with open(file_path, "w") as file:
            yaml.dump(content, file)
            # Log the fact that the YAML file has been written
            logging.info(f"Write yaml file: {file_path}")

    except Exception as e:
        # If an exception occurs, raise an AppException with the exception and the system details
        raise AppException(e, sys)
    
    

def decodeImage(imgstring, filename):
    """
    Decodes a base64-encoded image string and saves the resulting image to the specified file path.

    Args:
        imgstring (str): The base64-encoded image string.
        filename (str): The file path to save the decoded image to.

    Returns:
        None
    """
    # Decode the base64-encoded image string
    imagedata = base64.b64decode(imgstring)
    # Open the file for writing binary data and write the decoded image data to it
    with open('./data/'+filename, 'wb') as f:
        f.write(imagedata)
        # Close the file
        f.close()
        

def encodeImageIntoBase64(imagepath):
    """
    Reads an image file from the specified path and encodes it into a base64-encoded string.

    Args:
        imagepath (str): The path to the image file.

    Returns:
        str: The base64-encoded string representation of the image.
    """
    # Open the image file in binary mode and read its contents
    with open(imagepath, "rb") as image_file:
        # Encode the image contents into a base64-encoded string
        encoded_string = base64.b64encode(image_file.read())
    # Return the base64-encoded string
    return encoded_string

