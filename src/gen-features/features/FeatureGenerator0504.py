# --encoding: utf-8 -

from collections import defaultdict as ddict

'''
Description: add features as list
1) ���paperlist�г��ָ�paper�ĸ���, 0.004+
2) coauthor sumpapers/<paper author num>, 0.00099+, ���feature������BaselineFeatureGenerator��
'''
class FeatureGenerator0504:
    def __init__(self, data):
        self.data = data
        self.get_intermediate_data()
        
    def get_intermediate_data(self):
        author_paper_cocur_nums = ddict(int)
        for (author, paperid, label) in self.data.train_tuples + self.data.valid_tuples:
            author_paper_cocur_nums[(author, paperid)] += 1
        self.author_paper_cocur_nums = author_paper_cocur_nums


    def get_feature(self, authorid, paperid):
        return [ self.author_paper_cocur_nums[(authorid, paperid)] ]

