import os
import sys
import shutil

from DrishtiDrive.exception import AppException
from DrishtiDrive.logger import logging
from DrishtiDrive.entity.config_entity import DataValidationConfig
from DrishtiDrive.entity.artifacts_entity import DataIngestionArtifact, DataValidationArtifact


class DataValidation:
    """
    This class performs data validation by checking if all the required files exist in the feature store directory.
    """

    def __init__(self,
                 data_ingestion_artifact: DataIngestionArtifact,
                 data_validation_config: DataValidationConfig):
        """
        Initialize the DataValidation class.
        
        Args:
            data_ingestion_artifact (DataIngestionArtifact): The artifacts produced by the data ingestion process.
            data_validation_config (DataValidationConfig): The configuration for data validation.
        """
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config

        except Exception as e:
            raise AppException(e, sys)

    def validate_all_files_exist(self)-> bool:
        """
        Validate if all the required files exist in the feature store directory.
        
        Returns:
            bool: True if all the required files exist, False otherwise.
        """
        try:
            validation_status = None  # Initialize the validation status to None

            all_files = os.listdir(self.data_ingestion_artifact.feature_store_file_path)  # Get all files in the feature store directory

            for file in all_files:  # Iterate over each file
                if file not in self.data_validation_config.required_file_list:  # Check if the file is not in the required file list
                    validation_status = False  # Set the validation status to False
                    os.makedirs(self.data_validation_config.data_validation_dir, exist_ok=True)  # Create the data validation directory if it doesn't exist
                    with open(self.data_validation_config.valid_status_file_dir, 'w') as f:  # Write the validation status to the status file
                        f.write(f"Validation status: {validation_status}")
                else:
                    validation_status = True  # Set the validation status to True
                    os.makedirs(self.data_validation_config.data_validation_dir, exist_ok=True)  # Create the data validation directory if it doesn't exist
                    with open(self.data_validation_config.valid_status_file_dir, 'w') as f:  # Write the validation status to the status file
                        f.write(f"Validation status: {validation_status}")

            return validation_status  # Return the validation status

        except Exception as e:
            raise AppException(e, sys)

    def initiate_data_validation(self) -> DataValidationArtifact:
        """
        Initiate the data validation process.
        
        Returns:
            DataValidationArtifact: The artifacts produced by the data validation process.
        """
        logging.info("Entered initiate_data_validation method of DataValidation class")
        try:
            status = self.validate_all_files_exist()  # Validate if all the required files exist
            data_validation_artifact = DataValidationArtifact(
                validation_status=status
            )
            logging.info("Exited initiate_data_validation method of DataValidation class")
            logging.info(f"Data validation artifact: {data_validation_artifact}")

            if status:  # If the validation status is True
                shutil.copy(self.data_ingestion_artifact.data_zip_file_path, os.getcwd())  # Copy the data zip file to the current working directory
            return data_validation_artifact  # Return the data validation artifact

        except Exception as e:
            raise AppException(e, sys)

