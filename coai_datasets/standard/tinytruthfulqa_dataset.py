from coai_datasets.standard.BaseDataset import BaseDataset
from datasets import load_dataset
import pandas as pd


_citiation = """
@article{polo2024tinybenchmarks,
  title={tinyBenchmarks: evaluating LLMs with fewer examples}, 
  author={Felipe Maia Polo and Lucas Weber and Leshem Choshen and Yuekai Sun and Gongjun Xu and Mikhail Yurochkin},
  year={2024},
  eprint={2402.14992},
  archivePrefix={arXiv},
  primaryClass={cs.CL}
  }
@misc{lin2021truthfulqa,
  title={TruthfulQA: Measuring How Models Mimic Human Falsehoods},
  author={Stephanie Lin and Jacob Hilton and Owain Evans},
  year={2021},
  eprint={2109.07958},
  archivePrefix={arXiv},
  primaryClass={cs.CL}
}
"""

class TinyTruthfulQADataset(BaseDataset):
    """
    Class for handling the TinyTruthfulQA dataset.

    This class provides methods to load and format the TinyTruthfulQA dataset, as well as a help method
    to describe the dataset and its usage.
    """
    def __init__(self) -> None:
        """
        Initialize the TinyTruthfulQADataset instance.
        """
        super().__init__()
        self.data: pd.DataFrame = None

    def load(self, nb_items=None):
        """
        Load the TinyTruthfulQA dataset.

        This method fetches the TinyTruthfulQA dataset from the Hugging Face dataset library and loads it
        into a pandas DataFrame.

        :param nb_items: Optional; Number of items to load from the dataset.
        :return: The loaded dataset as a pandas DataFrame.
        """
        dataset = load_dataset("tinyBenchmarks/tinyTruthfulQA","multiple_choice")
        self.data = pd.DataFrame(dataset["validation"][:nb_items])
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
        Provide help information about the TinyTruthfulQA dataset.

        This method returns a detailed explanation of the dataset, including its source, structure,
        usage, and any other relevant information.

        :return: A string containing the explanation of the dataset.
        """
        explanation = (
            "The TinyTruthfulQADataset class handles the TinyTruthfulQA dataset.\n"
            "Methods:\n"
            "- load(nb_items=None): Fetches and loads the TinyTruthfulQA dataset using the specified repository and configuration.\n"
            "- format(data): Formats the dataset as needed for evaluation.\n"
            "- help(): Provides detailed information about the dataset and its usage.\n"
 
            "\nUsage Example:\n"
            "dataset = TinyTruthfulQADataset()\n"
            "dataset.load(nb_items=100)\n"
            "formatted_data = dataset.format(dataset.data)\n"
            "print(dataset.help())"
        )
        return explanation