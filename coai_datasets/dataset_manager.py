from config.config import Config
from coai_datasets.standard.mmlu_dataset import MMLUDataset
from coai_datasets.standard.coai_dataset import COAIDataset
from coai_datasets.datasets import DEFAULT_DATASETS
import requests
from pprint import pprint
from dotenv import load_dotenv
import os

BACKEND_API_URL = os.getenv("BACKEND_API_URL")
def load_user_datasets():
        
        #TODO: Change endpoint to get_datasets_for_eval later on
        api_url = f"{BACKEND_API_URL}/api/get_datasets_for_eval"
        params = {"user_id": Config.user_id}
        response = requests.get(api_url, params)

        if response.status_code == 200:
            data=response.json()["datasets"]
            return data
        else:
            print(f"Failed to load datasets. Status code: {response.status_code}, Response content: {response.content}")

class DatasetManager:
    def __init__(self):
        self.datasets = load_user_datasets()
        self.default_datasets = DEFAULT_DATASETS

    def add_dataset(self, dataset_name, description, data, project_id=None, user_id=None):
        """
        Adds a new dataset to the list.

        :param dataset_name: Name of the dataset.
        :param description: Description of dataset.
        :param data: Actual data of the dataset.
        :param project_id (str, optional): ID of the project associated with this dataset.
        :param user_id: ID of the user who owns this dataset.
        """
        
        dataset = {
            'dataset_id': dataset_name,
            'description': description,
            'data': data,
        }
        self.datasets.append(dataset)
        print("Dataset " + dataset_name + " added successfully.")

    def list_datasets(self):
        """
        Lists all datasets for a given user.
        
        :return: List of datasets belonging to the user.
        """
        print("\n===============Custom Datasets===============\n")
        pprint(self.datasets)
        print("\n===============Default Datasets===============\n")
        pprint(self.default_datasets)
        
    
    def load_default_dataset(self, dataset_name):
        """
        Load a default dataset by name.

        :param dataset_name: Name of the default dataset to load.
        :return: Dataset if found, else ValueError.
        """
        dataset = self.default_datasets.get(dataset_name.lower())
        if dataset:
            return dataset
        raise ValueError( f"No default dataset with name {dataset_name} found. Please choose from the following names: {list(self.default_datasets.keys())}")
    
    def load_custom_dataset(self, dataset_id):
        """
        Load a custom dataset by id.

        :param dataset_id: ID of the custom dataset to load.
        :return: Dataset if found, else ValueError.
        """
        dataset = COAIDataset()
        dataset.load(dataset_id=dataset_id)
        return dataset
        
   