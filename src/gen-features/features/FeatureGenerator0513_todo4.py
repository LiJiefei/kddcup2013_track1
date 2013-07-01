# --encoding:utf-8 -

'''

1) coauthor这个cid或者jid发表的个数
2) coauthor这个cid或者jid发表的个数/(author在这个cid或者jid发表过的个数)
3) coauthor是否存在同名,判断Rong Pan和R. Pan
4) coauthor的所有affi 与 author在author.csv中的affi 匹配的个数, 非空
#4) coauthor中共同发表过的cid
#5) coauthor中共同表表过的jid的个数


'''
from Data import *
from collections import defaultdict as ddict
from myutil import *
import sys

class FeatureGenerator0513_todo4:
    def __init__(self, data):
        self.data = data
        self.get_intermediate_data()
    
    def get_intermediate_data(self):
        need_paper_set = get_need_papers(self.data)
        self.paper_author_list = get_paper_authorlist(self.data, need_paper_set)
        need_author_coauthor_set = set()
        for (paperid, authorid, name, affi) in self.data.paperauthor_tuples:
            if paperid in need_paper_set:
                need_author_coauthor_set.add(authorid)
        author_affi_set = ddict(set)
        for (paperid, authorid, name, affi) in self.data.paperauthor_tuples:
            try:
                if affi.strip() == '' and affi != '':
                    print >> sys.stderr, 'affi error!'
            except:
                sys.exit(-1)
                
            if authorid in need_author_coauthor_set and affi.strip() != '':
                author_affi_set[authorid].add(affi.strip())
        self.author_affi_set = author_affi_set
        return 

    def get_feature(self, authorid, paperid):
        if authorid not in self.data.author_info_dict:
            return [-2]
        author_affi = self.data.author_info_dict[authorid]['affi']
        if author_affi == '':
            return [-1]
        match_cnt = 0
        for coauthor in self.paper_author_list[paperid]:
            if coauthor != authorid and (author_affi in self.author_affi_set[coauthor]):
                match_cnt += 1
        return [match_cnt]





