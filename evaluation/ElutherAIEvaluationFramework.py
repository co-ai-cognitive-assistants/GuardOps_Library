from evaluation.BaseEvaluationFramework import BaseEvaluationFramework
from lm_eval.evaluator import simple_evaluate , evaluate
from evaluation.evaluation import Evaluation


class ElutherAIEvaluationFramework(BaseEvaluationFramework):
    """
    An evaluation framework for models using the ElutherAI evaluation toolkit.

    This framework provides an implementation of the `evaluate` method using the `simple_evaluate`
    function from the lm_eval library. 
    """
    def __init__(self) -> None:
        super().__init__()

    def evaluate(self, model_type, model_args, eval_name, tasks, batch_size="auto", device="cuda:1", output_path="result.json"):
        """
        Evaluate the given model using the specified parameters and tasks. 

        This method runs the ElutherAI evaluation using the `simple_evaluate` function and calculates
        accuracy metrics for the specified tasks. The results are formatted and returned as an Evaluation object.

        :param model_type: The type of the model to be evaluated. (e.g., hf)
        :param model_args: Arguments for the model.
        :param eval_name: The name of the evaluation.
        :param tasks: A list of tasks to evaluate the model on. (e.g., arc_easy, arc_medium)
        :param batch_size: Optional; the batch size to use during evaluation (default is "auto").
        :param device: Optional; the device to use for evaluation (default is "cuda:1").
        :param output_path: Optional; the path to save the evaluation results (default is "result.json").

        :return: An Evaluation object containing the formatted results and average accuracy. #This will contain the evaluation results with accuracy in percentages 
        """

        # Run lm_eval using simple_evaluate function
        results = simple_evaluate(
            model=model_type,
            model_args=model_args,
            tasks=tasks,
            batch_size=batch_size,
            device=device
        )

        # Extract results
        results = results.get("results", {})

        # Initialize variables to calculate average
        total_acc_none = 0
        total_tasks = 0

        # Iterate through each task (e.g., arc_easy, arc_medium)
        formatted_results = {}
        for task, task_info in results.items():
            # Extract accuracy information for "acc,none"
            acc_none = task_info.get("acc,none")
            if acc_none is not None:
                formatted_results[task] = {"Accuracy (acc,none)": acc_none}
                total_acc_none += acc_none
                total_tasks += 1

        # Calculate average accuracy
        if total_tasks > 0:
            average_acc_none = total_acc_none / total_tasks
            formatted_results["Average Accuracy (acc,none)"] = average_acc_none

        # Create an Evaluation object and return it
        evaluation = Evaluation(name=eval_name, framework=self.__class__.__name__)
        evaluation.data = formatted_results
        return evaluation

    def help(self):
        explanation = (
            "The ElutherAIEvaluationFramework is designed to evaluate models using the ElutherAI evaluation toolkit."
            "It leverages the `simple_evaluate` function from the lm_eval library to assess model performance on a variety of tasks."

            "Parameters:\n"

            "- model_type: The type of the model to be evaluated. This should be compatible with the lm_eval toolkit.\n"
            "- model_args: Arguments for the model, such as configuration details or initialization parameters.\n"
            "- eval_name: A string representing the name of the evaluation. This is used to label the results.\n"
            "- tasks: A list of tasks to evaluate the model on. These tasks should be defined within the lm_eval toolkit.\n"
            "- batch_size: Optional; the batch size to use during evaluation. Default is 'auto'.\n"
            "- device: Optional; the device to use for evaluation, such as 'cuda:1' for a specific GPU. Default is 'cuda:1'.\n"
            "- output_path: Optional; the path to save the evaluation results in JSON format. Default is 'result.json'.\n\n"

            "The `evaluate` method calculates the accuracy for each specified task and computes an average accuracy across all tasks. "
            "The results are returned as an Evaluation object, which includes the formatted results and the average accuracy."
        )
        return explanation

"""Here's how to use it:

    python
    framework = ElutherAIEvaluationFramework()
    evaluation = framework.evaluate(
        model_type="hf",
        model_args={"pretrained": "/modelcache/vicuna-13b"},
        eval_name="arc_easy_evaluation",
        tasks=["arc_easy", "hellaswag"],
        batch_size="auto",
        device="cuda:1",
        output_path="result.json"
    )

    print(evaluation.data)  # This will contain the evaluation results with accuracy in percentages
"""

