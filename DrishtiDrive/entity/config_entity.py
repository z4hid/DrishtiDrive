import os
from dataclasses import dataclass, field
from datetime import datetime
from DrishtiDrive.constant.training_pipeline import *


@dataclass
class TrainingPipelineConfig:
    """
    Configuration class for the training pipeline.

    Attributes:
        artifacts_dir (str): The directory where artifacts are stored.
    """
    artifacts_dir: str = ARTIFACTS_DIR 

# Create an instance of the TrainingPipelineConfig class
training_pipeline_config: TrainingPipelineConfig = TrainingPipelineConfig()


@dataclass
class DataIngestionConfig:
    """
    Configuration class for data ingestion.

    Attributes:
        data_ingestion_dir (str): The directory for data ingestion.
        feature_store_file_path (str): The file path for the feature store.
        data_download_url (str): The URL for downloading the data.
    """
    # Create the directory for data ingestion
    data_ingestion_dir: str = os.path.join(
        training_pipeline_config.artifacts_dir, DATA_INGESTION_DIR_NAME
    )

    # Create the file path for the feature store
    feature_store_file_path: str = os.path.join(
        data_ingestion_dir, DATA_INGESTION_FEATURE_STORE_DIR
    )

    # Set the URL for downloading the data
    data_download_url: str = DATA_DOWNLOAD_URL




@dataclass
class DataValidationConfig:
    """
    Configuration class for data validation.

    Attributes:
        data_validation_dir (str): The directory for data validation.
        valid_status_file_dir (str): The file path for the status file.
        required_file_list (list): A list of all the required files for data validation.
    """

    def _get_required_file_list():
        """Returns a copy of the required file list."""
        return DATA_VALIDATION_ALL_REQUIRED_FILES.copy()  

    # Directory for data validation
    data_validation_dir: str = os.path.join(
        training_pipeline_config.artifacts_dir, DATA_VALIDATION_DIR_NAME
    )

    # File path for the status file
    valid_status_file_dir: str = os.path.join(data_validation_dir, DATA_VALIDATION_STATUS_FILE)

    # List of all the required files for data validation
    required_file_list: list = field(default_factory=_get_required_file_list) 


    
