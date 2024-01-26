#!/bin/bash

arr=(./b2ai-reproschemav3.1/activities/*) # change based on where your reproschema folders are
arr=("${arr[@]%/}")
arr=("${arr[@]##*/}") 

for folder in "${arr[@]}"; do
    python main.py ./b2ai-reproschemav3.1/activities/"${folder}"
done



