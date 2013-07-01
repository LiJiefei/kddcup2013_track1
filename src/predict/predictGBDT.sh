
#!/bin/bash

if [ $# -ne 3 ]
then
    echo "usage: <SETTINGS.json> <cut_str> <learning_rate>"
    exit -1
fi



model_dir=`python -c "import json;print json.loads(open(\"$1\").read())['model_path']"`

valid_csv=`python -c "import json;print json.loads(open(\"$1\").read())['valid_csv']"`
submission_csv=`python -c "import json;print json.loads(open(\"$1\").read())['submission_path']"`

cut_str=$2
learning_rate=$3


python src/predict/predictGBDT.py --setting $1 --cut_str $cut_str --learning_rate $learning_rate

gbdt_pred_file="$model_dir/GBDT-$cut_str-$learning_rate.predictions"


gbdt_submission_file="$model_dir/GBDT-$cut_str-$learning_rate.submissions.csv"


python src/predict/genPredictionCsv.py -p $gbdt_pred_file -i $valid_csv -o $gbdt_submission_file

