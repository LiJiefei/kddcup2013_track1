

from Data import *
from mylogger import *

class BaselineFeatureGenerator2:
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
        author_conferenceid_num = ddict(lambda :ddict(int))
        author_journalid_num = ddict(lambda : ddict(int))
        author_numpaper = ddict(int)
        paper_authorset = ddict(set)
        author_paper_coauthor_sum = ddict(int)


        for paperid, authorid, name, affi in self.data.paperauthor_tuples:
            if paperid in self.data.paper_info_dict:
                cid = self.data.paper_info_dict[paperid]['conferenceid']
                jid = self.data.paper_info_dict[paperid]['journalid']
                if cid > 0:
                    author_conferenceid_num[authorid][cid] += 1
                if jid > 0:
                    author_journalid_num[authorid][jid] += 1
            author_numpaper[authorid] += 1
            paper_authorset[paperid].add(authorid)

        self.logger.debug('getting the author coauthor sum papers....')
    
        author_coauthor_sumpapers = ddict(int)
        author_paper_pair_set = set()
        tmp_author_set = set()
        for (author,paperid,label) in self.data.train_tuples + self.data.valid_tuples:
            coauthors = paper_authorset[paperid]
            author_paper_pair_set.add((author, paperid))
            for coauthor in coauthors:
                if author != coauthor:
                    author_coauthor_sumpapers[tuple(sorted([author, coauthor]))] = 0
                tmp_author_set.add(coauthor)
        self.logger.debug('counting the author coauthor sum papers...') 

        cnt = 0
        for paper, authorset in paper_authorset.items():
            cnt += 1
            if cnt % 1000 == 0:
                self.logger.debug('count %d/%d done.' % (cnt, len(paper_authorset)))
            sorted_authorset = sorted(list(authorset))
            sorted_authorset = [author for author in sorted_authorset if author in tmp_author_set]
            l = len(sorted_authorset)
            for i in range(0, l-1):
                for j in range(i+1, l):
                    k = (sorted_authorset[i], sorted_authorset[j])
                    if k in author_coauthor_sumpapers:
                        author_coauthor_sumpapers[k] += 1

        self.logger.debug('for paper_authorset iteration end.')
        for (author, paper) in author_paper_pair_set:
            for coauthor in paper_authorset[paper]:
                if author != coauthor:
                    k = tuple(sorted([author, coauthor]))
                    author_paper_coauthor_sum[(author, paper)] += author_coauthor_sumpapers[k]
        del author_coauthor_sumpapers

        self.author_conferenceid_num = author_conferenceid_num
        self.author_journalid_num = author_journalid_num
        self.author_numpaper = author_numpaper
        self.paper_authorset = paper_authorset
        self.author_paper_coauthor_sum = author_paper_coauthor_sum

    '''
    Description: Generate the baseline features of pair (authorid, paperid)
    Parameter: authorid, paperid, data
    Return: list of featurs of (authorid, paperid)
    Features: 
    1) number of papers of author in the journal of paperid
    2) number of papers of author in the conference of paperid
    3) number of papers of author
    4) number of authors of paper
    5) number of papers between author and coauthors in this paper
    6) 5)/4)
    '''
    def get_feature(self, authorid, paperid):
        jid_nums = 0
        cid_nums = 0
        if paperid in self.data.paper_info_dict:
            jid = self.data.paper_info_dict[paperid]['journalid']
            cid = self.data.paper_info_dict[paperid]['conferenceid']
        else:
            jid = -1
            cid = -1
        if jid != -1:
            jid_nums = self.author_journalid_num[authorid][jid]
            cid_nums = self.author_conferenceid_num[authorid][cid]
        try: 
            author_num_papers = self.author_numpaper[authorid]
        except:
            author_num_papers = 0
        try:
            paper_num_authors = len(self.paper_authorset[paperid])
        except:
            paper_num_authors = 0
        try:
            author_coauthor_num_papers = self.author_paper_coauthor_sum[(authorid, paperid)]
        except:
            author_coauthor_num_papers = 0

        try:
            ratio_6 = float(author_coauthor_num_papers)/paper_num_authors
        except:
            ratio_6 = 0
        return [jid_nums, cid_nums, author_num_papers, paper_num_authors, author_coauthor_num_papers, ratio_6]
    
    
