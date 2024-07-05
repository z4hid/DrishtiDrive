from dataclasses import dataclass


# This dataclass represents the artifacts produced by the data ingestion process.
# It contains the paths to the downloaded zip file and the extracted directory.
@dataclass
class DataIngestionArtifact:
    # Path to the downloaded zip file.
    data_zip_file_path: str
    
    # Path to the extracted directory.
    feature_store_file_path: str


# This dataclass represents the artifacts produced by the data validation process.
# It contains a boolean indicating whether all the required files exist or not.
@dataclass
class DataValidationArtifact:
    # Boolean indicating whether all the required files exist or not.
    validation_status: bool


# This dataclass represents the artifacts produced by the model training process.
# It contains the path to the trained model file.
@dataclass
class ModelTrainerArtifact:
    # Path to the trained model file.
    trained_model_file_path: str
