# --encoding:utf-8 -

'''

1) dading 计算的keywords的cos simi
2) 大丁计算的keywords的jaccard simi


###
不加(2)会提高0.0004
####
'''

from Data import *
from collections import defaultdict as ddict
from myutil import *
import sys
import re

class FeatureGenerator0515_todo12:
    def __init__(self, data):
        self.data = data
        self.get_intermediate_data()
    

    def get_intermediate_data(self):
        return 

    def get_feature(self, authorid, paperid):
        return [self.data.authorpaper_simi_dict[(authorid, paperid)][0]]



