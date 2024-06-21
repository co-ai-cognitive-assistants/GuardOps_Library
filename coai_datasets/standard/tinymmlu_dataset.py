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
@article{hendryckstest2021,
  title={Measuring Massive Multitask Language Understanding},
  author={Dan Hendrycks and Collin Burns and Steven Basart and Andy Zou and Mantas Mazeika and Dawn Song and Jacob Steinhardt},
  journal={Proceedings of the International Conference on Learning Representations (ICLR)},
  year={2021}
}
"""

class TinyMMLUDataset(BaseDataset):
    """
    Class for handling the TinyMMLU dataset.

    This class provides methods to load and format the TinyMMLU dataset, as well as a help method
    to describe the dataset and its usage.
    """
    def __init__(self) -> None:
        super().__init__()
        self.data: pd.DataFrame = None

    def load(self, nb_items=None):
        """
        Load the TinyMMLU dataset.

        This method fetches the TinyMMLU dataset from the Hugging Face dataset library and loads it
        into a pandas DataFrame.

        :param nb_items: Optional; Number of items to load from the dataset.
        :return: The loaded dataset as a pandas DataFrame.
        """
        dataset = load_dataset("tinyBenchmarks/tinyMMLU","all")
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
        Provide help information about the TinyMMLU dataset.

        This method returns a detailed explanation of the dataset, including its source, structure,
        usage, and any other relevant information.

        :return: A string containing the explanation of the dataset.
        """
        explanation =  (
            "The TinyMMLUDataset class handles the TinyMMLU dataset.\n"
            "Methods:\n"
            "- load(nb_items=None): Fetches and loads the TinyMMLU dataset using the specified repository and configuration.\n"
            "- format(data): Formats the dataset as needed for evaluation.\n"
            "- help(): Provides detailed information about the dataset and its usage.\n"

            "\nUsage Example:\n"
            "dataset = TinyMMLUDataset()\n"
            "dataset.load(nb_items=100)\n"
            "formatted_data = dataset.format(dataset.data)\n"
            "print(dataset.help())"
        )
        return explanation