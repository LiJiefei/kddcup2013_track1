# --encoding: gbk -
'''

1) add the dading feature 0611

'''
import csv
from collections import defaultdict as ddict

def read_dading_simi_csv(dading_simi_csv):
    csv_reader = csv.reader(file(dading_simi_csv))
    csv_reader.next()
    authorpaper_simi_dict = dict()
    for cols in csv_reader:
        authorid = int(cols[0])
        paperid = int(cols[1])
        authorpaper_simi_dict[(authorid, paperid)] = map(float, cols[44:])
    return authorpaper_simi_dict

class FeatureGenerator0611:
    def __init__(self, data):
        self.data = data
        self.authorpaper_simi_dict = read_dading_simi_csv(self.data.info_input + '/dading_data/0611_similarity/features.csv')
        return

    def get_feature(self, authorid, paperid):
        return self.authorpaper_simi_dict[(authorid, paperid)]

