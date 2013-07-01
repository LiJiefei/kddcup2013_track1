# -- encoding: utf-8 -

from myutil import *

'''
1) authorºÍcoauthorµÄaffiµÄmatch¸öÊý (0.001+)
'''

class FeatureGenerator0507_2:
    def __init__(self, data):
        self.data = data
        self.get_intermediate_data()
        return
    
    def get_intermediate_data(self):
        paper_authoraffi_set = ddict(list)
        need_paper_set = get_need_papers(self.data)
        for (paperid, authorid, name, affi) in self.data.paperauthor_tuples:
            if paperid in need_paper_set:
                paper_authoraffi_set[paperid].append((authorid, affi))
        self.paper_authoraffi_set = paper_authoraffi_set
#self.paper_authorlist = get_paper_authorlist(self.data, get_need_papers(self.data))


    def get_feature(self, authorid, paperid):
        paper_authoraffi_set = self.paper_authoraffi_set
        cur_affi_set = set()
        if paperid not in paper_authoraffi_set:
            return [-1]
        if authorid in self.data.author_info_dict:
            cur_affi_set.add(self.data.author_info_dict[authorid]['affi'])

        for (coauthor, co_affi) in paper_authoraffi_set[paperid]:
            if coauthor == authorid:
                cur_affi_set.add(co_affi)

#if authorid in self.data.author_info_dict:
#            cur_affi = self.data.author_info_dict[authorid]['affi']

        cnt = 0
        for (co_author, co_affi) in paper_authoraffi_set[paperid]:
            if co_author != authorid and co_affi in cur_affi_set:# and co_affi != '':
                cnt += 1
        return [cnt]
                

#        fea1_value = 0
#        cur_affi = None
#        if authorid in self.data.author_info_dict:
#            cur_affi = self.data.author_info_dict[authorid]['affi']
#        for co_author in self.paper_authorlist[paperid]:
#            if co_author != authorid:
#                if co_author in self.data.author_info_dict:
#                    if self.data.author_info_dict[co_author]['affi'] == cur_affi and cur_affi != '':
#                        fea1_value += 1
#        return [fea1_value]
#                        
#
#         
