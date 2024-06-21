from coai_datasets.standard.BaseDataset import BaseDataset
from datasets import load_dataset
import pandas as pd


_citiation = """
    @article{hendryckstest2021,
      title={Measuring Massive Multitask Language Understanding},
      author={Dan Hendrycks and Collin Burns and Steven Basart and Andy Zou and Mantas Mazeika and Dawn Song and Jacob Steinhardt},
      journal={Proceedings of the International Conference on Learning Representations (ICLR)},
      year={2021}
    }
    
    Huggingface cais/mmlu
"""

class MMLUDataset(BaseDataset):
    """
    Class for handling the MMLU (Massive Multitask Language Understanding) dataset.

    This class provides methods to load and format the MMLU dataset, as well as a help method
    to describe the dataset and its usage.
    """

    def __init__(self) -> None:
        """
        Initialize the MMLUDataset instance.

        """
        super().__init__()
        self.data: None

    def load(self):
        """
        Load the MMLU dataset.

        This method fetches the MMLU dataset from the Hugging Face dataset library and loads it
        into a pandas DataFrame.

        :return: None
        """
        dataset = load_dataset("cais/mmlu","all", trust_remote_code=True)
        self.data = pd.DataFrame(dataset["test"])
        

    def format(self, data):
        """
        Format the dataset.

        This method applies specific formatting to the dataset as needed for the evaluation.
        Currently, it returns the data as is, but it can be extended to include data cleaning
        and preprocessing steps.

        :param data: The dataset to be formatted.
        :return: The formatted dataset.
        """
        # Specific formatting for the  dataset
        # ...
        return data
    
    def help(self):
        """
        Provide help information about the MMLU dataset.

        This method returns a detailed explanation of the dataset, including its source, structure,
        usage, and any other relevant information.

        :return: A string containing the explanation of the dataset.
        """
        explanation = (
            "The MMLUDataset class handles the MMLU (Massive Multitask Language Understanding) dataset.\n"
            "Methods:\n"
            "- load(): Fetches and loads the MMLU dataset using the specified repository and configuration.\n"
            "- format(data): Formats the dataset as needed for evaluation.\n"
            "- help(): Provides detailed information about the dataset and its usage.\n"

            "\nUsage Example:\n"
            "dataset = MMLUDataset()\n"
            "dataset.load()\n"
            "formatted_data = dataset.format(dataset.data)\n"
            "print(dataset.help())"
        )
        return explanation