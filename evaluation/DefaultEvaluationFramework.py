from tqdm import tqdm
from evaluation.BaseEvaluationFramework import BaseEvaluationFramework

class DefaultEvaluationFramework(BaseEvaluationFramework):
    """
    A default implementation of the BaseEvaluationFramework.

    """

    def evaluate(self, model, dataset, metrics):

        """
        Evaluate the given model using the specified dataset and metrics.

        :param model: The model to be evaluated. 
        :param dataset: The dataset to use for evaluation
        :param metrics: The metrics to use for evaluation of model for specified dataset.
         
        :return: A dictionary where the keys are the names of the metrics and the values are the calculated scores.
        """


        results = {}
        predictions = [model.predict(input_text) for input_text, _ in tqdm(dataset, desc="Prediction for Evaluation")]
        references = [ref for _, ref in dataset]
        for metric in tqdm(metrics, desc="Calculating Metrics"):
            score = metric.calculate(predictions, references)
            results[metric.__class__.__name__] = score
        return results
    
    def help(self):
        """ 
        """