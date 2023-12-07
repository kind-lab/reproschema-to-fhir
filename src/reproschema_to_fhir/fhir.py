from abc import ABC, abstractmethod
import os
import json
from collections import OrderedDict
from typing import Optional
from pathlib import Path

from fhir.resources.questionnaire import Questionnaire
from fhir.resources.valueset import ValueSet
from fhir.resources.codesystem import CodeSystem

from .config import Config

# TODO: migrate these globals to the config
CODESYSTEM_URI = os.getenv('CODESYSTEM_URI')
VALUESET_URI = os.getenv('VALUESET_URI')
QUESTIONNAIRE_URI = os.getenv('QUESTIONNAIRE_URI')

def generate_code_system(
    options_json, id_str: str
) -> dict:
    """
    Helper function to generate a FHIR CodeSystem resource from a reproschema options json.
    """
    # default headers for codesystem
    codeSystem = dict()
    # id = questionnaire + linkId
    # id = id.replace("_", "-")
    # id = id.lower()

    codeSystem[f"resourceType"] = f"CodeSystem"
    codeSystem[f"id"] = id_str
    codeSystem[f"text"] = {
        f"status": f"generated",
        f"div": f'<div xmlns="http://www.w3.org/1999/xhtml">Placeholder</div>',
    }

    codeSystem[f"url"] = f"{CODESYSTEM_URI}{id_str}"
    codeSystem[f"version"] = f"1.4.0"
    codeSystem[f"name"] = id_str.capitalize().replace("_", "")
    codeSystem[f"title"] = id_str
    codeSystem[f"status"] = f"active"
    codeSystem[f"date"] = f"2023-11-20T11:33:15-05:00"
    codeSystem[f"publisher"] = f"KinD Lab"
    codeSystem[f"contact"] = [
        {
            f"name": f"KinD Lab",
            f"telecom": [
                {f"system": f"url", f"value": f"http://fhir.kindlab.sickkids.ca"}
            ],
        }
    ]

    codeSystem[f"description"] = id_str
    codeSystem[f"caseSensitive"] = True
    codeSystem[f"content"] = f"complete"
    codeSystem[f"count"] = len(options_json[f"choices"])
    codeSystem[f"concept"] = []

    options = []
    # we wish to retrieve each option stored in the reproschema json list. We do this by parsing the list
    # of jsons and append then contents to an outlined codesystem
    for j in options_json[f"choices"]:
        codeSystem_option = dict()
        if f"schema:name" in j and j[f"schema:name"] != "":
            choice = j[f"schema:name"]
        else:
            choice = j[f"schema:value"]

        if (
            choice
            and not isinstance(choice, int)
            and f"en" in choice
            and isinstance(choice, dict)
        ):
            choice = choice["en"]

        choice = str(choice)
        codeSystem_option[f"code"] = j[f"schema:value"]
        codeSystem_option[f"display"] = str(choice)

        options.append(choice.replace(" ", ""))
        codeSystem[f"concept"].append(codeSystem_option)

    return codeSystem


def generate_value_set(id_str: str) -> dict:
    valueset = dict()
    valueset[f"resourceType"] = f"ValueSet"
    valueset[f"id"] = id_str
    valueset[f"text"] = {
        f"status": f"generated",
        f"div": f'<div xmlns="http://www.w3.org/1999/xhtml">Placeholder</div>',
    }
    valueset[f"url"] = f"{VALUESET_URI}{id_str}"
    valueset[f"version"] = f"1.4.0"

    valueset[f"name"] = id_str.capitalize().replace("_", "")
    valueset[f"title"] = id_str
    valueset[f"status"] = f"active"
    valueset[f"date"] = f"2023-11-20"
    valueset[f"publisher"] = f"KinD Lab"
    valueset[f"contact"] = [
        {
            f"name": f"KinD Lab",
            f"telecom": [
                {f"system": f"url", f"value": f"http://fhir.kindlab.sickkids.ca"}
            ],
        }
    ]

    valueset[f"description"] = id
    valueset[f"compose"] = dict()

    valueset[f"compose"][f"include"] = [{f"system": f"{CODESYSTEM_URI}{id_str}"}]

    return valueset

class Generator(ABC):
    """
    Abstract base class for FHIR resource generator.
    """

    def __init__(self, config: Config):
        self.config: Config = config
        # TODO: keep track of code systems created so we only ever create one per option
        self.code_system: dict = {}
        self.value_set: dict = {}

class QuestionnaireGenerator(Generator):
    """
    Class for generating FHIR questionnaire resource.
    """

    @classmethod
    def from_dict(cls, questionnaire_dict: dict):
        """
        Parse a dictionary into a FHIR questionnaire resource.
        """
        questionnaire = Questionnaire.parse_raw(questionnaire_dict)
        return questionnaire

    def parse_reproschema_items(self, reproschema_content: OrderedDict):
        """
        Helper function to parse reproschema items into fhir items

        Example of reproschema_items content:

        {
            "items/1": {
                "@id": "items/1",
                ...
            },
            "items/2": {
                "@id": "items/2",
                ...
            },
            ...
        }
        """
        raise NotImplementedError()

    def convert_to_fhir(self, reproschema_content: dict):
        """
        Function used to convert reproschema questionnaire into a fhir json

        Input is a dictionary which maps file: dict, where the dict is the loaded in
        jsonld file.
        """
        fhir_questionnaire = dict()

        # reference to the main schema file
        schema_name = [name for name in reproschema_content.keys() if name.endswith("_schema")][0]
        reproschema_schema = reproschema_content[schema_name]
        reproschema_id = reproschema_schema["@id"].replace("_", "")

        # create fhir questionnaire
        fhir_questionnaire[f"resourceType"] = f"Questionnaire"
        fhir_questionnaire[f"meta"] = {
            f"profile": [
                f"https://voicecollab.ai/fhir/StructureDefinition/vbai-questionnaire"
            ]
        }
        fhir_questionnaire[f"id"] = reproschema_id
        fhir_questionnaire[f"url"] = QUESTIONNAIRE_URI + reproschema_schema[f"@id"].replace("_", "")
        fhir_questionnaire[f"title"] = reproschema_content[f"@id"]

        fhir_questionnaire[f"text"] = {
            f"status": f"generated",
            f"div": f'<div xmlns="http://www.w3.org/1999/xhtml">Placeholder</div>',
        }
        fhir_questionnaire[f"version"] = f"1.4.0"
        fhir_questionnaire[f"status"] = f"active"
        fhir_questionnaire[f"date"] = f"2023-11-20T11:33:15-05:00"
        fhir_questionnaire[f"publisher"] = f"KinD Lab"
        fhir_questionnaire[f"contact"] = [
            {
                f"name": f"KinD Lab",
                f"telecom": [
                    {f"system": f"url", f"value": f"http://fhir.kindlab.sickkids.ca"}
                ],
            }
        ]

        fhir_questionnaire[f"item"] = []

        group = dict()
        group[f"linkId"] = f"T1"

        if f"preamble" in reproschema_schema.keys():
            if isinstance(reproschema_schema[f"preamble"], dict):
                group[f"text"] = reproschema_schema[f"preamble"]["en"]
            elif isinstance(reproschema_schema[f"preamble"], str):
                group[f"text"] = reproschema_schema[f"preamble"]
        else:
            group[f"text"] = ""

        group[f"type"] = f"group"

        # create a pointer to the reproschema_items jsons
        reproschema_items = OrderedDict(
            [
                (i, reproschema_content[i])
                for i in reproschema_content.keys()
                if i.startswith("items/")
            ]
        )

        items = []
        for item_path, item_json in reproschema_items.items():
            curr_item = dict()

            var_name = item_json["@id"]
            curr_item[f"linkId"] = var_name

            item_type = f"string"
            if f"inputType" in item_json[f"ui"]:
                if item_json[f"ui"][f"inputType"] == f"radio":
                    item_type = f"choice"
                elif item_json[f"ui"][f"inputType"] in (f"number", f"xsd:int"):
                    item_type = f"integer"
                # TODO: else what?

            curr_item[f"type"] = item_type

            # TODO: turn into a get_i18n function, which automatically
            # uses a self.language arg to pull the relevant language from the dict
            if f"question" in item_json and isinstance(
                item_json[f"question"], dict
            ):
                curr_item[f"text"] = str(item_json[f"question"][f"en"])
            else:
                curr_item[f"text"] = str(item_json[f"prefLabel"])

            # now we prepare the ValueSet used for the response options
            # there are a few possibilities for responses presented by reproschema:
            # 1. responseOptions is a string, which is a reference to a file with the responses
            # 2. responseOptions is a dict, which is a list of options

            # prepare the valueset
            value_set = None
            code_system = None

            id_str: str = reproschema_schema["@id"] + item_json["variableName"]
            id_str = id_str.replace("_", "-")
            id_str = id_str.lower()

            if f"responseOptions" in item_json:
                # if responseOptions is a string, it is a reference to a constraint file
                # TODO: refactor this out into a separate function
                # once that is done, the argument signature can be reproschema_items only
                if isinstance(item_json[f"responseOptions"], str):
                    # resolve the path relative to the items folder to load in the dict
                    options_path = Path(item_path).parent / item_json[f'responseOptions']
                    options_path = options_path.resolve()
                    options_json = reproschema_content[str(options_path)]

                    # create a code system for this
                    code_system = generate_code_system(options_json, id_str)
                    if id_str not in self.code_system:
                        self.code_system[id_str] = code_system
                elif isinstance(item_json["responseOptions", dict]):
                    if f"choices" in item_json[f"responseOptions"]:
                        options_json = item_json[f"responseOptions"]
                        code_system = generate_code_system(options_json, id_str)
                        if id_str not in self.code_system:
                            self.code_system[id_str] = code_system

            if code_system is not None:
                value_set = generate_value_set(id_str)
                if id_str not in self.value_set:
                    self.value_set[id_str] = value_set
                curr_item["answerValueSet"] = value_set[f"url"]
            group[f"item"].append(curr_item)

            curr_item[f"linkId"] = var_name
            curr_item[f"type"] = f"string"
            curr_item[f"text"] = str(item_json[f"prefLabel"])
            items.append(curr_item)
        group[f"item"] = items

        fhir_questionnaire[f"item"].append(group)
        return fhir_questionnaire
