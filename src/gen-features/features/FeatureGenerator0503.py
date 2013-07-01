# --encoding: utf-8 -

from Data import *
from mylogger import *


'''
Description: The feature Generator of 2013.05.03
feature1: trick1
feature2: author �� this paper��������������������ĸ���
feature3: ���߷�����journal�����ĸ���
feature4: ���߷�����conference�����ĸ���
feature5: <authorid jid>����/authorid journal�ĸ���
feature6: <authorid cid>����/authorid conference�ĸ���
'''

class FeatureGenerator0503:
    def __init__(self, data):
        self.data = data
        self.logger = MyLogger()
        self.generate_intermediate_data()

    '''
    Description: Generate the Intermedia feature data 
    Parameter: None
    Return: None
    '''
    def generate_intermediate_data(self):
        authorid_year_num = ddict(lambda : ddict(int))
        authorid_cid_num = ddict(lambda : ddict(int))
        authorid_jid_num = ddict(lambda : ddict(int))
        authorid_conference_sum = ddict(int)
        authorid_journal_sum = ddict(int)
        authorid_paperid_sum = dict()
 
        cal_authorid_set = set()
        for authorid, paperid, rate in self.data.train_tuples + self.data.valid_tuples:
            authorid_paperid_sum[(authorid, paperid)] = 0
            cal_authorid_set.add(authorid)

        for paperid, authorid, name, affi in self.data.paperauthor_tuples:
            paperid = int(paperid)
            authorid = int(authorid)
            if (authorid, paperid) in authorid_paperid_sum:
                authorid_paperid_sum[(authorid, paperid)] += 1

            if authorid in cal_authorid_set:
                if paperid in self.data.paper_info_dict: 
                    year = self.data.paper_info_dict[paperid]['year']
                    if year != 0:
                        authorid_year_num[authorid][year] += 1
                    cid = self.data.paper_info_dict[paperid]['conferenceid']
                    if cid != 0:
                        authorid_cid_num[authorid][cid] += 1
                        authorid_conference_sum[authorid] += 1
                    jid = self.data.paper_info_dict[paperid]['journalid']
                    if jid != 0:
                        authorid_jid_num[authorid][jid] += 1
                        authorid_journal_sum[authorid] += 1 

        self.authorid_year_num = authorid_year_num
        self.authorid_cid_num = authorid_cid_num
        self.authorid_jid_num = authorid_jid_num
        self.authorid_conference_sum = authorid_conference_sum
        self.authorid_journal_sum = authorid_journal_sum
        self.authorid_paperid_sum = authorid_paperid_sum

    def get_feature(self, authorid, paperid):
        year_sum = 0
        aid_cid_sum = 0
        aid_jid_sum = 0
        conference_sum = self.authorid_conference_sum[authorid]
        journal_sum = self.authorid_journal_sum[authorid]
        if paperid in self.data.paper_info_dict:
            yearid = self.data.paper_info_dict[paperid]['year']
            year_sum = self.authorid_year_num[authorid][yearid]
            
            cid = self.data.paper_info_dict[paperid]['conferenceid']
            
            if cid != 0:
                aid_cid_sum = self.authorid_cid_num[authorid][cid]
            jid = self.data.paper_info_dict[paperid]['journalid']

            if jid != 0:
                aid_jid_sum = self.authorid_jid_num[authorid][jid]
            
            aid_cid_conference_ratio = 0
            if conference_sum > 0:
                aid_cid_conference_ratio = float(aid_cid_sum)/conference_sum
            aid_jid_journal_ratio = 0
            if journal_sum > 0:
                aid_jid_journal_ratio = float(aid_jid_sum)/journal_sum  


        return [self.authorid_paperid_sum[(authorid, paperid)], year_sum, conference_sum, journal_sum, aid_cid_conference_ratio, aid_jid_journal_ratio]

