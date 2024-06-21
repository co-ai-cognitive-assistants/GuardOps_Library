from tqdm import tqdm
from evaluation.BaseEvaluationFramework import BaseEvaluationFramework
from coai_datasets.standard.mmlu_dataset import MMLUDataset
from models.base_model import BaseModel
from evaluation.evaluation import Evaluation


class MMLUFramework(BaseEvaluationFramework):
    """
    A framework for evaluating models on the MMLU dataset.

    This class provides the methods to load the MMLU dataset, evaluate a model's performance on it,
    and generate an Evaluation object containing the results.
    """

    def __init__(self) -> None:
        super().__init__()

    def evaluate(self, model: BaseModel, eval_name,  **kwargs):
        """
        Evaluate the model on the MMLU dataset.

        This method loads the MMLU dataset, performs predictions using the provided model,
        compares the predictions with the correct answers, and calculates the evaluation score.

        :param model: The model to be evaluated. It should be an instance of BaseModel.
        :param eval_name: The name of the evaluation.
        :param kwargs: Additional keyword arguments for future extensions.
        
        :return: An Evaluation object containing the evaluation results.
        """
        # Load the MMLU dataset
        dataset = MMLUDataset()
        dataset.load()

        # Create an Evaluation object
        evaluation = Evaluation(name=eval_name, framework=self.__class__.__name__)
        
        # List to store model's predictions
        prediction_choices = []

        #Get a sample of thye dataset for evaluation
        sample = dataset.data.head(2)
        total=len(sample)

        # Progress bar for monitoring evaluation progress
        with tqdm(total=total, desc="Evaluating") as progress_bar:
            for index,row in sample.iterrows():
            #for index,row in dataset.data.iterrows():
                question = row["question"]
                choices = row["choices"]

                # Make prediction using the model
                prediction_choices.append(model.predict(
                    input_text=f"This is your question: {question} and these are your answer choices: {choices}. Reply with the number of the correct choice. You should only respond with the number and nothing else."
                    )
                )
                progress_bar.update(1)
        
        # Compare predictions with the correct answers
        correct_predictions = sample['answer'] == prediction_choices
        #correct_predictions =  dataset.data['answer'] == prediction_choices
        
        # Calculate the score
        results = {}
        results["Score"] = (correct_predictions.sum() / len(sample)) * 100
        #results["Score"] = (correct_predictions.sum() / len(dataset.data)) * 100
        
        # Store the results in the Evaluation object
        evaluation.data = results
        return evaluation
    
    def help(self):
        """
        Provide help and explanations about the MMLUFramework.

        This method returns a string containing detailed information on what the framework does,
        what it is based on, and how to use it.

        :return: A help string explaining the MMLUFramework.
        """
        explanation = """
        The MMLUFramework is designed to evaluate models on the MMLU dataset.
        It loads the dataset, performs predictions using the provided model,
        and calculates the score based on the accuracy of the model's predictions.
        
        Usage:
        - Initialize the framework.
        - Call the evaluate method with the model and evaluation name.
        - Retrieve the Evaluation object for the results.
        """
        return explanation
    