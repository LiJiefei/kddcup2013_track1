### My team
Author: Jiefei Li, Xiaocong Liang, Weijie Ding, Weidong Yang \<br /\> 
Team: justforfun & let me try & let us try \<br /\> 
School: Sun-Yat Sen University \<br /\> 
Email: lijiefei@mail2.sysu.edu.cn \<br /\> 

### License
Copyright [2013] [Jiefei Li, Xiaocong Liang, Weijie Ding, Weidong Yang ] Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0 Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.

### The hardware / OS platform
Linux, 32G mem, 12-core cpu, 500G disk \<br /\> 

### 3rd-party software
Python2.6 \<br /\> 
sklearn: http://scikit-learn.org/stable/  (version 0.13.1) \<br /\> 
Levenshtein: https://pypi.python.org/pypi/python-Levenshtein/ \<br /\> 
RGF: http://stat.rutgers.edu/home/tzhang/software/rgf/ (please modify the RGF_ROOT in the SETTINGS.json) \<br /\> 



### Before Train Model and Make predictions
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! \<br /\> 
Please Put the Confernce.csv, PaperAuthor.csv, Author.csv, Paper.csv, Jorunal.csv and so on into the data/ \<br /\> 
If you want to change the test set, you can modeify the valid_csv in the SETTINGS.json \<br /\> 

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! \<br /\> 
Notice!! \<br /\> 
TrainMergeValid.csv in the data/ is created by the src/train/merge.sh, it merge the Train.csv and the validSoultion.csv, So we should use the TrainMergeValid.csv as my training data. \<br /\> 
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! \<br /\> 
If you delete the TrainMergeValid.csv, you should run the "bash src/train/merge.sh" to get it again. \<br /\> 
We should generate the features on the trainingSet and testSet. \<br /\> 

Run script: \<br /\> 
bash bin/genfeatures.sh SETTINGS.json \<br /\> 


### How to Train Model
Run script: \<br /\> 
bash bin/train.sh SETTINGS.json \<br /\> 

### How to make predictions on a new test set
If the test set is updated, we should rerun the 3) to get the features file, but if the training set is old, it is not necessary to train the model again. \<br /\> 
Run script: \<br /\> 
bash bin/predict.sh SETTINGS.json \<br /\> 

### Get the submit.csv
the file of the submission_path in the SETTINGS.json is the final submission.  \<br /\> 

