from abc import ABC, abstractmethod

class BaseDataset(ABC):
    """
    Abstract base class for datasets.

    This class defines the basic structure and required methods for any dataset
    used in the evaluation framework. It enforces the implementation of `load`,
    `format`, and `help` methods in any subclass.
    """
    @abstractmethod
    def load(self):
        """
        Load the dataset.

        This method should implement the logic to load the dataset from its source,
        such as a file, database, or API. The implementation should ensure that the
        dataset is properly loaded and ready for use.

        :raises NotImplementedError: If the method is not implemented in the subclass.
        """
        raise NotImplementedError

    @abstractmethod
    def format(self, data=None):
        """
        Format the dataset.

        This method should implement the logic to format the dataset into a structure
        suitable for evaluation. The formatting might include data cleaning, preprocessing,
        and structuring the data into the required format for the evaluation framework.

        :param data: Optional; the data to be formatted. If not provided, the method
                     should use the loaded dataset.
        :raises NotImplementedError: If the method is not implemented in the subclass.
        """
        raise NotImplementedError
    
    @abstractmethod
    def help(self):
        """
        Provide help information about the dataset.

        This method should return a detailed explanation of the dataset, including its
        source, structure, usage, and any other relevant information. It is intended to
        help users understand the dataset and how to use it within the evaluation framework.

        :raises NotImplementedError: If the method is not implemented in the subclass.
        """
        raise NotImplementedError