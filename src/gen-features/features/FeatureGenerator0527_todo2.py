# --encoding: gbk -
'''

2) Ëãµ±Ç°authorµÄpa>=2µÄÆäËûpaperµÄauthorµÄ¼¯ºÏºÍµ±Ç°coauthorµÄ½»¼¯µÄ´óÐ¡Ö®ºÍ

'''

from collections import defaultdict as ddict
from myutil import *

class FeatureGenerator0527_todo2:
    def __init__(self, data):
        self.data = data
        need_authors = get_need_authors(self.data)
        author_paper_count = ddict(lambda: ddict(int))
        for (paper, author, name, affi) in self.data.paperauthor_tuples:
            if author in need_authors:
                author_paper_count[author][paper] += 1
        
        author_paper_pa2 = ddict(set)
        paper_authorset = ddict(set)
        for author, paper_count in author_paper_count.items():
            for paper,cnt in paper_count.items():
                if cnt >= 2:
                    author_paper_pa2[author].add(paper)
                    paper_authorset[paper] = set()

        for (paper, author, name, affi) in self.data.paperauthor_tuples:
            if paper in paper_authorset:
                paper_authorset[paper].add(author)

        self.author_paper_pa2 = author_paper_pa2
        self.paper_authorset = paper_authorset
        return

    def get_feature(self, authorid, paperid):
        sum_cnt = 0
        cur_author_set = set(self.paper_authorset[paperid])
        for co_paper in self.author_paper_pa2[authorid]:
            if co_paper != paperid:
                sum_cnt += len(cur_author_set & self.paper_authorset[co_paper])
        return [sum_cnt]

