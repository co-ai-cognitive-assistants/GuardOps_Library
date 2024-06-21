import subprocess
from typing import Dict, List, Any
from flow_executor.component_mapping import COMPONENT_MAPPING
from flow_executor.demo_definition import FLOW_DEFINITION
from pprint import pprint

BASE_IMPORTS_FOR_CODE = [
"from coai_datasets.dataset_manager import DatasetManager",
"from coai_datasets.standard import *",
"from config.config import Config",
"from evaluation.metrics import BLEUMetric, Rouge1Metric",
"from evaluation import *",
"from exporter.EvalExporter import EvalExporter",
"from models.openai_model import OpenAIModel"
]

def run_format(line, variables):
    try: 
        #for debugging, remove the comments for the print statements
        valid_variables = {k: v for k, v in variables.items() if k in line}
        #print(f"attempting to format line: \n{line} \nwith variables: \n{valid_variables}")
        line = line.format_map(valid_variables)
        #print(f"final result: ")
        #print(f"{line}")
        #print("\n")
        return line
    except KeyError as e:
        return 

def group_edges(edges):
    # Create an empty dictionary to hold grouped data
    grouped_data = {} 
    #Group the edges by their target component and add the relevant variable names for model, exporter, dataset, framework
    for item in edges:
        target = item["target"].replace('-','')
        
        item["target"] = item["target"].replace('-','')
        item["source"] = item["source"].replace('-','')   
        if "dataset" in item["sourceHandle"]:
            item["dataset"] = item["source"]
        if "model" in item["sourceHandle"]:
            item["model"] = item["source"]    
        if "exporter" in item["targetHandle"]:
            item["exporter"] = item["target"]
            dataset_reference_edges = grouped_data[item["source"]]
            for dataset_item in dataset_reference_edges:
                item["dataset"] = dataset_item["dataset"]
        if "framework" in item["sourceHandle"]:
            item["framework"] = item["source"]
        #dummy for now:
        item["model"]="dummy"
        if target not in grouped_data:
            grouped_data[target] = []
        grouped_data[target].append(item)
    return grouped_data


def generate_python_script(components: Dict[Any,Any]):
    script_lines = BASE_IMPORTS_FOR_CODE
    config_values = {}
    for component in components["nodes"]:
        # store the id of the current component since this gets overridden to a non unique id if the following condition is true
        variable_name = component["id"].replace('-','')
        config_values[variable_name] = {}
        # if multiple instances of the same flow component exist, the actual definition is in the data key (this now means that the id of the component is no longer unique which is why it was stored before doing this)
        if "data" in component.keys():
            component = component["data"]
        mapping = COMPONENT_MAPPING[component["id"]]
        
        if "fields" in component.keys():
            #populate the field values for each variable and put them in a dict of pattern field_name:field_value
            for field in component["fields"]:
                field_name = field["name"]
                field_value = field["value"]
                config_values[f"{variable_name}"][field_name]=field_value
        if "creation_lines" in mapping.keys():
            #create the instances of every component in the flow with its respective field values and variable names stored in the config_values dict
            for line in mapping["creation_lines"]:
                if mapping.get("instance"):
                    config_values[variable_name]["id"]=variable_name
                line = run_format(line, config_values[variable_name])
                script_lines.append(line)
    #group the edges by target so that for every target component you get all the inputs in one dict instead of having it spread out makes further processing easier
    edges_dict = group_edges(components["edges"])
    #pprint(edges_dict)
    for component in components["nodes"]:
        #some components get exported with their component id (if it is an exporter, mlsumdataset, config etc.) in data.id and some have them just in id even though id needs to be the unique id 
        if "data" in component.keys():
            mapping = COMPONENT_MAPPING[component["data"]["id"]]
        else:
            mapping = COMPONENT_MAPPING[component["id"]]
        
        if "execution_lines" in mapping.keys():
            for variable, edges in edges_dict.items():
                for edge in edges:
                    #keep count of how many lines are actually added for execution. preparation to not include wrongly generated lines
                    count = 0
                    temp_lines = []
                    for line in mapping.get("execution_lines"):
                        config_values[variable].update(edge)
                        line = run_format(line, config_values[variable])
                        # every variables edges get computed even though they are not actually exporter variables. only two lines get returned by non exporter variables that should not be generated, thus just keeping count works
                        if line:
                            count += 1
                            temp_lines.append(line)
                            if count > 2:
                                for temp_line in temp_lines:
                                    script_lines.append(temp_line)
    
    return "\n".join(script_lines)

def save_generated_code(code, filename='generated_script.py'):
    with open(filename, 'w') as file:
        file.write(code)
        file.close()
    
generated_code = generate_python_script(FLOW_DEFINITION)

save_generated_code(generated_code)