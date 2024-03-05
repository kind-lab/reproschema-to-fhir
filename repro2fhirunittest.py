import pytest
from reproschema_to_fhir.fhir import add_options, add_enable_when, Config, generate_code_system, generate_value_set, QuestionnaireGenerator
from collections import OrderedDict


def test_add_options():
    codesystem_uri = "https://voicecollab.ai/fhir/CodeSystem/"
    valueset_uri = "https://voicecollab.ai/fhir/ValueSet/"
    questionnaire_uri = "https://voicecollab.ai/fhir/Questionnaire/"
    language = "en"
    mode = "ValueSet"
    config = Config()
    config.QUESTIONNAIRE_URI = questionnaire_uri
    config.VALUESET_URI = valueset_uri
    config.CODESYSTEM_URI = codesystem_uri
    config.LANGUAGE = language
    config.MODE = mode

    options = {'valueType': 'xsd:integer', 'choices': [{'name': 'No', 'value': 0}, {
        'name': 'Yes', 'value': 1}, {'name': 'Not certain', 'value': 2}]}
    actual = add_options(options, config)
    expected = ["No", "Yes", "Not certain"]
    assert expected == actual


def test_generate_codesystem_in_valueset_mode():
    codesystem_uri = "https://voicecollab.ai/fhir/CodeSystem/"
    valueset_uri = "https://voicecollab.ai/fhir/ValueSet/"
    questionnaire_uri = "https://voicecollab.ai/fhir/Questionnaire/"
    language = "en"
    mode = "ValueSet"
    config = Config()
    config.QUESTIONNAIRE_URI = questionnaire_uri
    config.VALUESET_URI = valueset_uri
    config.CODESYSTEM_URI = codesystem_uri
    config.LANGUAGE = language
    config.MODE = mode

    options = {'valueType': 'xsd:integer', 'choices': [{'name': 'No ', 'value': 0}, {
        'name': 'Yes ', 'value': 1}, {'name': 'Not certain', 'value': 2}]}
    id = "diagnosis-vfp-gsd"

    expected_codesystem = {'resourceType': 'CodeSystem', 'id': 'diagnosis-vfp-gsd', 'text': {'status': 'generated', 'div': '<div xmlns="http://www.w3.org/1999/xhtml">Placeholder</div>'}, 'url': 'https://voicecollab.ai/fhir/CodeSystem/diagnosis-vfp-gsd', 'version': '1.4.0', 'name': 'Diagnosis-vfp-gsd', 'title': 'diagnosis-vfp-gsd', 'status': 'active', 'date': '2024-01-29T19:50:09Z',
                           'publisher': 'KinD Lab', 'contact': [{'name': 'KinD Lab', 'telecom': [{'system': 'url', 'value': 'http://fhir.kindlab.sickkids.ca'}]}], 'description': 'diagnosis-vfp-gsd', 'caseSensitive': True, 'content': 'complete', 'count': 3, 'concept': [{'code': '0', 'display': 'No '}, {'code': '1', 'display': 'Yes '}, {'code': '2', 'display': 'Not certain'}]}
    expected_options = ['No ', 'Yes ', 'Not certain']

    actual_codesystem, actual_options = generate_code_system(
        options, id, config)
    # time is hardcoded to avoid error as function takes the current time
    actual_codesystem["date"] = '2024-01-29T19:50:09Z'

    assert (expected_codesystem, expected_options) == (
        actual_codesystem, actual_options)


def test_codesystem_not_generated_for_answeroption():
    codesystem_uri = "https://voicecollab.ai/fhir/CodeSystem/"
    valueset_uri = "https://voicecollab.ai/fhir/ValueSet/"
    questionnaire_uri = "https://voicecollab.ai/fhir/Questionnaire/"
    language = "en"
    mode = "AnswerOptions"  # changing modes
    config = Config()
    config.QUESTIONNAIRE_URI = questionnaire_uri
    config.VALUESET_URI = valueset_uri
    config.CODESYSTEM_URI = codesystem_uri
    config.LANGUAGE = language
    config.MODE = mode

    options = {'valueType': 'xsd:integer', 'choices': [{'name': 'No ', 'value': 0}, {
        'name': 'Yes ', 'value': 1}, {'name': 'Not certain', 'value': 2}]}
    id = "diagnosis-vfp-gsd"
    # codesystem shouldn't be generated in answerOption mode
    assert (dict() == generate_code_system(options, id, config))


def test_generate_valueset_in_valueset_mode():
    codesystem_uri = "https://voicecollab.ai/fhir/CodeSystem/"
    valueset_uri = "https://voicecollab.ai/fhir/ValueSet/"
    questionnaire_uri = "https://voicecollab.ai/fhir/Questionnaire/"
    language = "en"
    mode = "ValueSet"
    config = Config()
    config.QUESTIONNAIRE_URI = questionnaire_uri
    config.VALUESET_URI = valueset_uri
    config.CODESYSTEM_URI = codesystem_uri
    config.LANGUAGE = language
    config.MODE = mode
    id = "diagnosis-vfp-gsd"
    actual = generate_value_set(id, config)
    # hardcoded date as norally date is set to real time
    actual["date"] = '2024-1-1'
    expected = {'resourceType': 'ValueSet', 'id': 'diagnosis-vfp-gsd', 'text': {'status': 'generated', 'div': '<div xmlns="http://www.w3.org/1999/xhtml">Placeholder</div>'}, 'url': 'https://voicecollab.ai/fhir/ValueSet/diagnosis-vfp-gsd', 'version': '1.4.0', 'name': 'Diagnosis-vfp-gsd', 'title': 'diagnosis-vfp-gsd',
                'status': 'active', 'date': '2024-1-1', 'publisher': 'KinD Lab', 'contact': [{'name': 'KinD Lab', 'telecom': [{'system': 'url', 'value': 'http://fhir.kindlab.sickkids.ca'}]}], 'description': 'diagnosis-vfp-gsd', 'compose': {'include': [{'system': 'https://voicecollab.ai/fhir/CodeSystem/diagnosis-vfp-gsd'}]}}

    assert (expected == actual)


def test_valueset_not_generated_for_answeroption():
    codesystem_uri = "https://voicecollab.ai/fhir/CodeSystem/"
    valueset_uri = "https://voicecollab.ai/fhir/ValueSet/"
    questionnaire_uri = "https://voicecollab.ai/fhir/Questionnaire/"
    language = "en"
    mode = "AnswerOptions"  # mode change
    config = Config()
    config.QUESTIONNAIRE_URI = questionnaire_uri
    config.VALUESET_URI = valueset_uri
    config.CODESYSTEM_URI = codesystem_uri
    config.LANGUAGE = language
    config.MODE = mode
    id = "diagnosis-vfp-gsd"
    actual = generate_value_set(id, config)

    assert (dict() == actual)


def test_fhir_questionnaire_in_answeroption_mode():
    codesystem_uri = "https://voicecollab.ai/fhir/CodeSystem/"
    valueset_uri = "https://voicecollab.ai/fhir/ValueSet/"
    questionnaire_uri = "https://voicecollab.ai/fhir/Questionnaire/"
    language = "en"
    mode = "AnswerOptions"  # mode change
    config = Config()
    config.QUESTIONNAIRE_URI = questionnaire_uri
    config.VALUESET_URI = valueset_uri
    config.CODESYSTEM_URI = codesystem_uri
    config.LANGUAGE = language
    config.MODE = mode
    reproschema = {'session_schema': {'@context': 'https://raw.githubusercontent.com/ReproNim/reproschema/1.0.0-rc4/contexts/generic', '@type': 'reproschema:Activity', '@id': 'session_schema', 'prefLabel': 'session', 'description': 'Default description', 'schemaVersion': '1.0.0-rc4', 'version': '0.0.1', 'ui': {'order': ['items/session_id', 'items/session_status', 'items/session_started_at', 'items/session_completed_at', 'items/session_duration', 'items/session_site'], 'addProperties': [{'variableName': 'session_id', 'isAbout': 'items/session_id', 'isVis': True}, {'variableName': 'session_status', 'isAbout': 'items/session_status', 'isVis': True}, {'variableName': 'session_started_at', 'isAbout': 'items/session_started_at', 'isVis': True}, {'variableName': 'session_completed_at', 'isAbout': 'items/session_completed_at', 'isVis': True}, {'variableName': 'session_duration', 'isAbout': 'items/session_duration', 'isVis': True}, {'variableName': 'session_site', 'isAbout': 'items/session_site', 'isVis': True}], 'shuffle': False}}, 'items/session_status': {'@context': 'https://raw.githubusercontent.com/ReproNim/reproschema/1.0.0-rc4/contexts/generic', '@type': 'reproschema:Field', '@id': 'session_status', 'prefLabel': 'session_status', 'description': 'session_status of session', 'ui': {'inputType': 'radio'}, 'responseOptions': {'valueType': 'xsd:integer', 'choices': [{'name': 'In Progress ', 'value': 1}, {'name': 'Completed', 'value': 2}]}, 'question': {'en': 'Session Status'}}, 'items/session_id': {'@context': 'https://raw.githubusercontent.com/ReproNim/reproschema/1.0.0-rc4/contexts/generic', '@type': 'reproschema:Field', '@id': 'session_id', 'prefLabel': 'session_id', 'description': 'session_id of session', 'ui': {'inputType': 'text'}, 'responseOptions': {'valueType': 'xsd:string'}, 'question': {
        'en': 'Session ID'}}, 'items/session_duration': {'@context': 'https://raw.githubusercontent.com/ReproNim/reproschema/1.0.0-rc4/contexts/generic', '@type': 'reproschema:Field', '@id': 'session_duration', 'prefLabel': 'session_duration', 'description': 'session_duration of session', 'ui': {'inputType': 'text'}, 'responseOptions': {'valueType': 'xsd:string'}, 'question': {'en': 'Session Duration (seconds)'}}, 'items/session_started_at': {'@context': 'https://raw.githubusercontent.com/ReproNim/reproschema/1.0.0-rc4/contexts/generic', '@type': 'reproschema:Field', '@id': 'session_started_at', 'prefLabel': 'session_started_at', 'description': 'session_started_at of session', 'ui': {'inputType': 'text'}, 'responseOptions': {'valueType': 'xsd:string'}, 'question': {'en': 'Session Started At'}}, 'items/session_completed_at': {'@context': 'https://raw.githubusercontent.com/ReproNim/reproschema/1.0.0-rc4/contexts/generic', '@type': 'reproschema:Field', '@id': 'session_completed_at', 'prefLabel': 'session_completed_at', 'description': 'session_completed_at of session', 'ui': {'inputType': 'text'}, 'responseOptions': {'valueType': 'xsd:string'}, 'question': {'en': 'Session Completed At'}}, 'items/session_site': {'@context': 'https://raw.githubusercontent.com/ReproNim/reproschema/1.0.0-rc4/contexts/generic', '@type': 'reproschema:Field', '@id': 'session_site', 'prefLabel': 'session_site', 'description': 'session_site of session', 'ui': {'inputType': 'radio'}, 'responseOptions': {'valueType': 'xsd:integer', 'choices': [{'name': 'BCH ', 'value': 'bch'}, {'name': 'MIT ', 'value': ' mit'}, {'name': 'Mt. Sinai ', 'value': ' mt_sinai'}, {'name': 'USF ', 'value': ' usf'}, {'name': 'VUMC ', 'value': ' vumc'}, {'name': 'WCM', 'value': ' wcm'}]}, 'question': {'en': 'Session Site?'}}}

    generator = QuestionnaireGenerator(config)
    fhir_questionnaire = generator.convert_to_fhir(OrderedDict(reproschema))
    # hardcode time for testing
    fhir_questionnaire["date"] = "2024-01-30T15:45:41Z"
    expected = {"resourceType": "Questionnaire", "meta": {"profile": ["https://voicecollab.ai/fhir/StructureDefinition/vbai-questionnaire"]}, "id": "sessionschema", "url": "https://voicecollab.ai/fhir/Questionnaire/sessionschema", "title": "session_schema", "version": "1.4.0", "status": "active", "date": "2024-01-30T15:45:41Z", "publisher": "KinD Lab", "contact": [{"name": "KinD Lab", "telecom": [{"system": "url", "value": "http://fhir.kindlab.sickkids.ca"}]}], "item": [{"linkId": "session_id", "type": "string", "text": "Session ID"}, {"linkId": "session_status", "type": "choice", "text": "Session Status", "answerOption": [
        {"valueString": "In Progress "}, {"valueString": "Completed"}]}, {"linkId": "session_started_at", "type": "string", "text": "Session Started At"}, {"linkId": "session_completed_at", "type": "string", "text": "Session Completed At"}, {"linkId": "session_duration", "type": "string", "text": "Session Duration (seconds)"}, {"linkId": "session_site", "type": "choice", "text": "Session Site?", "answerOption": [{"valueString": "BCH "}, {"valueString": "MIT "}, {"valueString": "Mt. Sinai "}, {"valueString": "USF "}, {"valueString": "VUMC "}, {"valueString": "WCM"}]}]}
    assert expected == fhir_questionnaire


def test_fhir_questionnaire_in_valueset_mode():
    codesystem_uri = "https://voicecollab.ai/fhir/CodeSystem/"
    valueset_uri = "https://voicecollab.ai/fhir/ValueSet/"
    questionnaire_uri = "https://voicecollab.ai/fhir/Questionnaire/"
    language = "en"
    mode = "ValueSet"  # mode change
    config = Config()
    config.QUESTIONNAIRE_URI = questionnaire_uri
    config.VALUESET_URI = valueset_uri
    config.CODESYSTEM_URI = codesystem_uri
    config.LANGUAGE = language
    config.MODE = mode
    reproschema = {'session_schema': {'@context': 'https://raw.githubusercontent.com/ReproNim/reproschema/1.0.0-rc4/contexts/generic', '@type': 'reproschema:Activity', '@id': 'session_schema', 'prefLabel': 'session', 'description': 'Default description', 'schemaVersion': '1.0.0-rc4', 'version': '0.0.1', 'ui': {'order': ['items/session_id', 'items/session_status', 'items/session_started_at', 'items/session_completed_at', 'items/session_duration', 'items/session_site'], 'addProperties': [{'variableName': 'session_id', 'isAbout': 'items/session_id', 'isVis': True}, {'variableName': 'session_status', 'isAbout': 'items/session_status', 'isVis': True}, {'variableName': 'session_started_at', 'isAbout': 'items/session_started_at', 'isVis': True}, {'variableName': 'session_completed_at', 'isAbout': 'items/session_completed_at', 'isVis': True}, {'variableName': 'session_duration', 'isAbout': 'items/session_duration', 'isVis': True}, {'variableName': 'session_site', 'isAbout': 'items/session_site', 'isVis': True}], 'shuffle': False}}, 'items/session_status': {'@context': 'https://raw.githubusercontent.com/ReproNim/reproschema/1.0.0-rc4/contexts/generic', '@type': 'reproschema:Field', '@id': 'session_status', 'prefLabel': 'session_status', 'description': 'session_status of session', 'ui': {'inputType': 'radio'}, 'responseOptions': {'valueType': 'xsd:integer', 'choices': [{'name': 'In Progress ', 'value': 1}, {'name': 'Completed', 'value': 2}]}, 'question': {'en': 'Session Status'}}, 'items/session_id': {'@context': 'https://raw.githubusercontent.com/ReproNim/reproschema/1.0.0-rc4/contexts/generic', '@type': 'reproschema:Field', '@id': 'session_id', 'prefLabel': 'session_id', 'description': 'session_id of session', 'ui': {'inputType': 'text'}, 'responseOptions': {'valueType': 'xsd:string'}, 'question': {
        'en': 'Session ID'}}, 'items/session_duration': {'@context': 'https://raw.githubusercontent.com/ReproNim/reproschema/1.0.0-rc4/contexts/generic', '@type': 'reproschema:Field', '@id': 'session_duration', 'prefLabel': 'session_duration', 'description': 'session_duration of session', 'ui': {'inputType': 'text'}, 'responseOptions': {'valueType': 'xsd:string'}, 'question': {'en': 'Session Duration (seconds)'}}, 'items/session_started_at': {'@context': 'https://raw.githubusercontent.com/ReproNim/reproschema/1.0.0-rc4/contexts/generic', '@type': 'reproschema:Field', '@id': 'session_started_at', 'prefLabel': 'session_started_at', 'description': 'session_started_at of session', 'ui': {'inputType': 'text'}, 'responseOptions': {'valueType': 'xsd:string'}, 'question': {'en': 'Session Started At'}}, 'items/session_completed_at': {'@context': 'https://raw.githubusercontent.com/ReproNim/reproschema/1.0.0-rc4/contexts/generic', '@type': 'reproschema:Field', '@id': 'session_completed_at', 'prefLabel': 'session_completed_at', 'description': 'session_completed_at of session', 'ui': {'inputType': 'text'}, 'responseOptions': {'valueType': 'xsd:string'}, 'question': {'en': 'Session Completed At'}}, 'items/session_site': {'@context': 'https://raw.githubusercontent.com/ReproNim/reproschema/1.0.0-rc4/contexts/generic', '@type': 'reproschema:Field', '@id': 'session_site', 'prefLabel': 'session_site', 'description': 'session_site of session', 'ui': {'inputType': 'radio'}, 'responseOptions': {'valueType': 'xsd:integer', 'choices': [{'name': 'BCH ', 'value': 'bch'}, {'name': 'MIT ', 'value': ' mit'}, {'name': 'Mt. Sinai ', 'value': ' mt_sinai'}, {'name': 'USF ', 'value': ' usf'}, {'name': 'VUMC ', 'value': ' vumc'}, {'name': 'WCM', 'value': ' wcm'}]}, 'question': {'en': 'Session Site?'}}}

    generator = QuestionnaireGenerator(config)
    fhir_questionnaire = generator.convert_to_fhir(OrderedDict(reproschema))
    # hardcode time for testing
    fhir_questionnaire["date"] = "2024-01-30T15:45:41Z"
    expected = {"resourceType": "Questionnaire", "meta": {"profile": ["https://voicecollab.ai/fhir/StructureDefinition/vbai-questionnaire"]}, "id": "sessionschema", "url": "https://voicecollab.ai/fhir/Questionnaire/sessionschema", "title": "session_schema", "version": "1.4.0", "status": "active", "date": "2024-01-30T15:45:41Z", "publisher": "KinD Lab", "contact": [{"name": "KinD Lab", "telecom": [{"system": "url", "value": "http://fhir.kindlab.sickkids.ca"}]}], "item": [{"linkId": "session_id", "type": "string", "text": "Session ID"}, {
        "linkId": "session_status", "type": "choice", "text": "Session Status", "answerValueSet": "https://voicecollab.ai/fhir/ValueSet/session-status"}, {"linkId": "session_started_at", "type": "string", "text": "Session Started At"}, {"linkId": "session_completed_at", "type": "string", "text": "Session Completed At"}, {"linkId": "session_duration", "type": "string", "text": "Session Duration (seconds)"}, {"linkId": "session_site", "type": "choice", "text": "Session Site?", "answerValueSet": "https://voicecollab.ai/fhir/ValueSet/session-site"}]}
    assert expected == fhir_questionnaire


def test_parse_reproschema_items_in_valueset_mode():
    codesystem_uri = "https://voicecollab.ai/fhir/CodeSystem/"
    valueset_uri = "https://voicecollab.ai/fhir/ValueSet/"
    questionnaire_uri = "https://voicecollab.ai/fhir/Questionnaire/"
    language = "en"
    mode = "ValueSet"  # mode change
    config = Config()
    config.QUESTIONNAIRE_URI = questionnaire_uri
    config.VALUESET_URI = valueset_uri
    config.CODESYSTEM_URI = codesystem_uri
    config.LANGUAGE = language
    config.MODE = mode

    reproschema = {'session_schema': {'@context': 'https://raw.githubusercontent.com/ReproNim/reproschema/1.0.0-rc4/contexts/generic', '@type': 'reproschema:Activity', '@id': 'session_schema', 'prefLabel': 'session', 'description': 'Default description', 'schemaVersion': '1.0.0-rc4', 'version': '0.0.1', 'ui': {'order': ['items/session_id', 'items/session_status', 'items/session_started_at', 'items/session_completed_at', 'items/session_duration', 'items/session_site'], 'addProperties': [{'variableName': 'session_id', 'isAbout': 'items/session_id', 'isVis': True}, {'variableName': 'session_status', 'isAbout': 'items/session_status', 'isVis': True}, {'variableName': 'session_started_at', 'isAbout': 'items/session_started_at', 'isVis': True}, {'variableName': 'session_completed_at', 'isAbout': 'items/session_completed_at', 'isVis': True}, {'variableName': 'session_duration', 'isAbout': 'items/session_duration', 'isVis': True}, {'variableName': 'session_site', 'isAbout': 'items/session_site', 'isVis': True}], 'shuffle': False}}, 'items/session_status': {'@context': 'https://raw.githubusercontent.com/ReproNim/reproschema/1.0.0-rc4/contexts/generic', '@type': 'reproschema:Field', '@id': 'session_status', 'prefLabel': 'session_status', 'description': 'session_status of session', 'ui': {'inputType': 'radio'}, 'responseOptions': {'valueType': 'xsd:integer', 'choices': [{'name': 'In Progress ', 'value': 1}, {'name': 'Completed', 'value': 2}]}, 'question': {'en': 'Session Status'}}, 'items/session_id': {'@context': 'https://raw.githubusercontent.com/ReproNim/reproschema/1.0.0-rc4/contexts/generic', '@type': 'reproschema:Field', '@id': 'session_id', 'prefLabel': 'session_id', 'description': 'session_id of session', 'ui': {'inputType': 'text'}, 'responseOptions': {'valueType': 'xsd:string'}, 'question': {
        'en': 'Session ID'}}, 'items/session_duration': {'@context': 'https://raw.githubusercontent.com/ReproNim/reproschema/1.0.0-rc4/contexts/generic', '@type': 'reproschema:Field', '@id': 'session_duration', 'prefLabel': 'session_duration', 'description': 'session_duration of session', 'ui': {'inputType': 'text'}, 'responseOptions': {'valueType': 'xsd:string'}, 'question': {'en': 'Session Duration (seconds)'}}, 'items/session_started_at': {'@context': 'https://raw.githubusercontent.com/ReproNim/reproschema/1.0.0-rc4/contexts/generic', '@type': 'reproschema:Field', '@id': 'session_started_at', 'prefLabel': 'session_started_at', 'description': 'session_started_at of session', 'ui': {'inputType': 'text'}, 'responseOptions': {'valueType': 'xsd:string'}, 'question': {'en': 'Session Started At'}}, 'items/session_completed_at': {'@context': 'https://raw.githubusercontent.com/ReproNim/reproschema/1.0.0-rc4/contexts/generic', '@type': 'reproschema:Field', '@id': 'session_completed_at', 'prefLabel': 'session_completed_at', 'description': 'session_completed_at of session', 'ui': {'inputType': 'text'}, 'responseOptions': {'valueType': 'xsd:string'}, 'question': {'en': 'Session Completed At'}}, 'items/session_site': {'@context': 'https://raw.githubusercontent.com/ReproNim/reproschema/1.0.0-rc4/contexts/generic', '@type': 'reproschema:Field', '@id': 'session_site', 'prefLabel': 'session_site', 'description': 'session_site of session', 'ui': {'inputType': 'radio'}, 'responseOptions': {'valueType': 'xsd:integer', 'choices': [{'name': 'BCH ', 'value': 'bch'}, {'name': 'MIT ', 'value': ' mit'}, {'name': 'Mt. Sinai ', 'value': ' mt_sinai'}, {'name': 'USF ', 'value': ' usf'}, {'name': 'VUMC ', 'value': ' vumc'}, {'name': 'WCM', 'value': ' wcm'}]}, 'question': {'en': 'Session Site?'}}}
    reproschema_items = {'items/session_id': {'@context': 'https://raw.githubusercontent.com/ReproNim/reproschema/1.0.0-rc4/contexts/generic', '@type': 'reproschema:Field', '@id': 'session_id', 'prefLabel': 'session_id', 'description': 'session_id of session', 'ui': {'inputType': 'text'}, 'responseOptions': {'valueType': 'xsd:string'}, 'question': {'en': 'Session ID'}}, 'items/session_status': {'@context': 'https://raw.githubusercontent.com/ReproNim/reproschema/1.0.0-rc4/contexts/generic', '@type': 'reproschema:Field', '@id': 'session_status', 'prefLabel': 'session_status', 'description': 'session_status of session', 'ui': {'inputType': 'radio'}, 'responseOptions': {'valueType': 'xsd:integer', 'choices': [{'name': 'In Progress ', 'value': 1}, {'name': 'Completed', 'value': 2}]}, 'question': {'en': 'Session Status'}}, 'items/session_started_at': {'@context': 'https://raw.githubusercontent.com/ReproNim/reproschema/1.0.0-rc4/contexts/generic', '@type': 'reproschema:Field', '@id': 'session_started_at', 'prefLabel': 'session_started_at', 'description': 'session_started_at of session', 'ui': {'inputType': 'text'}, 'responseOptions': {'valueType': 'xsd:string'}, 'question': {'en': 'Session Started At'}}, 'items/session_completed_at': {
        '@context': 'https://raw.githubusercontent.com/ReproNim/reproschema/1.0.0-rc4/contexts/generic', '@type': 'reproschema:Field', '@id': 'session_completed_at', 'prefLabel': 'session_completed_at', 'description': 'session_completed_at of session', 'ui': {'inputType': 'text'}, 'responseOptions': {'valueType': 'xsd:string'}, 'question': {'en': 'Session Completed At'}}, 'items/session_duration': {'@context': 'https://raw.githubusercontent.com/ReproNim/reproschema/1.0.0-rc4/contexts/generic', '@type': 'reproschema:Field', '@id': 'session_duration', 'prefLabel': 'session_duration', 'description': 'session_duration of session', 'ui': {'inputType': 'text'}, 'responseOptions': {'valueType': 'xsd:string'}, 'question': {'en': 'Session Duration (seconds)'}}, 'items/session_site': {'@context': 'https://raw.githubusercontent.com/ReproNim/reproschema/1.0.0-rc4/contexts/generic', '@type': 'reproschema:Field', '@id': 'session_site', 'prefLabel': 'session_site', 'description': 'session_site of session', 'ui': {'inputType': 'radio'}, 'responseOptions': {'valueType': 'xsd:integer', 'choices': [{'name': 'BCH ', 'value': 'bch'}, {'name': 'MIT ', 'value': ' mit'}, {'name': 'Mt. Sinai ', 'value': ' mt_sinai'}, {'name': 'USF ', 'value': ' usf'}, {'name': 'VUMC ', 'value': ' vumc'}, {'name': 'WCM', 'value': ' wcm'}]}, 'question': {'en': 'Session Site?'}}}
    generator = QuestionnaireGenerator(config)

    fhir_items = generator.parse_reproschema_items(
        OrderedDict(reproschema_items), OrderedDict(reproschema))
    expected = [{'linkId': 'session_id', 'type': 'string', 'text': 'Session ID'}, {'linkId': 'session_status', 'type': 'choice', 'text': 'Session Status', 'answerValueSet': 'https://voicecollab.ai/fhir/ValueSet/session-status'}, {'linkId': 'session_started_at', 'type': 'string', 'text': 'Session Started At'},
                {'linkId': 'session_completed_at', 'type': 'string', 'text': 'Session Completed At'}, {'linkId': 'session_duration', 'type': 'string', 'text': 'Session Duration (seconds)'}, {'linkId': 'session_site', 'type': 'choice', 'text': 'Session Site?', 'answerValueSet': 'https://voicecollab.ai/fhir/ValueSet/session-site'}]
    assert expected == fhir_items


def test_parse_reproschema_items_in_answeroption_mode():
    codesystem_uri = "https://voicecollab.ai/fhir/CodeSystem/"
    valueset_uri = "https://voicecollab.ai/fhir/ValueSet/"
    questionnaire_uri = "https://voicecollab.ai/fhir/Questionnaire/"
    language = "en"
    mode = "AnswerOptions"  # mode change
    config = Config()
    config.QUESTIONNAIRE_URI = questionnaire_uri
    config.VALUESET_URI = valueset_uri
    config.CODESYSTEM_URI = codesystem_uri
    config.LANGUAGE = language
    config.MODE = mode

    reproschema = {'session_schema': {'@context': 'https://raw.githubusercontent.com/ReproNim/reproschema/1.0.0-rc4/contexts/generic', '@type': 'reproschema:Activity', '@id': 'session_schema', 'prefLabel': 'session', 'description': 'Default description', 'schemaVersion': '1.0.0-rc4', 'version': '0.0.1', 'ui': {'order': ['items/session_id', 'items/session_status', 'items/session_started_at', 'items/session_completed_at', 'items/session_duration', 'items/session_site'], 'addProperties': [{'variableName': 'session_id', 'isAbout': 'items/session_id', 'isVis': True}, {'variableName': 'session_status', 'isAbout': 'items/session_status', 'isVis': True}, {'variableName': 'session_started_at', 'isAbout': 'items/session_started_at', 'isVis': True}, {'variableName': 'session_completed_at', 'isAbout': 'items/session_completed_at', 'isVis': True}, {'variableName': 'session_duration', 'isAbout': 'items/session_duration', 'isVis': True}, {'variableName': 'session_site', 'isAbout': 'items/session_site', 'isVis': True}], 'shuffle': False}}, 'items/session_status': {'@context': 'https://raw.githubusercontent.com/ReproNim/reproschema/1.0.0-rc4/contexts/generic', '@type': 'reproschema:Field', '@id': 'session_status', 'prefLabel': 'session_status', 'description': 'session_status of session', 'ui': {'inputType': 'radio'}, 'responseOptions': {'valueType': 'xsd:integer', 'choices': [{'name': 'In Progress ', 'value': 1}, {'name': 'Completed', 'value': 2}]}, 'question': {'en': 'Session Status'}}, 'items/session_id': {'@context': 'https://raw.githubusercontent.com/ReproNim/reproschema/1.0.0-rc4/contexts/generic', '@type': 'reproschema:Field', '@id': 'session_id', 'prefLabel': 'session_id', 'description': 'session_id of session', 'ui': {'inputType': 'text'}, 'responseOptions': {'valueType': 'xsd:string'}, 'question': {
        'en': 'Session ID'}}, 'items/session_duration': {'@context': 'https://raw.githubusercontent.com/ReproNim/reproschema/1.0.0-rc4/contexts/generic', '@type': 'reproschema:Field', '@id': 'session_duration', 'prefLabel': 'session_duration', 'description': 'session_duration of session', 'ui': {'inputType': 'text'}, 'responseOptions': {'valueType': 'xsd:string'}, 'question': {'en': 'Session Duration (seconds)'}}, 'items/session_started_at': {'@context': 'https://raw.githubusercontent.com/ReproNim/reproschema/1.0.0-rc4/contexts/generic', '@type': 'reproschema:Field', '@id': 'session_started_at', 'prefLabel': 'session_started_at', 'description': 'session_started_at of session', 'ui': {'inputType': 'text'}, 'responseOptions': {'valueType': 'xsd:string'}, 'question': {'en': 'Session Started At'}}, 'items/session_completed_at': {'@context': 'https://raw.githubusercontent.com/ReproNim/reproschema/1.0.0-rc4/contexts/generic', '@type': 'reproschema:Field', '@id': 'session_completed_at', 'prefLabel': 'session_completed_at', 'description': 'session_completed_at of session', 'ui': {'inputType': 'text'}, 'responseOptions': {'valueType': 'xsd:string'}, 'question': {'en': 'Session Completed At'}}, 'items/session_site': {'@context': 'https://raw.githubusercontent.com/ReproNim/reproschema/1.0.0-rc4/contexts/generic', '@type': 'reproschema:Field', '@id': 'session_site', 'prefLabel': 'session_site', 'description': 'session_site of session', 'ui': {'inputType': 'radio'}, 'responseOptions': {'valueType': 'xsd:integer', 'choices': [{'name': 'BCH ', 'value': 'bch'}, {'name': 'MIT ', 'value': ' mit'}, {'name': 'Mt. Sinai ', 'value': ' mt_sinai'}, {'name': 'USF ', 'value': ' usf'}, {'name': 'VUMC ', 'value': ' vumc'}, {'name': 'WCM', 'value': ' wcm'}]}, 'question': {'en': 'Session Site?'}}}
    reproschema_items = {'items/session_id': {'@context': 'https://raw.githubusercontent.com/ReproNim/reproschema/1.0.0-rc4/contexts/generic', '@type': 'reproschema:Field', '@id': 'session_id', 'prefLabel': 'session_id', 'description': 'session_id of session', 'ui': {'inputType': 'text'}, 'responseOptions': {'valueType': 'xsd:string'}, 'question': {'en': 'Session ID'}}, 'items/session_status': {'@context': 'https://raw.githubusercontent.com/ReproNim/reproschema/1.0.0-rc4/contexts/generic', '@type': 'reproschema:Field', '@id': 'session_status', 'prefLabel': 'session_status', 'description': 'session_status of session', 'ui': {'inputType': 'radio'}, 'responseOptions': {'valueType': 'xsd:integer', 'choices': [{'name': 'In Progress ', 'value': 1}, {'name': 'Completed', 'value': 2}]}, 'question': {'en': 'Session Status'}}, 'items/session_started_at': {'@context': 'https://raw.githubusercontent.com/ReproNim/reproschema/1.0.0-rc4/contexts/generic', '@type': 'reproschema:Field', '@id': 'session_started_at', 'prefLabel': 'session_started_at', 'description': 'session_started_at of session', 'ui': {'inputType': 'text'}, 'responseOptions': {'valueType': 'xsd:string'}, 'question': {'en': 'Session Started At'}}, 'items/session_completed_at': {
        '@context': 'https://raw.githubusercontent.com/ReproNim/reproschema/1.0.0-rc4/contexts/generic', '@type': 'reproschema:Field', '@id': 'session_completed_at', 'prefLabel': 'session_completed_at', 'description': 'session_completed_at of session', 'ui': {'inputType': 'text'}, 'responseOptions': {'valueType': 'xsd:string'}, 'question': {'en': 'Session Completed At'}}, 'items/session_duration': {'@context': 'https://raw.githubusercontent.com/ReproNim/reproschema/1.0.0-rc4/contexts/generic', '@type': 'reproschema:Field', '@id': 'session_duration', 'prefLabel': 'session_duration', 'description': 'session_duration of session', 'ui': {'inputType': 'text'}, 'responseOptions': {'valueType': 'xsd:string'}, 'question': {'en': 'Session Duration (seconds)'}}, 'items/session_site': {'@context': 'https://raw.githubusercontent.com/ReproNim/reproschema/1.0.0-rc4/contexts/generic', '@type': 'reproschema:Field', '@id': 'session_site', 'prefLabel': 'session_site', 'description': 'session_site of session', 'ui': {'inputType': 'radio'}, 'responseOptions': {'valueType': 'xsd:integer', 'choices': [{'name': 'BCH ', 'value': 'bch'}, {'name': 'MIT ', 'value': ' mit'}, {'name': 'Mt. Sinai ', 'value': ' mt_sinai'}, {'name': 'USF ', 'value': ' usf'}, {'name': 'VUMC ', 'value': ' vumc'}, {'name': 'WCM', 'value': ' wcm'}]}, 'question': {'en': 'Session Site?'}}}
    generator = QuestionnaireGenerator(config)

    fhir_items = generator.parse_reproschema_items(
        OrderedDict(reproschema_items), OrderedDict(reproschema))
    expected = [{'linkId': 'session_id', 'type': 'string', 'text': 'Session ID'}, {'linkId': 'session_status', 'type': 'choice', 'text': 'Session Status', 'answerOption': [{'valueString': 'In Progress '}, {'valueString': 'Completed'}]}, {'linkId': 'session_started_at', 'type': 'string', 'text': 'Session Started At'}, {'linkId': 'session_completed_at', 'type': 'string',
                                                                                                                                                                                                                                                                                                                                'text': 'Session Completed At'}, {'linkId': 'session_duration', 'type': 'string', 'text': 'Session Duration (seconds)'}, {'linkId': 'session_site', 'type': 'choice', 'text': 'Session Site?', 'answerOption': [{'valueString': 'BCH '}, {'valueString': 'MIT '}, {'valueString': 'Mt. Sinai '}, {'valueString': 'USF '}, {'valueString': 'VUMC '}, {'valueString': 'WCM'}]}]
    assert expected == fhir_items




def test_add_enable_no_ors_and_no_ands():
    condition = "item_val == 2"
    actual = add_enable_when(condition)
    expected = ([
        {"question": "item_val",
         "operator": "=",
         "answerString": "2"
         }], "None")

    assert expected == actual




def test_add_enable_when_using_ors():
    condition = "item_1 > 1 || item_2 == 2"
    actual = add_enable_when(condition)
    expected = ([
        {"question": "item_1",
         "operator": ">",
         "answerString": "1"
         },
        {"question": "item_2",
         "operator": "=",
         "answerString": "2"
         }], "any")
    assert expected == actual


def test_add_enable_when_using_ands():
    condition = "item_1 == 1 && item_2 <= 2"
    actual = add_enable_when(condition)
    expected = ([
        {"question": "item_1",
         "operator": "=",
         "answerString": "1"
         },
        {"question": "item_2",
         "operator": "<=",
         "answerString": "2"
         }], "all")

    assert expected == actual

def test_add_enable_when_edgecase_with_triple_underscore():
    condition = "item_val___6 == 1 && item_2 <= 2"
    actual = add_enable_when(condition)
    expected = ([
        {"question": "item_val",
         "operator": "=",
         "answerString": "6"
         },
        {"question": "item_2",
         "operator": "<=",
         "answerString": "2"
         }], "all")

    assert expected == actual

def test_add_enable_when_edgecase_with_parentheses():
    condition = "item_1(placeholder) == 6 && item_2 <= 2"
    actual = add_enable_when(condition)
    expected = ([
        {"question": "item_1",
         "operator": "=",
         "answerString": "6"
         },
        {"question": "item_2",
         "operator": "<=",
         "answerString": "2"
         }], "all")

    assert expected == actual