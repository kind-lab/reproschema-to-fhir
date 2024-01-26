# reproschema-to-fhir

Transform ReproSchema files into FHIR resources.

## Quickstart

1. Clone this project and create a folder to store the questionnaire you wish to transform from reproschema to FHIR.
2. Create a .env file in the directory where you cloned this project. Please see .env.example for reference.
3. Run the main bash script: `./job.sh` to run all questionnaires or to run the script on an individual questionnaire:   `python main.py <path of reproschema folder>`  

Once executed, you should have 3 json files containing the questionnaire resource and their associated valuesets and codesystems in your current directory.

**NOTE**: In order to keep all the code systems and valuesets in their respective files, all the json are appended into a list. If you wish to add them into a FHIR store, you must create an individual json file for each element in the list.

## Installation

### Clone this repository

Clone this repository recursively to include the reproschema-library submodule.

```sh
git clone git@github.com:kind-lab/reproschema-to-fhir --recursive
```

### Create conda environment

```sh
conda env create -f environment.yml
```


## Misc

### ReproSchema as submodule

We are using reproschema as a submodule. To add reproschema as a submodule, the following commands were run in the main directory of this project:

```sh
git submodule add https://github.com/ReproNim/reproschema-library/ reproschema-library
cd reproschema-library
git checkout 43e7afab312596708c0ad4dfd45b69c8904088ae
cd ..
```