# --encoding:utf-8 -

'''

1) dading �����keywords��cos simi
2) �󶡼����keywords��jaccard simi


###
����(2)�����0.0004
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



