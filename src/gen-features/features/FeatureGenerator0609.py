# --encoding: gbk -

'''
1) coauthor µÄname ºÍ author µÄ nameµÄÏàËÆ¶È (ÏàËÆ¶ÈÓÃauthor.csv) À©Õ¹min,max,mean,stdev,sum
2) Í¬1) µ«ÊÇcoauthor°üÀ¨µ±Ç°µÄauthor
3) coauthor µÄaffi ºÍ author µÄ affiµÄÏàËÆ¶È (ÏàËÆ¶ÈÓÃaffi.csv) À©Õ¹min,max,mean,stdev,sum
4) Í¬3) µ«ÊÇcoauthor°üÀ¨µ±Ç°µÄauthor
'''


import math
from collections import defaultdict as ddict
from myutil import *


import Levenshtein

def nameSimi(s1, s2):
    if not s1 or not s2:
        return 0.0
    d = {}
    def dp(s1, s2):
        key = (tuple(s1), tuple(s2))
        if key in d:
            return d[key]
        if not s1 or not s2:
            return 0
        best = dp(s1[1:], s2)
        for s2i in s2:
            w = Levenshtein.jaro_winkler(s1[0], s2i)
            best = max(best, w + dp(s1[1:], s2 - set([s2i])))
        d[key] = best
        return best
    return dp(s1.lower().split(), set(s2.lower().split()))\
        / float(min(len(s1.split()), len(s2.split())))

def affiSimi(s1, s2):
    if not s1 or not s2:
        return 0.0
    if len(s1) == 0 and len(s2) == 0:
        return 1.0
    if len(s1) == 0 or len(s2) == 0:
        return 0.0
    return Levenshtein.seqratio(re.split(r',| ', s1.lower()), re.split(r',| ', s2.lower()))

def cal_max_min_mean_std_sum(similist):
    min_simi = 10.0
    max_simi = -1
    mean_simi = 0
    stddev = 0.0
    for simi in similist:
        min_simi = min(simi, min_simi)
        max_simi = max(simi, max_simi)
        mean_simi += simi
    sum_simi = mean_simi
    mean_simi/= len(similist)
    for simi in similist:
        stddev += (simi-mean_simi)**2

    stddev /= len(similist)
    stddev = math.sqrt(stddev)
    return [max_simi, min_simi, mean_simi, stddev, sum_simi]

class FeatureGenerator0609:
    def __init__(self, data):
        self.data = data
        need_authors = get_need_authors(self.data)
        need_papers = get_need_papers(self.data)
        paper_author_name = ddict(lambda: ddict(set))
        paper_author_affi = ddict(lambda: ddict(set))

        for (paperid, authorid, name, affi) in self.data.paperauthor_tuples:
            if paperid in need_papers:
                if len(name) > 0:
                    paper_author_name[paperid][authorid].add(name)
                paper_author_affi[paperid][authorid].add(affi)
        
        self.paper_author_name = paper_author_name
        self.paper_author_affi = paper_author_affi

        return

    def get_feature(self, authorid, paperid):
        coauthor_name_set = set()
        author_name_set = set()
        coauthor_affi_set = set()
        author_affi_set = set()
        for coauthor, nameset in self.paper_author_name[paperid].items():
            if coauthor != authorid:
                coauthor_name_set |= nameset
            else:
                author_name_set = nameset
        
        for coauthor, affiset in self.paper_author_affi[paperid].items():
            if coauthor != authorid:
                coauthor_affi_set |= affiset
            else:
                author_affi_set = affiset

        
        fea1_list = list()
        fea2_list = list()
        fea3_list = list()
        fea4_list = list()

        if authorid not in self.data.author_info_dict:
            fea1_list = [-2]*5
            fea2_list = [-2]*5
            fea3_list = [-2]*5
            fea4_list = [-2]*5
        else:
            if len(coauthor_name_set) == 0:
                fea1_list = [-1]*5
                fea2_list = [-1]*5
                fea3_list = [-1]*5
                fea4_list = [-1]*5
            else:
                name_similist1 = list()
                name_similist2 = list()
                cur_author_name = self.data.author_info_dict[authorid]['name']
                cur_author_affi = self.data.author_info_dict[authorid]['affi']
                for coauthor_name in coauthor_name_set:
                    name_similist1.append(nameSimi(coauthor_name, cur_author_name))
                for author_name in author_name_set:
                    name_similist2.append(nameSimi(author_name, cur_author_name))
                name_similist2 = name_similist2 + name_similist1
                fea1_list = cal_max_min_mean_std_sum(name_similist1)
                fea2_list = cal_max_min_mean_std_sum(name_similist2)

                affi_similist1 = list()
                affi_similist2 = list()
                for coauthor_affi in coauthor_affi_set:
                    affi_similist1.append(affiSimi(coauthor_affi, cur_author_affi))
                for author_affi in author_affi_set:
                    affi_similist2.append(affiSimi(author_affi, cur_author_affi))
                affi_similist2 = affi_similist2 + affi_similist1

                fea3_list = cal_max_min_mean_std_sum(affi_similist1)
                fea4_list = cal_max_min_mean_std_sum(affi_similist2)

        return fea1_list + fea2_list + fea3_list + fea4_list
