import sys, os
from DrishtiDrive.exception import AppException
from DrishtiDrive.logger import logging
from DrishtiDrive.components.data_ingestion import DataIngestion
from DrishtiDrive.components.data_validation import DataValidation
from DrishtiDrive.entity.config_entity import DataIngestionConfig, DataValidationConfig
from DrishtiDrive.entity.artifacts_entity import DataIngestionArtifact, DataValidationArtifact


class TrainingPipeline:
    def __init__(self):
        self.data_ingestion_config = DataIngestionConfig()
        self.data_validation_config = DataValidationConfig()

    def start_data_ingestion(self) -> DataIngestionArtifact:
        try:
            logging.info("Starting start_data_ingestion method of TrainingPipeline class")
            logging.info("Getting data from url")
            data_ingestion = DataIngestion(
                data_ingestion_config=self.data_ingestion_config
            )
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
            logging.info("Got data from url")
            logging.info("Exited start_data_ingestion method of TrainingPipeline class")
            return data_ingestion_artifact

        except Exception as e:
            raise AppException(e, sys)
        
    
    def start_data_validation(self, data_ingestion_artifact: DataIngestionArtifact) -> DataValidationArtifact:
        logging.info("Starting start_data_validation method of TrainingPipeline class")
        
        
        try:
            data_validation = DataValidation(
                data_ingestion_artifact=data_ingestion_artifact,
                data_validation_config=self.data_validation_config
            )
            data_validation_artifact = data_validation.initiate_data_validation()
            logging.info('Performed data validation')
            logging.info("Exited start_data_validation method of TrainingPipeline class")
            return data_validation_artifact
        
        except Exception as e:
            raise AppException(e, sys)
        
    
    def run_pipeline(self):
        try:
            data_ingestion_artifact = self.start_data_ingestion()
            data_validation_artifact = self.start_data_validation(data_ingestion_artifact=data_ingestion_artifact)
        except Exception as e:
            raise AppException(e, sys)