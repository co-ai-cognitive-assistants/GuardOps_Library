from deepeval.evaluate import TestResult
from evaluation.BaseEvaluationFramework import BaseEvaluationFramework
from deepeval import evaluate as deepeval_eval
from evaluation.evaluation import Evaluation
class DeepevalFramework(BaseEvaluationFramework):

    def __init__(self) -> None:
        super().__init__()

    
    def evaluate(self, eval_name,framework="DeepevalFramework",**kwargs):
        """
        A wrapper for the Deepeval evaluate function. Use this function instead of Deepeval's evaluate function with the usual parameters to automatically generate an evaluation that
        can then be exported to coai.

        :param eval_name: The name of the evaluation.
        :param framework: The name of the framework if a specific name is required. Defaults to DeepevalFramework.
        :return: An Evaluation object containing the evaluation results.
        """
        evaluation = Evaluation(name=eval_name,framework=framework)
        evaluation.data["test_results"] = []
        deepeval_results = deepeval_eval(**kwargs)
        success_count = 0
        for result in deepeval_results:
            evaluation.data["test_results"].append(object_to_dict(result))
            if result.success:
                success_count += 1
        evaluation.data["total_score"] = success_count / len(deepeval_results)
        evaluation.data["total_tests"] = len(deepeval_results)
        return evaluation
    

def object_to_dict(obj):
    """
    A utility function that takes an object of any type and recursively transforms it into a dict so that nested objects also get transformed.

    :param obj: The object to transform.
    :return: The transformed object as a dictionary-
    """
    if hasattr(obj, "__dict__"):
        data = {}
        for key, value in obj.__dict__.items():
            if isinstance(value, list):
                data[key] = [object_to_dict(item) for item in value]
            else:
                data[key] = object_to_dict(value)
        return data
    else:
        return obj