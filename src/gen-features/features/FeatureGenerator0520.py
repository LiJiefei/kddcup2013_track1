# --encoding: gbk -
'''
1) twiceCoauthor µÄpaperµÄ¼¯ºÏºÍauthorµÄpaperµÄ¼¯ºÏµÄ½»¼¯
2) ÕÒ³öaµÄËùÓÐcoauthorÊÇ·ñÓÐaÍêÈ«ÏàÍ¬µÄÃû×Ö£¬boolÀàÐÍÌØÕ÷
3) ÕÒ³öaµÄËùÓÐcoauthorÊÇ·ñÓÐaÏàÍ¬ÐÕÊÏ(×îºóÒ»¸öµ¥´ÊÏàÍ¬)µ«ÊÇ²»Í¬Ãû×Ö£¬boolÀàÐÍÌØÕ÷
#4) coauthorµÄÃû×ÖµÄ¸öÊý


'''

from collections import defaultdict as ddict
from myutil import *

class FeatureGenerator0520:
    def __init__(self, data):
        self.data = data
        need_authors = get_need_authors(self.data)
        need_papers = get_need_papers(self.data)
        paper_author_pacnt = ddict(lambda: ddict(int))
        author_paperset = dict()
        paper_author_name = ddict(lambda: ddict(set))
        for (paperid, authorid, name, affi) in self.data.paperauthor_tuples:
            if paperid in need_papers:
                paper_author_pacnt[paperid][authorid] += 1
                if len(name) > 0:
                    paper_author_name[paperid][authorid].add(name)
        
        
        for paperid,author_pacnt in paper_author_pacnt.items():
            for author, pacnt in author_pacnt.items():
                if author in need_authors or pacnt == 2:
                    author_paperset[author] = set()

        for (paperid, authorid, name, affi) in self.data.paperauthor_tuples:
            if authorid in author_paperset:
                author_paperset[authorid].add(paperid)

        self.author_paperset = author_paperset
        self.paper_author_pacnt = paper_author_pacnt
        self.paper_author_name = paper_author_name
        return

    def get_feature(self, authorid, paperid):
        coauthor_paperset = set()
        coauthor_name_match_flag = False
        coauthor_name_set = set()
        author_name_set = set()
        for coauthor,pacnt in self.paper_author_pacnt[paperid].items():
            if coauthor != authorid and pacnt == 2:
                coauthor_paperset = coauthor_paperset | self.author_paperset[coauthor]
            if coauthor != authorid:
                coauthor_name_set = coauthor_name_set | self.paper_author_name[paperid][coauthor]
            else:
                author_name_set = self.paper_author_name[paperid][authorid]
        fea1 = len(coauthor_paperset & self.author_paperset[authorid])
        coauthor_name_match_flag = len(author_name_set & coauthor_name_set) > 0
        
        coauthor_lastname_match_flag = False
        for name1 in author_name_set:
            for name2 in coauthor_name_set:
                if name1 != name2 and name1.split()[-1] == name2.split()[-1]:
                    coauthor_lastname_match_flag = True
                    break
            if coauthor_lastname_match_flag:
                break

        return [fea1, int(coauthor_name_match_flag), int(coauthor_lastname_match_flag)]

