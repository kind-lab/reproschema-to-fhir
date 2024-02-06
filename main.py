'''
script to convert repro scheme to json for fhir questionnaire
Currently supports reproschema to fhir json in en.
#example: "python reprotofhirjson.py <reproschema_folder directory>"
'''

import argparse
from collections import OrderedDict
import json
import os
import shutil
from pathlib import Path

from fhir.resources.questionnaire import Questionnaire
from fhir.resources.valueset import ValueSet
from fhir.resources.codesystem import CodeSystem
from fhir.resources import construct_fhir_element

from reproschema.jsonldutils import load_file

from reproschema_to_fhir.config import Config
from reproschema_to_fhir.fhir import QuestionnaireGenerator

def main():
    parser = argparse.ArgumentParser()
    # string param of path to folder containing reproschema files
    parser.add_argument("reproschema_questionnaire",
                        type=str,
                        help="path to folder containing reproschema files")
    args = parser.parse_args()
    reproschema_folder = Path(args.reproschema_questionnaire)
    if not os.path.isdir(reproschema_folder):
        raise FileNotFoundError(
            f"{reproschema_folder} does not exist. Please check if folder exists and is located at the correct directory"
        )

    # load each file recursively within the folder into its own key in the reproschema_content dict
    reproschema_content = OrderedDict()
    for file in reproschema_folder.glob("**/*"):
        if file.is_file():
            # get the full path to the file *after* the base reproschema_folder path
            # since files can be referenced by relative paths, we need to keep track of relative location
            filename = str(file.relative_to(reproschema_folder))
            with open(f"{reproschema_folder}/{filename}") as f:
                reproschema_content[filename] = json.loads(f.read())

    schema_name = [
        name for name in (reproschema_content.keys())
        if name.endswith("_schema")
    ][0]
    reproschema_schema = reproschema_content[schema_name]

    if (f"schema:version" in reproschema_schema and
            reproschema_schema["schema:version"] not in ("0.0.1", "1.0.0-rc1")
        ) or f"version" in reproschema_schema and reproschema_schema[
            "version"] not in ("0.0.1", "1.0.0-rc1", "1.0.0-rc4"):
        raise ValueError(
            'Unable to work with reproschema versions other than 0.0.1, 1.0.0-rc1, and 1.0.0-rc4'
        )
    # before we print to file we wish to validate the jsons using fhir resources

    # convert to fhir
    config = Config()

    questionnaire_generator = QuestionnaireGenerator(config)
    fhir_questionnaire = questionnaire_generator.convert_to_fhir(
        reproschema_content)

    questionnaire_json = construct_fhir_element('Questionnaire',
                                                fhir_questionnaire)

    valueset_dict = questionnaire_generator.get_value_set()

    for valueset in valueset_dict:
        valueset_json = construct_fhir_element('ValueSet',
                                               valueset_dict[valueset])

    codesystem_dict = questionnaire_generator.get_code_system()

    for codesystem in codesystem_dict:
        codesystem_json = construct_fhir_element('CodeSystem',
                                                 codesystem_dict[codesystem])

    # get filename from the reproschema_folder name provided

    file_name = reproschema_folder.parts[-1]

    dirpath = Path(f"./output/{file_name}")
    if dirpath.exists() and dirpath.is_dir():
        shutil.rmtree(dirpath)

    paths = [f"./output/{file_name}/", f"./output/{file_name}/valuesets/", f"./output/{file_name}/codesystems/"]
    
    for folder in paths:
        os.makedirs(folder)

    with open(f"./output/{file_name}/{file_name}.json", "w+") as f:
        f.write(json.dumps(fhir_questionnaire))

    # write out valuesets and codesystems which have been updated in the generator object
 
    valueset_count = 1
    valuesets = [value for (key,value) in questionnaire_generator.get_value_set().items()]
    for valueset in valuesets:
        with open(f"./output/{file_name}/valuesets/{file_name}-valueset-{valueset_count}.json", "w+") as f:
            f.write(json.dumps(valueset))
        valueset_count += 1

    codesystem_count = 1
    codesystems = [value for (key,value) in questionnaire_generator.get_code_system().items()]
    for codesystem in codesystems:
        with open(f"./output/{file_name}/codesystems/{file_name}-codesystem-{codesystem_count}.json", "w+") as f:
            f.write(json.dumps(codesystem))
        codesystem_count += 1

if __name__ == '__main__':
    main()
