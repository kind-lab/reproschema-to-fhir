# reproschema-to-fhir

This repository provides software to convert from a [ReproSchema protocol](https://www.repronim.org/reproschema/) into a set of [FHIR resources](https://www.hl7.org/fhir/).


## Quickstart

```sh
git clone git@github.com:kind-lab/reproschema-to-fhir --recursive
cd reproschema-to-fhir
mkdir fhir_output
cp .env.example .env

# create the python environment
conda env create -f environment.yml
pip install -e .
# Edit .env to point to the correct location of the reproschema-library
bash job.sh
```

## Detailed steps

0. Clone this project *recursively*.
    * `git clone git@github.com:kind-lab/reproschema-to-fhir --recursive`
    * If you've already cloned the repo, you can pull the submodule with `git submodule update --init --recursive`
0. Create a folder to store the questionnaire you wish to transform from reproschema to FHIR.
0. Create a .env file in the directory where you cloned this project. Please see .env.example for reference.
0. Create a conda environment using the environment.yml file provided in the repository.
    * `conda env create -f environment.yml`
0. Install the reproschema_to_fhir Python module
    * `pip install -e .`
    * This is an editable install that symlinks the local files, allowing you to make changes to the code and see the changes reflected immediately.
0. Run the main bash script: `./job.sh` to run all questionnaires or to run the script on an individual questionnaire:   `python main.py <path of reproschema folder>`  

Once executed, you should have 3 json files containing the questionnaire resource and their associated valuesets and codesystems in your current directory.


## Installation

### Clone this repository

Clone this repository recursively to include the reproschema-library submodule.

```sh
git clone git@github.com:kind-lab/reproschema-to-fhir --recursive
```

### Create conda environment

```sh
conda env create -f environment.yml
pip install -e .
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