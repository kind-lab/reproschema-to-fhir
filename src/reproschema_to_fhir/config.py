import os
from dotenv import load_dotenv


class Config:

    def __init__(self):
        load_dotenv()
        self.CODESYSTEM_URI = os.getenv('CODESYSTEM_URI')
        self.VALUESET_URI = os.getenv('VALUESET_URI')
        self.QUESTIONNAIRE_URI = os.getenv('QUESTIONNAIRE_URI')
        #print(os.getenv('LANG'))
        self.LANGUAGE = str(os.getenv('QUESTIONNAIRE_LANGUAGE'))

    def get_questionnaire(self):
        return self.QUESTIONNAIRE_URI

    def get_valueset(self):
        return self.VALUESET_URI

    def get_codesystem(self):
        return self.CODESYSTEM_URI

    def get_language(self):
        return self.LANGUAGE