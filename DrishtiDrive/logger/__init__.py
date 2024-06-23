# Import necessary modules
import os
import sys
import logging

# Set the format of the log messages
# The format is "[%(asctime)s: %(levelname)s: %(module)s: %(message)s]"
# %(asctime)s is the time when the message is logged
# %(levelname)s is the level of the log message (e.g., INFO, DEBUG, ERROR)
# %(module)s is the name of the module that logged the message
# %(message)s is the actual log message
logging_str = "[%(asctime)s: %(levelname)s: %(module)s: %(message)s]"

# Set the directory where the log file will be created
log_dir = "logs"

# Set the full path of the log file
log_filepath = os.path.join(log_dir,"logs.log")

# Create the logs directory if it doesn't already exist
os.makedirs(log_dir, exist_ok=True)

# Configure the logging module to log messages to the log file and to the console
# Set the log level to INFO, which means that only messages with a level of INFO or higher will be logged
# Set the log format to the one defined above
# Add a FileHandler that logs messages to the log file
# Add a StreamHandler that logs messages to the console
logging.basicConfig(
    level= logging.INFO,
    format= logging_str,

    handlers=[
        logging.FileHandler(log_filepath),
        logging.StreamHandler(sys.stdout)
    ]
)

