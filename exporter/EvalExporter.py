from evaluation.evaluation import Evaluation
from typing import List
import requests
from config.config import Config
import uuid 
from datetime import datetime
from dotenv import load_dotenv
load_dotenv(override=True)
import os

BACKEND_API_URL = os.getenv("BACKEND_API_URL")
class EvalExporter():

    def __init__(self, title) -> None:
        """
        Initialize the EvalExporter instance.
        
        :param title: Title for the evaluation export session.
        """
        self.evaluations: List[Evaluation] = []
        self.evaluation_title = title
        self.evaluations_id = str(uuid.uuid4())

    def export(self, eval: Evaluation = None):
        """
        Exports the stored evaluations in self.evaluations to the MongoDB.
        :param eval: Evaluation to export. If None is provided, all stored evaluations get exported.
        """
        try:
            #api_url = "http://127.0.0.1:8000/api/export_evaluations"
            api_url = f"{BACKEND_API_URL}/api/export_evaluations"
            exported_count = 0
            if eval:
                if eval not in self.evaluations:
                    print (f"{eval.id} - {eval.name} is not an element of currently stored evaluations. Please use EvalExporter.add_eval(eval=your_eval) to add your evaluation before exporting.")
                    return
                else:
                    params = {"user_id": Config.user_id, "project_id": Config.project_id, "date": datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ"),"evaluation_id": self.evaluations_id, "evaluations_title": self.evaluation_title, "eval_id": eval.id, "eval_name": eval.name, "eval_framework": eval.framework}
                    data={"eval_data" : eval.data}
                    response = requests.post(api_url, params=params, json=data)

                    if response.status_code == 200:
                        print(f"Successfully exported {eval.id} - {eval.name}")
                        exported_count += 1
                    else:
                        print(f"Failed to export{eval.id} - {eval.name}. Status code: {response.status_code}, Response content: {response.content}")
                    self.evaluations.remove(eval)
                    return
            else:
                for eval_to_export in self.evaluations:
                    params = {"user_id": Config.user_id, "project_id": Config.project_id,"date":datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ"), "evaluation_id": self.evaluations_id, "evaluations_title": self.evaluation_title,"eval_id": eval_to_export.id, "eval_name": eval_to_export.name,"eval_framework": eval_to_export.framework}
                    data={"eval_data" : eval_to_export.data}
                    response = requests.post(api_url, params=params, json=data)

                    if response.status_code == 200:
                        print(f"Successfully exported {eval_to_export.id} - {eval_to_export.name}")
                        exported_count += 1
                    else:
                        print(f"Failed to export {eval_to_export.id} - {eval_to_export.name}. Status code: {response.status_code}, Response content: {response.content}")
                    self.evaluations.remove(eval_to_export)
                print(f"Successfully exported {exported_count} evaluations.")
        except Exception as e:
            print(str(e))

         

    def add_eval(self, eval: Evaluation):
        """
        Add an evaluation to the list of evaluations to be exported.
        
        :param eval: Evaluation object to add.
        """
        if any(eval_obj.id == eval.id for eval_obj in self.evaluations):
            print(f"Evaluation with ID {eval.id} already exists in currently stored evaluations of the EvalExporter.")
            return
        else:
            self.evaluations.append(eval)
            print(f"Evaluation with ID {eval.id} stored in EvalExporter")
    
    def clear(self):
        """
        Clear all evaluations from the exporter.
        """
        self.evaluations = []
        print("Emptied evaluation list")

    def remove(self, eval: Evaluation):
        """
        Remove a specific evaluation from the list.
        
        :param eval: Evaluation object to remove.
        """
        if eval in self.evaluations:
            self.evaluations.remove(eval)
            print(f"Successfully removed {eval.id} - {eval.name} from EvalExporter")
        else:
            print(f"{eval.id} - {eval.name} is not an element of currently stored evaluations")
             