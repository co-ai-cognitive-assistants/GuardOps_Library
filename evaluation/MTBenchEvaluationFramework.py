from evaluation.BaseEvaluationFramework import BaseEvaluationFramework
from evaluation.evaluation import Evaluation
from typing import List

class MTBenchEvaluationFramework(BaseEvaluationFramework):
    def __init__(self) -> None:
        self.evaluations: List[Evaluation] = []
        

    def evaluate(self, model, dataset,eval_name, **kwargs):
        evaluation = Evaluation(name=eval_name)
        results = {}
        evaluation.framework = self.__class__.__name__
        evaluation.data = results
        self.evaluations.append(evaluation)
    
    def help(self):
        return super().help()