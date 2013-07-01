# --encoding:utf-8 -

'''

1) coauthor ÔÚpaÖĞ³öÏÖµÄ×î´ó´ÎÊı
2) coauthor ÔÚpaÖĞÊÇ·ñ³öÏÖ2´Î
3) µ±Ç°paper³öÏÖ³¬¹ıÁ½´ÎµÄcoauthorÊıÁ¿ÓĞÃ»ÓĞÓÃ£
4) 3/coauthor num (3+4 1fold 0.001-, 3 1fold 0.0004+)

'''

from Data import *
from collections import defaultdict as ddict
from myutil import *
import sys
import re

class FeatureGenerator0516_todo12:
    def __init__(self, data):
        self.data = data
        self.get_intermediate_data()
    

    def get_intermediate_data(self):
        need_papers_set = get_need_papers(self.data)
        authorpaper_count = ddict(int)
        paper_authorlist = ddict(set)
        for (paperid, authorid, name, affi) in self.data.paperauthor_tuples:
            if paperid in need_papers_set:
                authorpaper_count[(authorid, paperid)] += 1
                paper_authorlist[paperid].add(authorid)

        self.authorpaper_count = authorpaper_count
        self.paper_authorlist = paper_authorlist 
        return 

    def get_feature(self, authorid, paperid):
        coauthor_maxpa_count = 0
        coauthor_pacount2_flag = 0
        coauthor_pacount2_cnt = 0
        coauthor_num = len(self.paper_authorlist[paperid])
        for coauthor in self.paper_authorlist[paperid]:
            if coauthor != authorid:
                pacount = self.authorpaper_count[(coauthor, paperid)] 
                coauthor_maxpa_count = max(pacount, coauthor_maxpa_count)
                if pacount == 2:
                    coauthor_pacount2_flag = 1
                    coauthor_pacount2_cnt += 1
            
        return [coauthor_maxpa_count, coauthor_pacount2_flag, coauthor_pacount2_cnt]



