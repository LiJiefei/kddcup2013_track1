
#!/bin/bash



cp data/Train.csv data/TrainMergeValid.csv

python src/train/merge.py data/Valid.csv data/ValidSolution.csv | sed -n '2,$p' >> data/TrainMergeValid.csv 

