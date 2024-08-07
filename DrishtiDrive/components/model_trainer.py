import os
import sys
import yaml
import subprocess
from DrishtiDrive.utils.main_utils import read_yaml_file
from DrishtiDrive.exception import AppException
from DrishtiDrive.logger import logging
from DrishtiDrive.entity.config_entity import ModelTrainerConfig
from DrishtiDrive.entity.artifacts_entity import ModelTrainerArtifact

class ModelTrainer:
    def __init__(self, model_trainer_config: ModelTrainerConfig, feature_store_file_path: str):
        """
        Initializes a new instance of the `ModelTrainer` class.

        Args:
            model_trainer_config (ModelTrainerConfig): The configuration for the model trainer.
            feature_store_file_path (str): The path to the feature store file.

        Raises:
            AppException: If an error occurs during initialization.
        """
        try:
            self.model_trainer_config = model_trainer_config
            self.feature_store_file_path = feature_store_file_path
        except Exception as e:
            raise AppException(e, sys)

    def initiate_model_trainer(self) -> ModelTrainerArtifact:
        """
        Initializes the model trainer by performing the following steps:
        
        1. Checks for the existence of the data.yaml file in the specified feature store file path.
        2. Reads and updates the data.yaml file by updating the paths to be absolute.
        3. Prepares the model configuration by reading the corresponding YAML file and updating the number of classes.
        4. Prepares the training command by constructing the command string using the specified parameters.
        5. Executes the training command using the `os.system()` function.
        6. Checks for the existence of the best.pt file in the specified path.
        7. Copies the best model to the specified model trainer directory.
        
        Returns:
            ModelTrainerArtifact: An instance of the ModelTrainerArtifact class containing the path to the trained model file.
        
        Raises:
            FileNotFoundError: If the data.yaml file or the best.pt file is not found.
            AppException: If an error occurs during the initialization process.
        """
        logging.info("Entered initiate_model_trainer method of ModelTrainer class")
        try:
            # 1. Check for data.yaml file
            data_yaml_path = os.path.join(self.feature_store_file_path, 'data.yaml')
            logging.info(f"Checking for data YAML file: {data_yaml_path}")
            
            if not os.path.exists(data_yaml_path):
                logging.error(f"Data YAML file not found: {data_yaml_path}")
                logging.info(f"Contents of {self.feature_store_file_path}:")
                for item in os.listdir(self.feature_store_file_path):
                    logging.info(item)
                raise FileNotFoundError(f"Data YAML file not found: {data_yaml_path}")
            
            # 2. Read and update data.yaml
            with open(data_yaml_path, 'r') as stream:
                
                yaml_data = yaml.safe_load(stream)
                num_classes = yaml_data['nc']
                logging.info(f"Number of classes: {num_classes}")
                
                # Update paths in data.yaml to be absolute
                yaml_data['train'] = os.path.abspath(os.path.join(self.feature_store_file_path, yaml_data['train']))
                yaml_data['val'] = os.path.abspath(os.path.join(self.feature_store_file_path, yaml_data['val']))
                
            # Write updated data.yaml
            with open(data_yaml_path, 'w') as outfile:
                yaml.dump(yaml_data, outfile)
            
            # 3. Prepare model configuration
            model_config_file_name = self.model_trainer_config.weight_name.split('.')[0]
            config = read_yaml_file(f'yolov5/models/{model_config_file_name}.yaml')
            config['nc'] = num_classes

            custom_model_config_path = f'yolov5/models/custom_{model_config_file_name}.yaml'
            with open(custom_model_config_path, 'w') as outfile:
                yaml.dump(config, outfile)
            
            # 4. Prepare training command
            train_command = (
                f'cd yolov5/ && python train.py '
                f'--img 416 '
                f'--batch {self.model_trainer_config.batch_size} '
                f'--epochs {self.model_trainer_config.no_epochs} '
                f'--data {os.path.abspath(data_yaml_path)} '
                f'--cfg {os.path.abspath(custom_model_config_path)} '
                f'--weights {self.model_trainer_config.weight_name} '
                f'--name yolov5s_results '
                f'--cache'
            )
            logging.info(f"Training command: {train_command}")
            
            os.system(train_command)
            


            # 6. Check for best.pt file
            best_model_path = "yolov5/runs/train/yolov5s_results/weights/best.pt"
            if not os.path.exists(best_model_path):
                logging.error(f"Best model not found: {best_model_path}")
                logging.info("Contents of yolov5/runs/train/yolov5s_results/weights/:")
                weights_dir = os.path.dirname(best_model_path)
                if os.path.exists(weights_dir):
                    for item in os.listdir(weights_dir):
                        logging.info(item)
                else:
                    logging.error(f"Weights directory not found: {weights_dir}")
                raise FileNotFoundError(f"Best model not found: {best_model_path}")
            
            # 7. Copy best model
            os.system(f"cp {best_model_path} yolov5/")
            os.makedirs(self.model_trainer_config.model_trainer_dir, exist_ok=True)
            os.system(f"cp {best_model_path} {self.model_trainer_config.model_trainer_dir}/")
            
            model_trainer_artifact = ModelTrainerArtifact(
                trained_model_file_path="yolov5/best.pt",
            )

            logging.info("Exited initiate_model_trainer method of ModelTrainer class")
            logging.info(f"Model trainer artifact: {model_trainer_artifact}")
            
            return model_trainer_artifact

        except Exception as e:
            logging.error(f"Error in initiate_model_trainer: {str(e)}")
            raise AppException(e, sys)