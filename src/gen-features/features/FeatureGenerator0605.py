# --encoding: gbk -
'''
1) coauthor µÄname ºÍ author µÄ nameµÄÏàËÆ¶È
2) ap >=2 µÄÊ±ºò£¬Ëãµ±Ç°authorµÄËùÓÐµÄnameµÄÁ½Á½Ö®¼äµÄÏàËÆ¶ÈµÄÆ½¾ùÖµ


'''

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

class FeatureGenerator0605:
    def __init__(self, data):
        self.data = data
        need_authors = get_need_authors(self.data)
        need_papers = get_need_papers(self.data)
        paper_author_name = ddict(lambda: ddict(set))
        for (paperid, authorid, name, affi) in self.data.paperauthor_tuples:
            if paperid in need_papers:
                if len(name) > 0:
                    paper_author_name[paperid][authorid].add(name)
        
        self.paper_author_name = paper_author_name
        return

    def get_feature(self, authorid, paperid):
        coauthor_name_set = set()
        author_name_set = set()
        for coauthor, nameset in self.paper_author_name[paperid].items():
            if coauthor != authorid:
                coauthor_name_set |= nameset
            else:
                author_name_set = nameset

        if len(coauthor_name_set) == 0:
            return [-1]
        maxsimi = -1
        for coauthor_name in coauthor_name_set:
            for author_name in author_name_set:
                maxsimi = max(maxsimi, nameSimi(coauthor_name, author_name))
        return [maxsimi]
