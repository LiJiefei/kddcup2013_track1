# --encoding: utf-8 -
'''
1) �����rankֵ
2) �����rank ֵ
3) �Ƿ�����С��pid
4) �Ƿ�������pid
5) pa�е�����rank
6) pa�еķ���rank
7) �Ƿ���pa����С��pid
8) �Ƿ���pa������pid
'''
from collections import defaultdict as ddict


class FeatureGenerator0604:
    def __init__(self, data):
        self.data = data
        train_authorpaperlist = ddict(list)
        need_authors = set()
        for (authorid, paperid, label) in data.train_tuples:
            train_authorpaperlist[authorid].append(paperid)
            need_authors.add(authorid)
        pa_authorpaperlist = ddict(list)
        for (paperid, authorid, name, affi) in data.paperauthor_tuples:
            if authorid in need_authors:
                pa_authorpaperlist[authorid].append(paperid)

        self.train_authorpaperlist = train_authorpaperlist
        self.pa_authorpaperlist = pa_authorpaperlist


    def get_feature(self, authorid, paperid):
        train_pos_rank = 0
        train_neg_rank = 0
        train_min_flag = 1
        train_max_flag = 1
        pa_pos_rank = 0
        pa_neg_rank = 0
        pa_min_flag = 1
        pa_max_flag = 1
        for paper in self.train_authorpaperlist[authorid]:
            if paper < paperid:
                train_pos_rank += 1
                train_min_flag = 0
            if paper > paperid:
                train_neg_rank += 1
                train_max_flag = 0

        for paper in self.pa_authorpaperlist[authorid]:
            if paper < paperid:
                pa_pos_rank += 1
                pa_min_flag = 0
            if paper > paperid:
                pa_neg_rank += 1
                pa_max_flag = 0
        return [train_pos_rank, train_neg_rank, train_min_flag, train_max_flag, pa_pos_rank, pa_neg_rank, pa_min_flag, pa_max_flag]




