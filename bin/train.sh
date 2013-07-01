
if [ $# -ne 1 ]
then
    echo "usage: <SETTINGS.json>"
    exit -1
fi


python src/train/runGBDT.py --setting $1 --cut_str 4-11_13-35 --learning_rate 0.1 &
python src/train/runGBDT.py --setting $1 --cut_str 1-11_13-end --learning_rate 0.08 &
python src/train/runGBDT.py --setting $1 --cut_str 1-35 --learning_rate 0.1 &

bash src/train/runRGF.sh $1 4-11_13-end 0.02 1000 &
bash src/train/runRGF.sh $1 1-11_13-35 0.01 2000 &
bash src/train/runRGF.sh $1 1-11_13-end 0.02 1000 &
bash src/train/runRGF.sh $1 4-11_13-end 0.02 2000 &




wait

