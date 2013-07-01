
from Data import *

from myutil import *
from collections import defaultdict as ddict


class rule0616:
    def __init__(self, data):
        self.data = data
        need_papers = get_need_papers(self.data)
        need_authors = get_need_authors(self.data)

        pa_cnt = ddict(int)
        for (paperid, authorid, name, affi) in data.paperauthor_tuples:
            if paperid in need_papers and authorid in need_authors:
                pa_cnt[(paperid, authorid)] += 1

        self.pa_cnt = pa_cnt


    def postprocess(self, authorid, paperlist): 
        pred_list = list()
        l = len(paperlist)
        for i in range(l):
            if paperlist[i] not in paperlist[0:i]:
                pred_list.append(paperlist[i])
        
        firstlist = list()
        endlist = list()
        for paperid in pred_list:
            if self.pa_cnt[(paperid, authorid)] >= 2:
                firstlist.append(paperid)
            else:
                endlist.append(paperid)
        
        return firstlist + endlist

