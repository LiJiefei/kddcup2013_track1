#!/bin/bash

if [ $# -ne 1 ]
then
    echo "usage: <SETTINGS.json>"
    exit -1
fi


model_dir=`python -c "import json;print json.loads(open(\"$1\").read())['model_path']"`
submission_csv=`python -c "import json;print json.loads(open(\"$1\").read())['submission_path']"`



python src/predict/postprocess-rule-base-code/postprocess.py --setting $1 --rules_list_file src/predict/postprocess-rule-base-code/rules.list --submission_list_file src/predict/postprocess-rule-base-code/submission.list


python src/predict/postprocess-rule-base-code/average-rank.py $model_dir src/predict/postprocess-rule-base-code/ensemble.list $submission_csv 

