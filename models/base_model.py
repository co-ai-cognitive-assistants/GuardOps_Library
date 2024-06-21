class BaseModel:
     """
    Abstract base class for models.

    This class defines a common interface for models, requiring the implementation
    of a predict method that takes an input text and returns a predicted text.

    Methods:
    - predict(input_text): Makes a prediction based on the input text. Must be implemented by subclasses.
    """
     def predict(self, input_text):
                """
        Make a prediction based on the input text.

        This method must be implemented by subclasses to provide specific prediction functionality.

        :param input_text: The input text for which to make a prediction.
        :return: The prediction result.
        :raises NotImplementedError: If the method is not implemented by a subclass.
        """
                raise NotImplementedError