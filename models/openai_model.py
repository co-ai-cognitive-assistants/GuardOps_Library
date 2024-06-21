from openai import OpenAI
from models.base_model import BaseModel

class OpenAIModel(BaseModel):
    def __init__(self, api_key, model_name, base_url="https://api.openai.com/v1/chat/completions"):
        """
        :param api_key: API key for OpenAI.
        :param model_name: Name of the OpenAI model (e.g., 'gpt-3.5-turbo').
        :param base_url: Base URL for the OpenAI API. Defaults to https://api.openai.com/v1/chat/completions.
        """
        self.api_key = api_key
        self.base_url = base_url
        self.model_name = model_name

    def predict(self, input_text):
        """
        Generates a prediction using the OpenAI model.

        :param input_text: A string containing the input text.
        
        :return: A string containing the model's prediction.
        """
        client = OpenAI(
                api_key = self.api_key,
                base_url=self.base_url
            )
        model = self.model_name
        messages = [{"role": "user", "content": input_text}]
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.0,
            max_tokens=500,
            stop=["###"],
            stream=False,
        )
        return response.choices[0].message.content.strip()




