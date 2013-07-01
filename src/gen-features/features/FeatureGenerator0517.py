

import Levenshtein
from Data import *
from collections import defaultdict as ddict
from myutil import *

class FeatureGenerator0517:
    def __init__(self, data):
        self.data = data
        need_authorpaper_pair = get_need_authorpaper_pair(self.data)
        authorpaper_affilist = ddict(list)
        for (paperid, authorid, name, affi) in data.paperauthor_tuples:
            k = (authorid, paperid)
            authorpaper_affilist[k].append((name, affi))
        self.authorpaper_affilist = authorpaper_affilist
    
    def get_str_simis(self, str1, str2):
        return [Levenshtein.jaro(str1, str2), Levenshtein.ratio(str1,str2), len(Levenshtein.editops(str1, str2))]
    
    def max_simi(self, simis1, simis2):
        ret = []
        for i in range(len(simis1)):
            ret.append(max(simis1[i], simis2[i]))
        return ret

    def min_simi(self, simis1, simis2):
        ret = []
        for i in range(len(simis1)):
            ret.append(min(simis1[i], simis2[i]))
        return ret

    def get_feature(self, authorid, paperid):
        ret = [1000, 1000, 1000, 1000, 1000, 1000]
        if authorid not in self.data.author_info_dict:
            return ret
        author_name = self.data.author_info_dict[authorid]['name']
        author_affi = self.data.author_info_dict[authorid]['affi']

        for (name, affi) in self.authorpaper_affilist[(authorid, paperid)]:
            ret = self.min_simi(ret, self.get_str_simis(name,author_name) + self.get_str_simis(affi, author_affi))

        return ret

