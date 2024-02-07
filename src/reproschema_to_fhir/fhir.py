from abc import ABC, abstractmethod
import os
import json
from collections import OrderedDict
from typing import Optional
from pathlib import Path

from fhir.resources.questionnaire import Questionnaire
from fhir.resources.valueset import ValueSet
from fhir.resources.codesystem import CodeSystem
from datetime import datetime, timezone

from .config import Config


def add_options(options_json, config) -> list:
    """
    Helper function to extract all answer choices to a list
    """
    options = []
    for j in options_json[f"choices"]:
        if "schema:name" in j and j["schema:name"] != "":
            choice = j["schema:name"]
        elif "name" in j and j["name"] != "":
            choice = j[f"name"]
            if config.get_language() in j["name"] and isinstance(["name"],
                                                                 dict):
                choice = choice[config.get_language()]
            else:
                pass
        elif "schema:value" in j:
            choice = j["schema:value"]
        else:
            choice = j["value"]

        if (choice and not isinstance(choice, int)
                and config.get_language() in choice
                and isinstance(choice, dict)):
            choice = choice[config.get_language()]

        choice = str(choice)
        options.append(choice)
    return options


def generate_code_system(options_json, id_str: str, config) -> dict:
    """
    Helper function to generate a FHIR CodeSystem resource from a reproschema options json.
    """
    codeSystem = dict()
    if config.get_mode() == "ValueSet":
        # default headers for codesystem

        codeSystem["resourceType"] = "CodeSystem"
        codeSystem["id"] = id_str
        codeSystem["text"] = {
            "status": "generated",
            "div":
            '<div xmlns="http://www.w3.org/1999/xhtml">Placeholder</div>',
        }

        codeSystem["url"] = f"{config.get_codesystem()}{id_str}"
        codeSystem["version"] = "1.4.0"
        codeSystem["name"] = id_str.capitalize().replace("_", "")
        codeSystem["title"] = id_str
        codeSystem["status"] = "active"
        codeSystem["date"] = (datetime.now(
            timezone.utc)).strftime('%Y-%m-%dT%H:%M:%SZ')
        codeSystem["publisher"] = "KinD Lab"
        codeSystem["contact"] = [{
            "name":
            "KinD Lab",
            "telecom": [{
                "system": "url",
                "value": "http://fhir.kindlab.sickkids.ca"
            }],
        }]

        codeSystem["description"] = id_str
        codeSystem["caseSensitive"] = True
        codeSystem["content"] = "complete"
        codeSystem["count"] = len(options_json["choices"])
        codeSystem["concept"] = []
    else:
        return codeSystem

    options = add_options(options_json, config)
    # we wish to retrieve each option stored in the reproschema json list. We do this by parsing the list
    # of jsons and append then contents to an outlined codesystem
    count = 1

    for j in options_json[f"choices"]:

        codeSystem_option = dict()

        if config.get_mode() == "ValueSet":
            # we parse to string and lsstrip as fhir codes don't allow leading whitespaces
            if "schema:value" in j and j["schema:value"] is not None:
                codeSystem_option["code"] = str(j[f"schema:value"]).lstrip()
            elif "value" in j and j["value"] is not None:
                codeSystem_option["code"] = str(j["value"]).lstrip()
            else:
                codeSystem_option[f"code"] = count
            codeSystem_option[f"display"] = str(options[count - 1])

            codeSystem[f"concept"].append(codeSystem_option)
        count += 1

    return (codeSystem, options)


def generate_value_set(id_str: str, config) -> dict:
    """
    Helper function that generates a FHIR valueset for a given question
    """
    valueset = dict()
    if config.get_mode() != "ValueSet":
        return valueset

    valueset["resourceType"] = "ValueSet"
    valueset["id"] = id_str
    valueset["text"] = {
        "status": "generated",
        "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\">Placeholder</div>"
    }
    valueset["url"] = f"{config.get_valueset()}{id_str}"
    valueset["version"] = "1.4.0"

    valueset["name"] = id_str.capitalize().replace("_", "")
    valueset["title"] = id_str
    valueset["status"] = "active"
    valueset["date"] = str(datetime.today().strftime('%Y-%m-%d'))
    valueset["publisher"] = f"KinD Lab"
    valueset["contact"] = [{
        "name":
        "KinD Lab",
        "telecom": [{
            "system": "url",
            "value": "http://fhir.kindlab.sickkids.ca"
        }]
    }]

    valueset["description"] = id_str
    valueset["compose"] = dict()

    valueset["compose"]["include"] = [{
        "system":
        f"{config.get_codesystem()}{id_str}"
    }]

    return valueset


class Generator(ABC):
    """
    Abstract base class for FHIR resource generator.
    """

    def __init__(self, config: Config):
        self.config: Config = config
        self.code_system_options: dict = {}
        self.code_system: dict = {}
        self.value_set: dict = {}

    def get_code_system(self):
        return self.code_system

    def get_value_set(self):
        return self.value_set


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

    def parse_reproschema_items(self, reproschema_items: OrderedDict,
                                reproschema_content: OrderedDict):
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
        # there are a few possibilities for responses presented by reproschema:
        # 1. responseOptions is a string, which is a reference to a file with the responses
        # 2. responseOptions is a dict, which is a list of options
        items = []

        for item_path, item_json in reproschema_items.items():
            curr_item = dict()

            var_name = item_path.replace("items/", "")
            curr_item["linkId"] = var_name

            item_type = "string"
            if "inputType" in item_json["ui"]:
                if item_json["ui"]["inputType"] == "radio":
                    item_type = f"choice"
                elif item_json["ui"]["inputType"] in ("number", "xsd:int"):
                    item_type = "integer"
                else:
                    item_type = "string"

            curr_item["type"] = item_type

            if "question" in item_json and isinstance(item_json["question"],
                                                      dict):
                curr_item["text"] = str(
                    item_json["question"][self.config.get_language()])
            elif f"prefLabel" in item_json:
                curr_item["text"] = str(item_json["prefLabel"])
            else:
                curr_item[f"text"] = curr_item[f"linkId"]

            # now we prepare the ValueSet used for the response options
            # prepare the valueset
            value_set = None
            code_system = None
            # id must be 64 characters
            id_str: str = var_name
            id_str = id_str.replace("_", "-")
            id_str = id_str.lower()

            if "responseOptions" in item_json:
                # FOR VERSION 1.0.0
                if isinstance(item_json["responseOptions"], str):
                    # resolve the path relative to the items folder to load in the dict
                    codesystem_id_for_valueset = id_str
                    options_path = Path(
                        item_path).parent / item_json['responseOptions']
                    options_path = options_path.resolve()

                    options_json = reproschema_content[(
                        str(options_path)).split("/")[-1]]

                    if (self.config.get_mode() == "ValueSet"):
                        # create a code system for this
                        (code_system, options) = generate_code_system(
                            options_json, id_str, self.config)
                        if tuple(options) not in self.code_system_options:
                            self.code_system_options[tuple(options)] = id_str
                            self.code_system[id_str] = code_system
                        else:
                            codesystem_id_for_valueset = self.code_system_options[
                                tuple(options)]
                            curr_item["linkId"] = var_name
                            curr_item["type"] = "string"
                            curr_item["text"] = str(item_json["question"][
                                self.config.get_language()])
                    elif (self.config.get_mode() == "AnswerOptions"):
                        options = add_options(options_json, self.config)
                        curr_item["linkId"] = var_name
                        curr_item["type"] = "string"
                        curr_item["text"] = str(
                            item_json["question"][self.config.get_language()])
                        curr_item["answerOption"] = [{
                            "valueString": option
                        } for option in options]

                    # VERSION 0.0.1
                elif isinstance(item_json["responseOptions"], dict):
                    # we wish to avoid making identical codesystems. we assume the codesystem
                    # we are making doesnt exist yet. Later when we find out it already exists,
                    # we overright the codesystem_id_for_valueset to the codesystem that matches
                    codesystem_id_for_valueset = id_str
                    if "choices" not in item_json[
                            "responseOptions"] or item_json["responseOptions"][
                                "choices"] is None:
                        curr_item["linkId"] = var_name
                        if "valueType" in item_json[
                                "responseOptions"] and "int" in item_json[
                                    "responseOptions"]["valueType"]:
                            curr_item[f"type"] = f"integer"
                        elif "valueType" in item_json[
                                "responseOptions"] and "date" in item_json[
                                    "responseOptions"]["valueType"]:
                            curr_item["type"] = "date"
                        else:
                            curr_item["type"] = "string"
                        if "question" not in item_json:
                            if "prefLabel" in item_json:
                                curr_item["text"] = str(item_json["prefLabel"])
                            else:
                                curr_item["text"] = curr_item["linkId"]
                        else:
                            curr_item["text"] = str(item_json["question"][
                                self.config.get_language()])
                        code_system = None
                    elif "choices" in item_json["responseOptions"]:
                        options_json = item_json["responseOptions"]
                        options = add_options(options_json, self.config)
                        curr_item["linkId"] = var_name
                        curr_item["type"] = "choice"
                        curr_item["text"] = str(
                            item_json["question"][self.config.get_language()])

                        if self.config.get_mode() == "ValueSet":
                            (code_system, options) = generate_code_system(
                                options_json, id_str, self.config)
                            if tuple(options) not in self.code_system_options:
                                self.code_system_options[tuple(
                                    options)] = id_str
                                self.code_system[id_str] = code_system
                            else:
                                codesystem_id_for_valueset = self.code_system_options[
                                    tuple(options)]
                        elif self.config.get_mode() == "AnswerOptions":
                            curr_item["answerOption"] = [{
                                "valueString": option
                            } for option in options]

            if self.config.get_mode() == "ValueSet" and code_system is not None:
                value_set = generate_value_set(codesystem_id_for_valueset,
                                               self.config)

                if codesystem_id_for_valueset not in self.value_set:
                    self.value_set[codesystem_id_for_valueset] = value_set
                curr_item["answerValueSet"] = value_set["url"]
                curr_item["type"] = "choice"

            items.append(curr_item)
        return items

    def convert_to_fhir(self, reproschema_content: dict):
        """
        Function used to convert reproschema questionnaire into a fhir json

        Input is a dictionary which maps file: dict, where the dict is the loaded in
        jsonld file.
        """
        fhir_questionnaire = dict()

        # reference to the main schema file
        schema_name = [
            name for name in list(reproschema_content.keys())
            if name.endswith("_schema")
        ][0]
        reproschema_schema = reproschema_content[schema_name]

        reproschema_id = (reproschema_schema["@id"]).replace("_", "")

        # create fhir questionnaire
        fhir_questionnaire["resourceType"] = "Questionnaire"
        fhir_questionnaire["meta"] = {
            "profile": [
                f"https://voicecollab.ai/fhir/StructureDefinition/vbai-questionnaire"
            ]
        }
        fhir_questionnaire["id"] = reproschema_id
        fhir_questionnaire[
            "url"] = self.config.QUESTIONNAIRE_URI + reproschema_schema[
                "@id"].replace("_", "")
        fhir_questionnaire["title"] = reproschema_schema["@id"]

        fhir_questionnaire[f"version"] = "1.4.0"
        fhir_questionnaire[f"status"] = "active"
        fhir_questionnaire[f"date"] = (datetime.now(
            timezone.utc)).strftime('%Y-%m-%dT%H:%M:%SZ')
        fhir_questionnaire[f"publisher"] = f"KinD Lab"
        fhir_questionnaire[f"contact"] = [{
            "name":
            "KinD Lab",
            "telecom": [{
                "system": "url",
                "value": "http://fhir.kindlab.sickkids.ca"
            }],
        }]

        fhir_questionnaire["item"] = []

        group = dict()
        group["linkId"] = "T1"

        if "preamble" in reproschema_schema.keys():
            if isinstance(reproschema_schema["preamble"], dict):
                group["text"] = reproschema_schema["preamble"][
                    self.config.get_language()]
            elif isinstance(reproschema_schema["preamble"], str):
                group["text"] = reproschema_schema["preamble"]
        else:
            group["text"] = " "

        group["type"] = "group"

        # create a pointer to the reproschema_items jsons and match the question
        reproschema_items = OrderedDict([
            (i, value) for (i, value) in reproschema_content.items()
            if i.startswith("items/")
        ])

        question_order = [("items/" + sub.replace("items/", ""))
                          for sub in reproschema_schema[f"ui"][f"order"]]

        reproschema_items = OrderedDict(
            (key, reproschema_items[key]) for key in question_order)

        items = self.parse_reproschema_items(reproschema_items,
                                             reproschema_content)

        group[f"item"] = items

        fhir_questionnaire["item"].append(group)
        return fhir_questionnaire
