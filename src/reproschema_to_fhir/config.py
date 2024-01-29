import os
from dotenv import load_dotenv


class Config:

    def __init__(self):
        load_dotenv()
        self.CODESYSTEM_URI = os.getenv('CODESYSTEM_URI')
        self.VALUESET_URI = os.getenv('VALUESET_URI')
        self.QUESTIONNAIRE_URI = os.getenv('QUESTIONNAIRE_URI')
        self.LANGUAGE = str(os.getenv('QUESTIONNAIRE_LANGUAGE'))
        self.MODE = os.getenv('FHIR_QUESTIONNAIRE_MODE')


    def get_questionnaire(self):
        return self.QUESTIONNAIRE_URI

    def get_valueset(self):
        return self.VALUESET_URI

    def get_codesystem(self):
        return self.CODESYSTEM_URI

    def get_language(self):
        return self.LANGUAGE
    
    def get_mode(self):
        return self.MODE

    def set_questionnaire(self, questionnaire):
        self.QUESTIONNAIRE_URI = questionnaire

    def set_valueset(self, valueset_uri):
        self.VALUESET_URI = valueset_uri

    def set_codesystem(self, codesystem_uri):
        self.CODESYSTEM_URI = codesystem_uri

    def set_language(self, language):
        self.LANGUAGE = language
    
    def set_mode(self, mode):
        self.MODE = mode