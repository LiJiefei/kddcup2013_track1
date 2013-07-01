'''

1) add the feature of weige + 0517, (0.00007+)
2) author csv affi id
3) paperauthor csv affi id
#4) paperid

'''

from Levenshtein import *
from collections import defaultdict as ddict
from myutil import *

class FeatureGenerator0518_todo23:
    def __init__(self, data):
        self.data = data
        affi_dict = dict()
        affi_cnt = 0
        need_authorpaper_pair = get_need_authorpaper_pair(self.data)
        ap_pair_affi = dict()
        ap_pair_cnt = ddict(int)
        for author, info_dict in self.data.author_info_dict.items():
            affi = info_dict['affi']
            if affi not in affi_dict:
                affi_dict[affi] = affi_cnt
                affi_cnt += 1
        for (paperid, authorid, name, affi) in self.data.paperauthor_tuples:
            if affi not in affi_dict:
                affi_dict[affi] = affi_cnt
                affi_cnt += 1
            k = (authorid, paperid)
            if k in need_authorpaper_pair:
                ap_pair_affi[k] = affi
                ap_pair_cnt[k] += 1
        self.affi_dict = affi_dict
        self.ap_pair_affi = ap_pair_affi
        self.ap_pair_cnt = ap_pair_cnt
        return

    def get_feature(self, authorid, paperid):
        author_affi_id = -1
        if authorid in self.data.author_info_dict:
            author_affi = self.data.author_info_dict[authorid]['affi']
            author_affi_id = self.affi_dict[author_affi]

        pa_affi_id = -1
        k = (authorid, paperid)
        pa_affi = self.ap_pair_affi[(authorid, paperid)]
        if self.ap_pair_cnt[k] == 1:
            pa_affi_id = self.affi_dict[pa_affi]
        return [author_affi_id, pa_affi_id, paperid]


