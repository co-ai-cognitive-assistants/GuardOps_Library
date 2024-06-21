from abc import ABC, abstractmethod

class BaseMetric(ABC):
    """
    An abstract base class for evaluation metrics.

    This class provides the structure for implementing various evaluation metrics.
    """
    
    @abstractmethod
    def __init__(self, name):
        self.name = name
    
    @abstractmethod
    def calculate(self, predictions, references):
        """
        Calculate the metric score for given predictions and referance.
        
        :param predictions: A list of model predictions.
        :param references: A list of reference (ground truth) values.

        :return: The calculated metric score.
        """
        raise NotImplementedError

class BLEUMetric(BaseMetric):
    """
    A class to calculate the BLEU score.

    This class implements the BLEU (Bilingual Evaluation Understudy) metric.
    """

    def __init__(self):
        """
        Initialize the BLEU metric with a name.
        """
        super().__init__("bleu")


    def calculate(self, predictions, references):
        """
        Calculate the BLEU score for the given predictions and references.

        :param predictions: A list of model predictions.
        :param references: A list of reference (ground truth) values.

        :return: The calculated BLEU score.
        """
        # BLEU calculation logic
        bleu_score = None
        return bleu_score

class Rouge1Metric(BaseMetric):
    """
    A class to calculate the ROUGE-1 score.

    This class implements a basic version of the ROUGE-1 (Recall-Oriented Understudy for Gisting Evaluation) metric.
    """
    def __init__(self):
        """
        Initialize the ROUGE-1 metric with a name.
        """
        super().__init__("rouge1")
    
    def calculate(self, predictions, references):
        # Simple ROUGE-1 calculation
        # This is a very basic implementation. Later implement rouge_score library
        total_overlap = 0
        for pred, ref in zip(predictions, references):
            pred_set = set(pred.split())
            ref_set = set(ref.split())
            overlap = pred_set.intersection(ref_set)
            total_overlap += len(overlap) / len(ref_set)
        return total_overlap / len(predictions) if predictions else 0