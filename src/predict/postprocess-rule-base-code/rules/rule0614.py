
from Data import *

from myutil import *
from collections import defaultdict as ddict


class rule0614:
    def __init__(self, data):
        self.data = data
        need_papers = get_need_papers(self.data)
        paper_authorlist = ddict(list)
        pa_cnt = ddict(int)
        for (paperid, authorid, name, affi) in data.paperauthor_tuples:
            if paperid in need_papers:
                paper_authorlist[paperid].append((authorid, name))
                pa_cnt[(paperid, authorid)] += 1

        self.paper_authorlist = paper_authorlist
        self.pa_cnt = pa_cnt


    def postprocess(self, authorid, paperlist):
        
        author_csv_name = ''
        if authorid in self.data.author_info_dict:
            author_csv_name = self.data.author_info_dict[authorid]['name']
        

        pred_list = list()
        l = len(paperlist)
        for i in range(l):
            if paperlist[i] not in paperlist[0:i]:
                pred_list.append(paperlist[i])
        
        if re.match('^([A-Z]\. ){1,10}[A-Za-z]+$', author_csv_name):
            return pred_list

        pa2_ratio = 0.0

        for paperid in pred_list:
            if self.pa_cnt[(paperid,authorid)] >= 2:
                pa2_ratio += 1

        pa2_ratio /= len(pred_list)
        
        if pa2_ratio >= 0.001 and pa2_ratio <= 1.0:
            return pred_list
        

        put_back_papers = list()
        for paperid in pred_list:
            coauthor_num = 0
            short_name_num = 0
            for (coauthor, name) in self.paper_authorlist[paperid]:
                if coauthor != authorid:
                    coauthor_num += 1
                    if re.match('^([A-Z]\. ){1,10}[A-Za-z]+$', name):
                        short_name_num += 1
                    

            if short_name_num == coauthor_num:
                put_back_papers.append(paperid)
        
        print '%d,%s' % (authorid, ' '.join(map(str, put_back_papers)))
        ans_list = list()
        for paperid in pred_list:
            if paperid not in put_back_papers:
                ans_list.append(paperid)
        ans_list += put_back_papers
        return ans_list

