'''
script to convert repro scheme to json for fhir questionnaire
Currently supports reproschema to fhir json in en.
#example: "python reprotofhirjson.py <reproschema_folder> valueset"
'''

import argparse
from collections import OrderedDict
import json
import os
from pathlib import Path

from fhir.resources.questionnaire import Questionnaire
from fhir.resources.valueset import ValueSet
from fhir.resources.codesystem import CodeSystem
from fhir.resources import construct_fhir_element

from reproschema.jsonldutils import load_file

from src.reproschema_to_fhir.config import Config
from src.reproschema_to_fhir.fhir import QuestionnaireGenerator

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("reproschema_questionnaire")
    #reproschema_folder = Path.cwd() / "b2ai-redcap2rs/activities/questionnaire_across_all_cohorts_gad7_anxiety"
    args = parser.parse_args()
    reproschema_folder = Path(str(args.reproschema_questionnaire))

    # load each file recursively within the folder into its own key in the reproschema_content dict
    reproschema_content = OrderedDict()
    for file in reproschema_folder.glob("**/*"):
        if file.is_file():
            # get the full path to the file *after* the base reproschema_folder path
            # since files can be referenced by relative paths, we need to keep track of relative location
            filename = str(file.relative_to(reproschema_folder))
            with open(f"{reproschema_folder}/{filename}") as f:
                reproschema_content[filename] = json.loads(str(f.read()))

    schema_name = [
        name for name in list(reproschema_content.keys())
        if name.endswith("_schema")
    ][0]
    reproschema_schema = reproschema_content[schema_name]

    if (f"schema:version" in reproschema_schema and
            reproschema_schema["schema:version"] not in ("0.0.1", "1.0.0-rc1")
        ) or f"version" in reproschema_schema and reproschema_schema[
            "version"] not in ("0.0.1", "1.0.0-rc1"):
        raise ValueError(
            'Unable to work with reproschema versions other than 0.0.1 or 1.0.0-rc1'
        )
    # before we print to file we wish to validate the jsons using fhir resources

    # convert to fhir
    config = Config()

    questionnaire_generator = QuestionnaireGenerator(config)
    fhir_questionnaire = questionnaire_generator.convert_to_fhir(
        reproschema_content)

    try:
        questionnaire_json = construct_fhir_element('Questionnaire',
                                                    fhir_questionnaire)
    except:
        raise ValueError(f"The Questionnaire json is not properly structured")

    try:
        valueset_dict = questionnaire_generator.get_value_set()

        for valueset in valueset_dict:
            valueset_json = construct_fhir_element('ValueSet',
                                                   valueset_dict[valueset])
    except:
        raise ValueError(
            f"One of the valueset json's are not properly structured")

    try:
        codesystem_dict = questionnaire_generator.get_code_system()

        for codesystem in codesystem_dict:
            codesystem_json = construct_fhir_element(
                'CodeSystem', codesystem_dict[codesystem])
    except:
        raise ValueError(
            f"One of the codesystem json's are not properly structured")

    # get filename from the reproschema_folder name provided
    file_name = reproschema_folder.parts[-1]
    with open(f"{file_name}.json", "w+") as f:
        f.write(json.dumps(fhir_questionnaire))

    # write out valuesets and codesystems which have been updated in the generator object
    with open(f"{file_name}-valuesets.json", "w+") as f:
        f.write(json.dumps(questionnaire_generator.get_value_set()))

    with open(f"{file_name}-codesystems.json", "w+") as f:
        f.write(json.dumps(questionnaire_generator.get_code_system()))
