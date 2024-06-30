import os
import sys
import zipfile
import gdown

from DrishtiDrive.logger import logging
from DrishtiDrive.exception import AppException
from DrishtiDrive.entity.config_entity import DataIngestionConfig
from DrishtiDrive.entity.artifacts_entity import DataIngestionArtifact


class DataIngestion:
    """
    Class to handle data ingestion process.
    """

    def __init__(self, data_ingestion_config: DataIngestionConfig):
        """
        Initialize DataIngestion class with data ingestion configuration.

        Args:
            data_ingestion_config (DataIngestionConfig): Data ingestion configuration.
        """
        try:
            self.data_ingestion_config = data_ingestion_config

        except Exception as e:
            raise AppException(e, sys)
    
    
    def download_data(self) -> str:
        """
        Downloads data from the specified URL and saves it as a zip file.

        Returns:
            str: Path to the downloaded zip file.
        """
        try:
            # Get the URL and download directory from the configuration
            url = self.data_ingestion_config.data_download_url
            download_dir = self.data_ingestion_config.data_ingestion_dir

            # Create the download directory if it doesn't exist
            os.makedirs(download_dir, exist_ok=True)
            
            # Set the name of the zip file
            data_file_name = 'data.zip'
            # Construct the path to the zip file
            zip_file_path = os.path.join(download_dir, data_file_name)

            # Check if the file already exists
            if os.path.exists(zip_file_path):
                logging.info(f"File already exists at : [{zip_file_path}]. Skipping download.")
                return zip_file_path
            
            # Log the download operation
            logging.info(f"Downloading file from : [{url}] into : [{zip_file_path}]")
            
            # Extract the file ID from the URL
            file_id = url.split('/')[-2]
            # Construct the prefix for the download URL
            prefix = f'https://drive.google.com/uc?export=download&id='
            # Download the file using gdown
            gdown.download(prefix + file_id, zip_file_path, quiet=False)
            # Log the successful download
            logging.info(f"File : [{zip_file_path}] has been downloaded successfully.")
            # Return the path to the downloaded zip file
            return zip_file_path

        except Exception as e:
            raise AppException(e, sys)
        
    
    def extract_zip_file(self, zip_file_path: str) -> str:
        """
        Extracts the contents of the specified zip file to the specified directory.

        Args:
            zip_file_path (str): Path to the zip file.

        Returns:
            str: Path to the extracted directory.
        """
        try:
            # Get the feature store path from the configuration
            feature_store_path = self.data_ingestion_config.feature_store_file_path
            # Create the feature store directory if it doesn't exist
            os.makedirs(feature_store_path, exist_ok=True)
            # Open the zip file for reading
            with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
                # Extract all files from the zip file to the feature store directory
                zip_ref.extractall(feature_store_path)
                # Log the successful extraction
                logging.info(f"Extracting Zip File: [{zip_file_path}] into dir: {feature_store_path}")
            # Log the successful extraction
            logging.info(f"Data has been extracted successfully.")
            # Return the path to the extracted directory
            return feature_store_path
        
        except Exception as e:
            raise AppException(e, sys)
        
    
    def initiate_data_ingestion(self) -> DataIngestionArtifact:
        """
        Initiates the data ingestion process by downloading and extracting the data.

        Returns:
            DataIngestionArtifact: Artifact containing the paths to the downloaded zip file and extracted directory.
        """
        logging.info("Entered initiate_data_ingestion method of DataIngestion class")
        try:
            # Download the data and get the path to the downloaded zip file
            zip_file_path = self.download_data()
            # Extract the zip file and get the path to the extracted directory
            feature_store_path = self.extract_zip_file(zip_file_path=zip_file_path)
            # Create a DataIngestionArtifact with the paths to the downloaded zip file and extracted directory
            data_ingestion_artifact = DataIngestionArtifact(
                data_zip_file_path=zip_file_path,
                feature_store_file_path=feature_store_path
            )
            logging.info("Exited initiate_data_ingestion method of DataIngestion class")
            logging.info(f"Data Ingestion Artifact: [{data_ingestion_artifact}]")
            # Return the DataIngestionArtifact
            return data_ingestion_artifact
        
        except Exception as e:
            raise AppException(e, sys)
