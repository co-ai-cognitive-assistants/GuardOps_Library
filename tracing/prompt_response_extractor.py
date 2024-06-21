from enum import Enum
import re

PROMPT_DEFINITIONS = [
    r'llm_prompts_\d+_content',
    r'gen_ai_prompt_\d+_content'

]

RESPONSE_DEFINITIONS = [
    r'llm_completions_\d+_content',
    r'gen_ai_completion_\d+_content'
]

MODEL_DEFINITIONS = [
    "llm_response_model",
    "gen_ai_response_model"
]


def extract_response(span):
    response = ""
    for key in span["attributes"].keys():
        for pattern in RESPONSE_DEFINITIONS:
            if re.match(pattern, key):
                response += span["attributes"][key]
                response += "\n"
    return response

def extract_prompt(span):
    response = ""
    for key in span["attributes"].keys():
        for pattern in PROMPT_DEFINITIONS:
            if re.match(pattern, key):
                response +=  span["attributes"][key]
                response += "\n"
    return response

def extract_model(span):
      model = ""
      for model_definition in MODEL_DEFINITIONS:
        if model_definition in span["attributes"].keys():
            model = span["attributes"][model_definition]
      return model