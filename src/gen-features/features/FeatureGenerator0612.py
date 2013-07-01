# --encoding: gbk -
'''

1) stacking

'''
import csv
from collections import defaultdict as ddict
from myutil import *


class FeatureGenerator0612:
    def __init__(self, data):
        self.data = data
        self.authorpaper_preds = read_predictions_file('%s/predictions_data/predictions-0612-2149.csv' % (data.info_input))
        return

    def get_feature(self, authorid, paperid):
        return self.authorpaper_preds[(authorid, paperid)]

