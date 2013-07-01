

if [ $# -ne 1 ]
then
    echo "usage: <SETTINGS.json>"
    exit -1
fi


bash src/predict/predictRGF.sh $1 4-11_13-end 0.02 1000  &
bash src/predict/predictRGF.sh $1 1-11_13-35 0.01 2000 &
bash src/predict/predictGBDT.sh $1 4-11_13-35 0.1 &
bash src/predict/predictGBDT.sh $1 1-11_13-end 0.08 &
bash src/predict/predictRGF.sh $1 1-11_13-end 0.02 1000  &
bash src/predict/predictGBDT.sh $1 1-35 0.1 &
bash src/predict/predictRGF.sh $1 4-11_13-end 0.02 2000 &


wait

bash src/predict/postprocess-rule-base-code/run-postprocess.sh $1


