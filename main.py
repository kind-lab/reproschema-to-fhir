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


from reproschema.jsonldutils import load_file

from src.reproschema_to_fhir.config import Config
from src.reproschema_to_fhir.fhir import QuestionnaireGenerator


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    # TODO: change from hard-coded to command line argument
    reproschema_folder = Path.cwd() / "b2ai-redcap2rs/activities/questionnaire_across_all_cohorts_gad7_anxiety"
    args = parser.parse_args()

    # load each file recursively within the folder into its own key in the reproschema_content dict
    reproschema_content = OrderedDict()
    for file in reproschema_folder.glob("**/*"):
        if file.is_file():
            # get the full path to the file *after* the base reproschema_folder path
            # since files can be referenced by relative paths, we need to keep track of relative location
            filename = str(file.relative_to(reproschema_folder))
            with open(f"{reproschema_folder}/{filename}") as f:
                #print(str(f))
                reproschema_content[filename] = json.loads(str(f.read()))
    #print(reproschema_content)

    # TODO: validate reproschema
    # if reproschema_content["schema"] != "0.0.1":
    #     raise ValueError('Unable to work with reproschema versions other than 0.0.1')

    # convert to fhir
    config = Config()
    print(config.get_questionnaire())
    questionnaire_generator = QuestionnaireGenerator(config)
    fhir_questionnaire = questionnaire_generator.convert_to_fhir(reproschema_content)


    # get filename from the reproschema_folder name provided
    file_name = reproschema_folder.parts[-1]
    with open(f"{file_name}.json", "w+") as f:
        f.write(json.dumps(fhir_questionnaire))

    # write out valuesets and codesystems which have been updated in the generator object
    with open(f"{file_name}-valuesets.json", "w+") as f:
        f.write(json.dumps(questionnaire_generator.value_set))

    with open(f"{file_name}-codesystems.json", "w+") as f:
        f.write(json.dumps(questionnaire_generator.code_system))
