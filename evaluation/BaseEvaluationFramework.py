from abc import ABC, abstractmethod
from evaluation.evaluation import Evaluation

class BaseEvaluationFramework(ABC):

    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def evaluate(self, model, dataset, evaluation: Evaluation, metrics=None, **kwargs):
        """
        Evaluate the given model using the specified dataset.

        :param model: The model to be evaluated.
        :param dataset: The dataset to use for evaluation.
        :param metrics: Optional; the metrics to use for evaluation.
        :param kwargs: Additional keyword arguments.

        :return: Evaluation results.
        """
        pass

    def help(self):
        """
        Print a detailed explanation on what the evaluation framework does, what it is based on and how to use it.
        This method should be overridden in the subclass to provide specific details.
        """
        print("This is the placeholder explanation for your EvaluationFramework. Implement the help method in your class and override it.")

