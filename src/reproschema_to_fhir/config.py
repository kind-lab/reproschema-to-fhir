import os

class Config:
    def __init__(self):
        self.CODESYSTEM_URI = os.getenv('CODESYSTEM_URI')
        self.VALUESET_URI = os.getenv('VALUESET_URI')
        self.QUESTIONNAIRE_URI = os.getenv('QUESTIONNAIRE_URI')