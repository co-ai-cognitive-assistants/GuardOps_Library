from opentelemetry.sdk.trace.export import BatchSpanProcessor, SpanExporter
import json
from config.config import Config
import requests
import hashlib
from tracing.prompt_response_extractor import extract_response, extract_prompt, extract_model
import os
from dotenv import load_dotenv
load_dotenv(override=True)

BACKEND_API_URL = os.getenv("BACKEND_API_URL")


class JSONProcessor(BatchSpanProcessor):
    """
    A BatchSpanProcessor that additionally keeps track of all the spans in an array to then export this array into the MongoDB
    """

    def __init__(self, config, span_exporter: SpanExporter, max_queue_size: int = None, schedule_delay_millis: float = None, max_export_batch_size: int = None, export_timeout_millis: float = None):
        super().__init__(span_exporter, max_queue_size, schedule_delay_millis, max_export_batch_size, export_timeout_millis)
        self.traces = []
        self.config: Config = config
        self.trace_ids = []

    def on_end(self, export_span):
        """
        This function gets automatically executed after every span is finished. 
        The span is then added to the traces buffer list for MongoDB export in the clean function.
        Also filters out non LLM traces.
        """
        export_span_dict = json.loads(export_span.to_json())
        if export_span_dict["name"] == "GET" or export_span_dict["name"] == "POST":
            pass
        else:
            export_span_dict = replace_dots_recursive(export_span_dict)
            export_span_dict["attributes"]["response"] = json.dumps(export_span_dict["attributes"])
            export_span_dict["attributes"]["output"] = extract_response(export_span_dict)
            export_span_dict["attributes"]["prompt"] = extract_prompt(export_span_dict)
            export_span_dict["attributes"]["model"] = extract_model(export_span_dict)


            self.traces.append(export_span_dict)
            self.clean()

    def clean(self,  key: str=None, project_id=None, user=None,playground_id=None):
        """
        A function that stores the relevant spans in MongoDB and refreshes the buffers to avoid excessive memory use.
        This function gets called after every span ends.
        """
        
        key=self.config.tracing_key
        project_id=self.config.project_id
        user=self.config.user_id
        main_trace = ""
        
        # store the spans
        for span_dict in self.traces:
            trace_id = span_dict["context"]["trace_id"]
            main_trace = trace_id
        # Insert the trace and access token in the Traces collection and clear the traces list     
            if main_trace not in self.trace_ids:   
                trace_dict = {"trace_id": main_trace, "access_token": key,"project_id":project_id,"playground_id":playground_id}
                data={"span":span_dict,"trace":trace_dict}
            else:
                data={"span":span_dict}
            response = requests.post(url=f"{BACKEND_API_URL}/api/store_trace/",params={"user_id":user,"project_id":project_id,"key_hash":hashlib.sha256(key.encode("utf-8")).hexdigest()},json=data)
            print(response.content)
            self.trace_ids.append(main_trace)
        self.traces = []

def replace_dots_recursive(obj):
    """
    MongoDB can't store keys that have dots in them. This function replaces the dots with underscores.
    """
    if isinstance(obj, dict):
        return {key.replace('.', '_'): replace_dots_recursive(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [replace_dots_recursive(element) for element in obj]
    else:
        return obj

def process_response(response, current_span):
    """
    A function that takes the response and current span as input. 
    Iterates recursively through the response dict and stores every key: value pair where the value is no longer a dict or list as attributes.
    This is needed because OpenTelemetry attributes can only be of primitive types e.g string or int but not dict.
    """
    if isinstance(response, str):
        current_span.set_attribute("response",response)
    else:
        if not isinstance(response, dict):
            response = dict(response)
        for key, value in response.items():
            if isinstance(value, dict):
                # If the value is a dictionary, recursively process it
                process_response(value, current_span)
            elif isinstance(value, list):
                # If the value is a list, recursively process it
                for item in value:
                    process_response(item, current_span)
            else:
                # If the value is not a dictionary or a list, set the attribute            
                current_span.set_attribute(key, value)
