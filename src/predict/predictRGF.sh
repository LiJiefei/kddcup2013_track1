

if [ $# -ne 4 ]
then
    echo "usage: <SETTINGS.json> <cut_str> <reg> <num_leaf>"
    exit -1
fi

valid_features_file=`python -c "import json;print json.loads(open(\"$1\").read())['valid_feature_file']"`

model_dir=`python -c "import json;print json.loads(open(\"$1\").read())['model_path']"`
valid_csv=`python -c "import json;print json.loads(open(\"$1\").read())['valid_csv']"`
submission_csv=`python -c "import json;print json.loads(open(\"$1\").read())['submission_path']"`

rgf_root=`python -c "import json;print json.loads(open(\"$1\").read())['RGF_ROOT']"`

cut_str=$2
reg=$3
num_leaf=$4

rgf_pred_file="$model_dir/RGF-$cut_str-$reg-$num_leaf.predictions"
rgf_model_dir=$model_dir"/RGF-MODEL-$cut_str-$reg-$num_leaf/"

echo $valid_features_file $rgf_model_dir $rgf_pred_file


if [ ! -d $rgf_model_dir ]
then
    echo "Please run the RGF model first!!"
    exit -1
fi

if [ ! -d src/predict/tmp ]
then
    mkdir -p src/predict/tmp
fi
rgf_valid_x="src/predict/tmp/valid-rgf-$cut_str-$reg-$num_leaf.x"
python src/predict/cutfeafile.py --feature_file $valid_features_file --feature_select_str $cut_str --output $rgf_valid_x



model_tag=`echo $num_leaf | awk '{print $1/100}'`
$rgf_root/bin/rgf predict test_x_fn=$rgf_valid_x,model_fn=$rgf_model_dir/model-$model_tag,prediction_fn=$rgf_pred_file


rgf_submission_file="$model_dir/RGF-$cut_str-$reg-$num_leaf.submissions.csv"
python src/predict/genPredictionCsv.py -p $rgf_pred_file -i $valid_csv -o $rgf_submission_file




