from coai_datasets.standard.BaseDataset import BaseDataset
from datasets import load_dataset
import pandas as pd
import requests
from config.config import Config




class COAIDataset(BaseDataset):
    """
    Class for handling COAI datasets.

    This class provides methods to load and format datasets from the COAI evaluation framework,
    as well as a help method to describe the dataset and its usage.
    """
    def __init__(self) -> None:
        """
        Initialize the COAIDataset instance.
        """
        super().__init__()
        self.data: None

    def load(self, dataset_id):
        """
        Load the dataset using the provided dataset ID.

        This method fetches the dataset from the specified API endpoint using the user ID and dataset ID,
        and loads it into a pandas DataFrame.

        :param dataset_id: ID of the dataset to be loaded.
        :raises ValueError: If the dataset fails to load, with details of the response status code and content.
        """
        api_url = f"https://lm3.hs-ansbach.de/tracing/api/get_dataset_for_eval"
        params = {"user_id": Config.user_id, "dataset_id": dataset_id}
        response = requests.get(api_url, params)

        if response.status_code == 200:
            self.data = pd.DataFrame(response.json()["data"], columns=["prompt","response"])
        else:
            raise ValueError(f"Failed to load dataset. Status code: {response.status_code}, Response content: {response.content}")
        
        

    def format(self, data):
        """
        Format the dataset.

        This method applies specific formatting to the dataset as needed for the evaluation.
       
        :param data: The dataset to be formatted.
        :return: The formatted dataset.
        """
        # Specific formatting for the  dataset
        # ...
        return data
    
    def help(self):
        """
        Provide help information about the COAI dataset.

        This method returns a detailed explanation of the dataset, including its source, structure,
        usage, and any other relevant information.

        :return: A string containing the explanation of the dataset.
        """
        explanation = (
            "The COAIDataset class handles datasets used in the COAI evaluation framework.\n"
            "Methods:\n"
            "- load(dataset_id): Fetches and loads the dataset using the provided dataset ID.\n"
            "- format(data): Formats the dataset as needed for evaluation.\n"
            "- help(): Provides detailed information about the dataset and its usage.\n"
            "\nUsage Example:\n"
            "dataset = COAIDataset()\n"
            "dataset.load('your_dataset_id')\n"
            "formatted_data = dataset.format(dataset.data)\n"
            "print(dataset.help())"
        )
        return explanation