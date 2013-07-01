'''

1) add the feature of dading 0519

'''

from collections import defaultdict as ddict


class FeatureGenerator0519:
    def __init__(self, data):
        self.data = data
        return

    def get_feature(self, authorid, paperid):
        return self.data.authorpaper_0519_simi_dict[(authorid, paperid)]

