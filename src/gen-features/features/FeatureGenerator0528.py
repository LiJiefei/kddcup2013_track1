# --encoding: gbk -
'''

1) add weige feature
2) Í³¼Æ×÷ÕßÔÚµ±Ç°µÄaffiÏÂ·¢±í¹ýµÄpaper
3) Í³¼Æ×÷ÕßÔÚµ±Ç°Äê·ÝÏÂ¸ÃaffiÏÂ·¢±í¹ýµÄpaper


'''

from collections import defaultdict as ddict


def load_weige_feature(ap_fea_dict, featurefile):
    for line in file(featurefile):
        cols = line.strip().split(',')
        ap_fea_dict[(int(cols[0]), int(cols[1]))] = map(float, cols[2].split(','))

class FeatureGenerator0528:
    def __init__(self, data):
        self.data = data
        self.weige_fea_dict = dict()
        load_weige_feature(self.weige_fea_dict, '%s/weige_data/train.30f.txt' % self.data.info_input)
        load_weige_feature(self.weige_fea_dict, '%s/weige_data/val.30f.txt' % self.data.info_input)
        return

    def get_feature(self, authorid, paperid):
        return self.weige_fea_dict[(authorid, paperid)]

