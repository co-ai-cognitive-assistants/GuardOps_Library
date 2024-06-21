class Config:
    user_id = None
    project_id = None
    tracing_key = None

    @classmethod
    def set_user_id(cls, user_id):
        cls.user_id = user_id

    @classmethod
    def set_project_id(cls, project_id):
        cls.project_id = project_id
        
    @classmethod
    def set_api_key(cls, api_key):
        cls.api_key = api_key

    @classmethod
    def set_tracing_key(cls,tracing_key):
        cls.tracing_key = tracing_key