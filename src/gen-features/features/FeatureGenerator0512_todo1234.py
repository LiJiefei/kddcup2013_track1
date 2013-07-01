# --encoding:utf-8 -

from Data import *
from myutil import *
from collections import defaultdict as ddict

'''
1) paperµÄ²»Í¬µÄaffi¸öÊý
2) paperauthorÖÐ³öÏÖµÄÃû×ÖÊÇ·ñºÍauthor.csv match
3) paperautorÖÐ³öÏÖµÄauthoridµÄ×î´óaffi match¸öÊý
4) ³öÏÖ×î´óµÄaffiÊÇ·ñ¶ÔÓ¦author.csvµÄaffi
5) 3)/paperµÄaffi¸öÊý
#### + journalid, conferenceid (0.003+)
'''


class FeatureGenerator0512_todo1234:
    def __init__(self, data):
        self.data = data
        self.get_intermediate_data()

    def get_intermediate_data(self):
        paper_authoraffi_list = dict()
        for (authorid, paperid, label) in self.data.train_tuples + self.data.valid_tuples:
            paper_authoraffi_list[paperid] = list()
        for (paperid, authorid, name, affi) in self.data.paperauthor_tuples:
            if paperid in paper_authoraffi_list:
                paper_authoraffi_list[paperid].append((authorid, name, affi))
        
        need_authorpaper_pair_set = get_need_authorpaper_pair(self.data)
        paper_affi_num = dict()
        authorpaper_fea_dict = dict()
        for paperid, authoraffi_list in paper_authoraffi_list.items():
            paper_affi_num[paperid] = len(set([x[2] for x in authoraffi_list]))
            for authorid, name, affi in authoraffi_list:
                k = (authorid, paperid)
                if authorid in self.data.author_info_dict:
                    author_name = self.data.author_info_dict[authorid]['name']
                    author_affi = self.data.author_info_dict[authorid]['affi']
                else:
                    author_name = ''
                    author_affi = ''
                if k in need_authorpaper_pair_set:
                    curname_list = [x[1] for x in authoraffi_list if x[0] == authorid]
                    namematch_flag = 0
                    for name in curname_list:
                        if name == author_name:
                            namematch_flag = 1
                    affi_cnt = ddict(int)
                    curaffi_set = set()
                    for (author, na, aff) in authoraffi_list:
                        affi_cnt[aff] += 1
                        if author == authorid:
                            curaffi_set.add(aff)
                    max_aff = None
                    max_aff_cnt = -1
                    for aff in curaffi_set:
                        if max_aff_cnt < affi_cnt[aff]:
                            max_aff_cnt = affi_cnt[aff]
                            max_aff = aff
                    if max_aff == author_affi:
                        match_aff_flag = 1
                    else:
                        match_aff_flag = 0

                    authorpaper_fea_dict[k] = (namematch_flag, max_aff_cnt, match_aff_flag, float(max_aff_cnt)/len(authoraffi_list))
            
        self.paper_affi_num = paper_affi_num
        self.authorpaper_fea_dict = authorpaper_fea_dict
        return 

    def get_feature(self, authorid, paperid):
        return [self.paper_affi_num[paperid]] + list(self.authorpaper_fea_dict[(authorid,paperid)]) 
        
