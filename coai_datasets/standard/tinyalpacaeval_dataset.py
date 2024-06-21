from coai_datasets.standard.BaseDataset import BaseDataset
from datasets import load_dataset
import pandas as pd


class TinyAlpacaEvalDataset(BaseDataset):
    """
    Class for handling the TinyAlpacaEval dataset.

    This class provides methods to load and format the TinyAlpacaEval dataset, as well as a help method
    to describe the dataset and its usage.
    """
    def __init__(self) -> None:
        """
        Initialize the TinyAlpacaEvalDataset instance.

        This method initializes the dataset instance, setting the data attribute to None.
        """
        super().__init__()
        self.data: pd.DataFrame = None

    def load(self, nb_items=None):
        """
        Load the TinyAlpacaEval dataset.

        This method fetches the TinyAlpacaEval dataset from the Hugging Face dataset library and loads it
        into a pandas DataFrame.

        :param nb_items: Optional; Number of items to load from the dataset.
        :return: The loaded dataset as a pandas DataFrame.
        """
        dataset = load_dataset("tinyBenchmarks/tinyAlpacaEval","default")
        self.data = pd.DataFrame(dataset["test"][:nb_items])
        return self.data

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
        Provide help information about the TinyAlpacaEval dataset.

        This method returns a detailed explanation of the dataset, including its source, structure,
        usage, and any other relevant information.

        :return: A string containing the explanation of the dataset.
        """
        explanation =  (
            "The TinyAlpacaEvalDataset class handles the TinyAlpacaEval dataset.\n"
            "Methods:\n"
            "- load(nb_items=None): Fetches and loads the TinyAlpacaEval dataset using the specified repository and configuration.\n"
            "- format(data): Formats the dataset as needed for evaluation.\n"
            "- help(): Provides detailed information about the dataset and its usage.\n"

            "\nUsage Example:\n"
            "dataset = TinyAlpacaEvalDataset()\n"
            "dataset.load(nb_items=100)\n"
            "formatted_data = dataset.format(dataset.data)\n"
            "print(dataset.help())"
        )
        return explanation