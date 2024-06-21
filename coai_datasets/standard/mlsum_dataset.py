from coai_datasets.standard.BaseDataset import BaseDataset
from datasets import load_dataset
import pandas as pd


_citiation = """
    @article{scialom2020mlsum,
  title={MLSUM: The Multilingual Summarization Corpus},
  author={Scialom, Thomas and Dray, Paul-Alexis and Lamprier, Sylvain and Piwowarski, Benjamin and Staiano, Jacopo},
  journal={arXiv preprint arXiv:2004.14900},
  year={2020}
    }
    
   Huggingface mlsum
"""

class MLSUMDataset(BaseDataset):
    """
    Class for handling the MLSUM dataset.

    This class provides methods to load and format the MLSUM dataset, as well as a help method
    to describe the dataset and its usage.
    """
    def __init__(self) -> None:
        """
        Initialize the MLSUMDataset instance.

        """
        super().__init__()
        self.data: pd.DataFrame = None

    def load(self, lang='de', nb_items=None):
        """
        Load the MLSUM dataset.

        This method fetches the MLSUM dataset from the Hugging Face dataset library and loads it
        into a pandas DataFrame. Optionally, it can limit the number of items loaded.

        :param lang: Language of the dataset to load (default is 'de' for German).
        :param nb_items: Optional; The number of items to load from the dataset. If None, loads the entire split.
        :return: A pandas DataFrame containing the loaded dataset.
        """
        dataset = load_dataset("mlsum", lang, trust_remote_code=True)
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
        Provide help information about the MLSUM dataset.

        This method returns a detailed explanation of the dataset, including its source, structure,
        usage, and any other relevant information.

        :return: A string containing the explanation of the dataset.
        """
        explanation = (
            "The MLSUMDataset class handles the MLSUM dataset.\n"
            "Methods:\n"
            "- load(lang='de', nb_items=None): Fetches and loads the MLSUM dataset using the specified language and number of items.\n"
            "- format(data): Formats the dataset as needed for evaluation.\n"
            "- help(): Provides detailed information about the dataset and its usage.\n"

            "\nUsage Example:\n"
            "dataset = MLSUMDataset()\n"
            "dataset.load(lang='de', nb_items=100)\n"
            "formatted_data = dataset.format(dataset.data)\n"
            "print(dataset.help())"
        )
        return explanation