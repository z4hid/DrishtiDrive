"""
This script is used to generate a template project structure for a Python project.
It creates directories and empty files based on a list of file paths.
"""

import os
from pathlib import Path
import logging


# Configure the logging module to log messages with a level of INFO or higher.
# The format of the log message is set to "[%(asctime)s]: %(message)s:",
# where %(asctime)s is the time when the message is logged and %(message)s
# is the log message itself.
# The logging level is set to INFO, which means that only messages with a
# level of INFO or higher will be logged.
# Other logging levels are CRITICAL (highest), ERROR, WARNING, and DEBUG (lowest).
# The ':' at the end of the format string is used to separate the log message
# from the timestamp.
logging.basicConfig(
    level=logging.INFO, 
    format='[%(asctime)s]: %(message)s:'
)


project_name = "DrishtiDrive"

# List of file paths to be created
list_of_files = [
    ".github/workflows/.gitkeep",  # Keep GitHub Actions workflows directory
    "data/.gitkeep",  # Keep data directory
    f"{project_name}/__init__.py",  # __init__.py for project package
    f"{project_name}/components/__init__.py",  # __init__.py for components package
    f"{project_name}/components/data_ingestion.py",  # Data ingestion component
    f"{project_name}/components/data_validation.py",  # Data validation component
    f"{project_name}/components/model_trainer.py",  # Model training component
    f"{project_name}/constant/__init__.py",  # __init__.py for constants package
    f"{project_name}/constant/training_pipeline/__init__.py",  # __init__.py for training pipeline constants package
    f"{project_name}/constant/application.py",  # Application constants
    f"{project_name}/entity/config_entity.py",  # Configuration entity
    f"{project_name}/entity/artifacts_entity.py",  # Artifacts entity
    f"{project_name}/exception/__init__.py",  # __init__.py for exception package
    f"{project_name}/logger/__init__.py",  # __init__.py for logger package
    f"{project_name}/pipeline/__init__.py",  # __init__.py for pipeline package
    f"{project_name}/pipeline/training_pipeline.py",  # Training pipeline
    f"{project_name}/utils/__init__.py",  # __init__.py for utils package
    f"{project_name}/utils/main_utils.py",  # Main utilities
    "research/trials.ipynb",  # Research notebook
    "templates/index.html",  # HTML template for app
    "app.py",  # Main app file
    "Dockerfile",  # Dockerfile for building container
    "requirements.txt",  # Requirements file
    "setup.py",  # Setup file for packaging
]


# Loop through the list of file paths and create directories and files
for filepath in list_of_files:
    filepath = Path(filepath)

    filedir, filename = os.path.split(filepath)

    # Create directory if it doesn't exist
    if filedir != "":
        os.makedirs(filedir, exist_ok=True)
        logging.info(f"Creating directory: {filedir} for the file {filename}")

    # Create empty file if it doesn't exist or is empty
    if (not os.path.exists(filename)) or (os.path.getsize(filename) == 0):
        with open(filepath, "w") as f:
            pass
            logging.info(f"Creating empty file: {filename}")

    # Log message if file already exists
    else:
        logging.info(f"{filename} is already created")


