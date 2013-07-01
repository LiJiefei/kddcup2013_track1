
import csv

'''
1) add the f36 feature

'''

def read_myfeature_file(myfeature_csv):
    csv_reader = csv.reader(file(myfeature_csv))
    csv_reader.next()
    authorpaper_features = dict()
    for cols in csv_reader:

        authorid = int(cols[0])
        paperid = int(cols[1])
        preds = map(float, cols[2:])
        authorpaper_features[(authorid, paperid)] = preds
    return authorpaper_features


class FeatureGenerator0613:
    def __init__(self, data):
        self.data = data
        self.authorpaper_features = read_myfeature_file('%s/features-0605-f36.csv' % data.info_input)

    def get_feature(self, authorid, paperid):
        return self.authorpaper_features[(authorid, paperid)]




       

