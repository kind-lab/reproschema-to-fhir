import unittest
from reproschema_to_fhir.fhir import add_options, Config, generate_code_system, generate_value_set

class TestReprotoFhir(unittest.TestCase):
    def testcase_1_add_options(self):
        codesystem_uri = "https://voicecollab.ai/fhir/CodeSystem/"
        valueset_uri = "https://voicecollab.ai/fhir/ValueSet/"
        questionnaire_uri = "https://voicecollab.ai/fhir/Questionnaire/"
        language = "en"
        mode = "ValueSet"
        config = Config()
        config.set_questionnaire(questionnaire_uri)
        config.set_valueset(valueset_uri)
        config.set_codesystem(codesystem_uri)
        config.set_language(language)
        config.set_mode(mode)

        options = {'valueType': 'xsd:integer', 'choices': [{'name': 'No', 'value': 0}, {'name': 'Yes', 'value': 1}, {'name': 'Not certain', 'value': 2}]}
        output = add_options(options, config)
        sol = ["No", "Yes", "Not certain"]
        self.assertEqual(sol, output)


    def testcase_2_codesystems(self):
        codesystem_uri = "https://voicecollab.ai/fhir/CodeSystem/"
        valueset_uri = "https://voicecollab.ai/fhir/ValueSet/"
        questionnaire_uri = "https://voicecollab.ai/fhir/Questionnaire/"
        language = "en"
        mode = "ValueSet"
        config = Config()
        config.set_questionnaire(questionnaire_uri)
        config.set_valueset(valueset_uri)
        config.set_codesystem(codesystem_uri)
        config.set_language(language)
        config.set_mode(mode)

        options = {'valueType': 'xsd:integer', 'choices': [{'name': 'No ', 'value': 0}, {'name': 'Yes ', 'value': 1}, {'name': 'Not certain', 'value': 2}]}
        id = "diagnosis-vfp-gsd"
        
        expected_codesystem = {'resourceType': 'CodeSystem', 'id': 'diagnosis-vfp-gsd', 'text': {'status': 'generated', 'div': '<div xmlns="http://www.w3.org/1999/xhtml">Placeholder</div>'}, 'url': 'https://voicecollab.ai/fhir/CodeSystem/diagnosis-vfp-gsd', 'version': '1.4.0', 'name': 'Diagnosis-vfp-gsd', 'title': 'diagnosis-vfp-gsd', 'status': 'active', 'date': '2024-01-29T19:50:09Z', 'publisher': 'KinD Lab', 'contact': [{'name': 'KinD Lab', 'telecom': [{'system': 'url', 'value': 'http://fhir.kindlab.sickkids.ca'}]}], 'description': 'diagnosis-vfp-gsd', 'caseSensitive': True, 'content': 'complete', 'count': 3, 'concept': [{'code': '0', 'display': 'No '}, {'code': '1', 'display': 'Yes '}, {'code': '2', 'display': 'Not certain'}]}
        expected_options = ['No ', 'Yes ', 'Not certain']
        
        actual_codesystem, actual_options = generate_code_system(options, id, config)
        actual_codesystem["date"] = '2024-01-29T19:50:09Z' # time is hardcoded to avoid error as function takes the current time

        self.assertEqual((expected_codesystem, expected_options) , (actual_codesystem, actual_options))


    def testcase_3_codesystems(self):
        codesystem_uri = "https://voicecollab.ai/fhir/CodeSystem/"
        valueset_uri = "https://voicecollab.ai/fhir/ValueSet/"
        questionnaire_uri = "https://voicecollab.ai/fhir/Questionnaire/"
        language = "en"
        mode = "AnswerOptions" # changing modes 
        config = Config()
        config.set_questionnaire(questionnaire_uri)
        config.set_valueset(valueset_uri)
        config.set_codesystem(codesystem_uri)
        config.set_language(language)
        config.set_mode(mode)


        
        options = {'valueType': 'xsd:integer', 'choices': [{'name': 'No ', 'value': 0}, {'name': 'Yes ', 'value': 1}, {'name': 'Not certain', 'value': 2}]}
        id = "diagnosis-vfp-gsd"
        # codesystem shouldn't be generated in answerOption mode
        self.assertEqual(dict(), generate_code_system(options, id, config))

    def testcase_4_valuesets(self):
        codesystem_uri = "https://voicecollab.ai/fhir/CodeSystem/"
        valueset_uri = "https://voicecollab.ai/fhir/ValueSet/"
        questionnaire_uri = "https://voicecollab.ai/fhir/Questionnaire/"
        language = "en"
        mode = "ValueSet"
        config = Config()
        config.set_questionnaire(questionnaire_uri)
        config.set_valueset(valueset_uri)
        config.set_codesystem(codesystem_uri)
        config.set_language(language)
        config.set_mode(mode)
        id = "diagnosis-vfp-gsd"
        actual = generate_value_set(id, config)
        actual["date"] = '2024-1-1'  # hardcoded date as norally date is set to real time
        expected = {'resourceType': 'ValueSet', 'id': 'diagnosis-vfp-gsd', 'text': {'status': 'generated', 'div': '<div xmlns="http://www.w3.org/1999/xhtml">Placeholder</div>'}, 'url': 'https://voicecollab.ai/fhir/ValueSet/diagnosis-vfp-gsd', 'version': '1.4.0', 'name': 'Diagnosis-vfp-gsd', 'title': 'diagnosis-vfp-gsd', 'status': 'active', 'date': '2024-1-1', 'publisher': 'KinD Lab', 'contact': [{'name': 'KinD Lab', 'telecom': [{'system': 'url', 'value': 'http://fhir.kindlab.sickkids.ca'}]}], 'description': 'diagnosis-vfp-gsd', 'compose': {'include': [{'system': 'https://voicecollab.ai/fhir/CodeSystem/diagnosis-vfp-gsd'}]}}
        
        self.assertEqual(expected, actual)


    def testcase_5_valuesets(self):
        codesystem_uri = "https://voicecollab.ai/fhir/CodeSystem/"
        valueset_uri = "https://voicecollab.ai/fhir/ValueSet/"
        questionnaire_uri = "https://voicecollab.ai/fhir/Questionnaire/"
        language = "en"
        mode = "AnswerOptions" # mode change
        config = Config()
        config.set_questionnaire(questionnaire_uri)
        config.set_valueset(valueset_uri)
        config.set_codesystem(codesystem_uri)
        config.set_language(language)
        config.set_mode(mode)
        id = "diagnosis-vfp-gsd"
        actual = generate_value_set(id, config)
       
        self.assertEqual(dict(), actual)







if __name__ == '__main__':
    unittest.main()