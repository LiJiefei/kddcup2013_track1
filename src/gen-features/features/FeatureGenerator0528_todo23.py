# --encoding: gbk -
'''

1) add weige feature
2) Í³¼Æ×÷ÕßÔÚµ±Ç°µÄaffiÏÂ·¢±í¹ýµÄpaper
3) Í³¼Æ×÷ÕßÔÚµ±Ç°Äê·ÝÏÂ¸ÃaffiÏÂ·¢±í¹ýµÄpaper


'''

from collections import defaultdict as ddict
from myutil import *

def load_weige_feature(ap_fea_dict, featurefile):
    for line in file(featurefile):
        cols = line.strip().split(',')
        ap_fea_dict[(int(cols[0]), int(cols[1]))] = map(float, cols[2].split(','))

class FeatureGenerator0528_todo23:
    def __init__(self, data):
        self.data = data
#        self.weige_fea_dict = dict()
#        load_weige_feature(self.weige_fea_dict, '%s/weige_data/train.30f.txt' % self.data.info_input)
#        load_weige_feature(self.weige_fea_dict, '%s/weige_data/val.30f.txt' % self.data.info_input)
        author_affi_count = ddict(lambda: ddict(int))
        authoryear_affi_count = ddict(lambda: ddict(int))
        need_authors = get_need_authors(data)
        need_papers = get_need_papers(data)
        paper_authoraffi = ddict(list)
        for (paper, author, name, affi) in data.paperauthor_tuples:
            if paper in need_papers:
                paper_authoraffi[paper].append((author, affi))

            if author in need_authors:
                author_affi_count[author][affi] += 1
                if paper in data.paper_info_dict:
                    year = data.paper_info_dict[paper]['year']
                else:
                    year = -1
                authoryear_affi_count[(author, year)][affi] += 1
        self.author_affi_count = author_affi_count
        self.authoryear_affi_count = authoryear_affi_count
        self.paper_authoraffi = paper_authoraffi
        self.author_sum_affi_count = ddict(int)
        self.authoryear_sum_affi_count = ddict(int)
        for author,affi_cnt in self.author_affi_count.items():
            for affi, cnt in affi_cnt.items():
                self.author_sum_affi_count[author] += cnt
        for author_year, affi_cnt in self.authoryear_affi_count.items():
            for affi, cnt in affi_cnt.items():
                self.authoryear_sum_affi_count[author_year] += cnt

        return

    def get_feature(self, authorid, paperid):
        if paperid not in self.data.paper_info_dict:
            year = -1
        else:
            year = self.data.paper_info_dict[paperid]['year']

        affi_cnt = ddict(int)
        author_affi_set = set()
        for co_author,affi in self.paper_authoraffi[paperid]:
            if co_author != authorid:
                affi_cnt[affi] += 1
            else:
                author_affi_set.add(affi)
        max_affi = ''
        max_affi_cnt = -1
        for affi in author_affi_set:
            if max_affi_cnt < affi_cnt[affi]:
                max_affi_cnt = affi_cnt[affi]
                max_affi = affi
#            return [self.author_affi_count[authorid][max_affi]/self.author_sum_affi_count[authorid], self.authoryear_affi_count[(authorid, year)][max_affi]/self.authoryear_sum_affi_count[(authorid, year)]] 
        return [self.author_affi_count[authorid][max_affi]]



#return self.weige_fea_dict[(authorid, paperid)]

