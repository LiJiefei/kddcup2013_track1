# --encoding:utf-8 -

'''

1) coauthor这个cid或者jid发表的个数
2) coauthor这个cid或者jid发表的个数/(author在这个cid或者jid发表过的个数)
3) coauthor是否存在同名,判断Rong Pan和R. Pan
4) coauthor的所有affi 与 author在author.csv中的affi 匹配的个数, 非空

5) coauthor在train.csv 删除该paper的个数
6) coauthor在train.csv 确认该paper的个数
7) 5/coauthor的个数
8) 6/coauthor的个数


'''
from Data import *
from collections import defaultdict as ddict
from myutil import *
import sys

class FeatureGenerator0513_todo5678:
    def __init__(self, data):
        self.data = data
        self.get_intermediate_data()
    
    def get_intermediate_data(self):

        author_deleted_paperset = ddict(set)
        author_confirmed_paperset = ddict(set)
        for (authorid, paperid, label) in self.data.train_tuples:
            if label == 1:
                author_confirmed_paperset[authorid].add(paperid)
            else:
                author_deleted_paperset[authorid].add(paperid)

        need_paper_set = get_need_papers(self.data)
        self.paper_author_list = get_paper_authorlist(self.data, need_paper_set)
        self.author_deleted_paperset = author_deleted_paperset
        self.author_confirmed_paperset = author_confirmed_paperset
        return 

    def get_feature(self, authorid, paperid):
        
        coauthor_num = 0
        coauthor_deleted_num = 0
        coauthor_confired_num = 0
        for coauthor in self.paper_author_list[paperid]:
            if coauthor != authorid:
                if paperid in self.author_deleted_paperset[coauthor]:
                    coauthor_deleted_num += 1
                    coauthor_num += 1
                if paperid in self.author_confirmed_paperset[coauthor]:
                    coauthor_confired_num += 1
                    coauthor_num += 1
        
        if coauthor_num == 0:
            return [-1,-1,-1,-1]
        else:
            return [coauthor_confired_num, coauthor_deleted_num, float(coauthor_confired_num)/coauthor_num, float(coauthor_deleted_num)/coauthor_num]

