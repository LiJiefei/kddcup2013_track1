#!/bin/bash 

if [ $# -ne 1 ]
then
    echo "usage: <SETTINGS.json>"
    exit -1
fi

setting_json=$1
python src/gen-features/genFeaturesFile.py --setting $setting_json 

