# --encoding: gbk -
'''

1) add the feature of dading, base on my fold
2) add the feature of dading, base on dading fold

'''
import csv
from collections import defaultdict as ddict

def read_dading_simi_csv(dading_simi_csv):
    select_feaid_str =  [469, 470, 471, 472, 461, 462, 463, 464, 313, 314, 315, 316, 365, 366, 367, 368, 42, 473, 474, 475, 476, 201, 202, 203, 204, 465, 466, 467, 468, 309, 310, 311, 312, 213, 214, 215, 216, 174, 39, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 249, 250, 251, 252, 205, 206, 207, 208]

    csv_reader = csv.reader(file(dading_simi_csv))
    csv_reader.next()
    authorpaper_simi_dict = dict()
    for cols in csv_reader:
        authorid = int(cols[0])
        paperid = int(cols[1])
        fealist = list()
        for idx in select_feaid_str:
            fealist.append(float(cols[idx]))

        authorpaper_simi_dict[(authorid, paperid)] = fealist

    return authorpaper_simi_dict

class FeatureGenerator0615_todo2:
    def __init__(self, data):
        self.data = data
        self.authorpaper_simi_dict = read_dading_simi_csv(self.data.info_input + '/dading_data/0611_similarity/features.csv')
        return

    def get_feature(self, authorid, paperid):
        return self.authorpaper_simi_dict[(authorid, paperid)]

