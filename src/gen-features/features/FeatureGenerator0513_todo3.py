# --encoding:utf-8 -

'''

1) coauthor这个cid或者jid发表的个数
2) coauthor这个cid或者jid发表的个数/(author在这个cid或者jid发表过的个数)
3) coauthor是否存在同名,判断Rong Pan和R. Pan
4) coauthor中共同发表过的cid
5) coauthor中共同表表过的jid的个数


'''
from Data import *
from collections import defaultdict as ddict
from myutil import *

class FeatureGenerator0513_todo3:
    def __init__(self, data):
        self.data = data
        self.get_intermediate_data()

    def cal_name_simi(self,name1,name2):
        name1_cols = name1.split()
        name2_cols = name2.split()
        if len(name1_cols) != len(name2_cols):
            return 0
        l = len(name1_cols)
        for i in range(l):
            if '.' in name1_cols[i] or '.' in name2_cols[i] or len(name1_cols[i]) == 1 or len(name2_cols[i])==1:
                if name1_cols[i][0] != name2_cols[i][0]:
                    return 0
            else:
                if name1_cols[i] != name2_cols[i]:
                    return 0
        return 1
    
    def get_intermediate_data(self):
        paper_authorname_list = ddict(list)
        need_paper_set = get_need_papers(self.data)
        for (paperid, authorid, name, affi) in self.data.paperauthor_tuples:
            if paperid in need_paper_set:
                paper_authorname_list[paperid].append((authorid, name))
        self.paper_authorname_list = paper_authorname_list
        return 

    def get_feature(self, authorid, paperid):
        if authorid not in self.data.author_info_dict:
            return [-1]
        author_name = self.data.author_info_dict[authorid]['name']
        flag = 0
        for (coauthor,co_name) in self.paper_authorname_list[paperid]:
            if coauthor != authorid and self.cal_name_simi(co_name, author_name) == 1:
                flag = 1
                break
        return [flag]





