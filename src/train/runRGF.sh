

if [ $# -ne 4 ]
then
    echo "usage: <SETTINGS.json> <cut_str> <reg> <num_leaf>"
    exit -1
fi

train_csv=`python -c "import json;print json.loads(open(\"$1\").read())['train_csv']"`
train_features_file=`python -c "import json;print json.loads(open(\"$1\").read())['train_feature_file']"`

rgf_model_dir=`python -c "import json;print json.loads(open(\"$1\").read())['model_path']"`
rgf_root=`python -c "import json;print json.loads(open(\"$1\").read())['RGF_ROOT']"`



cut_str=$2
reg=$3
num_leaf=$4

rgf_model_dir=$rgf_model_dir"/RGF-MODEL-$cut_str-$reg-$num_leaf/"

echo $train_features_file $rgf_model_dir

if [ ! -d $rgf_model_dir ]
then
    mkdir -p $rgf_model_dir
fi

if [ ! -d "src/train/tmp" ]
then
    mkdir -p src/train/tmp
fi

rgf_train_y="src/train/tmp/train-rgf-$cut_str-$reg-$num_leaf.y"
rgf_train_x="src/train/tmp/train-rgf-$cut_str-$reg-$num_leaf.x"
rgf_train_w="src/train/tmp/train-rgf-$cut_str-$reg-$num_leaf.w"


awk '{if($1==0)print -1;else {print 1}}' $train_features_file > $rgf_train_y

python src/train/cutfeafile.py --feature_file $train_features_file --feature_select_str $cut_str --output $rgf_train_x

python src/train/genWeights.py < $train_csv > $rgf_train_w



$rgf_root/bin/rgf train train_x_fn=$rgf_train_x,train_y_fn=$rgf_train_y,train_w_fn=$rgf_train_w,model_fn_prefix=$rgf_model_dir/model,algorithm=RGF,reg_L2=$reg,loss=Log,test_interval=100,max_leaf_forest=$num_leaf,Verbose,Time


