import uuid
class Evaluation():

    def __init__(self, name, framework) -> None:
        self.id = str(uuid.uuid4())
        self.name = name
        self.framework = framework
        self.data = {}

    def __repr__(self) -> str:
        return f"ID: {self.id} - Name: {self.name} - Framework: {self.framework} - Data: {self.data}"

