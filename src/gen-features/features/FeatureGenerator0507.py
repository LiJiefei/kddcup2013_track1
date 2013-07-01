# -- encoding: utf-8 -

from myutil import *
from collections import defaultdict as ddict

'''
1) coauthor ²»³öÏÖÔÚ author.csvµÄ¸öÊý

'''

class FeatureGenerator0507:
    def __init__(self, data):
        self.data = data
        self.get_intermediate_data()
        return
    
    def get_intermediate_data(self):
        need_papers = get_need_papers(self.data)
        paper_authors = ddict(set)
        for (paperid, authorid, name, affi) in self.data.paperauthor_tuples:
            if paperid in need_papers:
                paper_authors[paperid].add(authorid)
        self.paper_authors = paper_authors

    def get_feature(self, authorid, paperid):
        cnt = 0
        for coauthor in self.paper_authors[paperid]:
            if coauthor != authorid and coauthor not in self.data.author_info_dict:
                cnt += 1
        return [cnt]
            
