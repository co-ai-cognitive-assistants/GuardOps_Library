from coai_datasets.standard.BaseDataset import BaseDataset
from datasets import load_dataset
import pandas as pd


_citiation = """
Add the appropriate citation for the dataset here.
"""

class HuggingfaceDataset(BaseDataset):
    """
    Class for handling datasets from Hugging Face's dataset library.

    This class provides methods to load and format datasets from the Hugging Face library,
    as well as a help method to describe the dataset and its usage.
    """

    def __init__(self, repo,tag,split) -> None:
        """
        Initialize the HuggingfaceDataset instance.

        This method initializes the dataset instance with the specified repository, tag, and split,
        setting the data attribute to None.

        :param repo: The repository name in the Hugging Face dataset library.
        :param tag: The tag or configuration name of the dataset.
        :param split: The split of the dataset (e.g., 'train', 'test').
        """
        super().__init__()
        self.repo = repo
        self.split = split
        self.tag = tag
        self.data: pd.DataFrame = None

    def load(self, nb_items=None):
        """
        Load the dataset using the specified repository, tag, and split.

        This method fetches the dataset from the Hugging Face dataset library and loads it into
        a pandas DataFrame. Optionally, it can limit the number of items loaded.

        :param nb_items: Optional; The number of items to load from the dataset. If None, loads the entire split.
        :return: A pandas DataFrame containing the loaded dataset.
        """
        dataset = load_dataset(self.repo,self.tag)
        self.data = pd.DataFrame(dataset[self.split][:nb_items])
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
        Provide help information about the Hugging Face dataset.

        This method returns a detailed explanation of the dataset, including its source, structure,
        usage, and any other relevant information.

        :return: A string containing the explanation of the dataset.
        """
        explanation = (
            "The HuggingfaceDataset class handles datasets from the Hugging Face dataset library.\n"
            "Methods:\n"
            "- load(nb_items=None): Fetches and loads the dataset using the specified repository, tag, and split.\n"
            "- format(data): Formats the dataset as needed for evaluation.\n"
            "- help(): Provides detailed information about the dataset and its usage.\n"
            "\nUsage Example:\n"
            "dataset = HuggingfaceDataset(repo='repo_name', tag='config_tag', split='train')\n"
            "dataset.load(nb_items=100)\n"
            "formatted_data = dataset.format(dataset.data)\n"
            "print(dataset.help())"
        )
        return explanation