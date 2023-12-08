import os
from dotenv import load_dotenv
class Config:
    def __init__(self):
        load_dotenv()
        self.CODESYSTEM_URI = os.getenv('CODESYSTEM_URI')
        self.VALUESET_URI = os.getenv('VALUESET_URI')
        self.QUESTIONNAIRE_URI = os.getenv('QUESTIONNAIRE_URI')

    def get_questionnaire(self):
        return self.QUESTIONNAIRE_URI