# --encoding: gbk -
'''
1) twiceCoauthor µÄpaperµÄ¼¯ºÏºÍauthorµÄpaperµÄ¼¯ºÏµÄ½»¼¯
2) ÕÒ³öaµÄËùÓÐcoauthorÊÇ·ñÓÐaÍêÈ«ÏàÍ¬µÄÃû×Ö£¬boolÀàÐÍÌØÕ÷, Ò»ÑùµÄ¶¨Òå²»Í¬0520, ÕâÀïµÄÒ»ÑùÊÇlast nameÒ»Ñù£¬³¤¶ÈÒ»Ñù£¬È»ºólastnameÇ°ÃæµÄ¿ªÍ·×ÖÄ¸Ò»Ñù
3) ÕÒ³öaµÄËùÓÐcoauthorÊÇ·ñÓÐaÏàÍ¬ÐÕÊÏ(×îºóÒ»¸öµ¥´ÊÏàÍ¬)µ«ÊÇ²»Í¬Ãû×Ö£¬boolÀàÐÍÌØÕ÷
#4) coauthorµÄÃû×ÖµÄ¸öÊý


'''

from collections import defaultdict as ddict
from myutil import *

def is_samename(name1, name2):
    name1_lower = name1.lower()
    name2_lower = name2.lower()
    name1_cols = name1_lower.split()
    name2_cols = name2_lower.split()
    if len(name1_cols) != len(name2_cols):
        return False
    else:
        if name1_cols[-1] == name2_cols[-1] and (''.join([ x[0] for x in name1_cols[0:-1]]) == ''.join([x[0] for x in name2_cols[0:-1]])):
            return True
    return False

class FeatureGenerator0520_samename:
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
        global is_samename
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
        
        coauthor_name_match_flag2 = False
        coauthor_lastname_match_flag = False
        coauthor_lastname_match_flag2 = False

        for name1 in author_name_set:
            for name2 in coauthor_name_set:
                if name1 != name2 and name1.split()[-1] == name2.split()[-1]:
                    coauthor_lastname_match_flag = True
                if is_samename(name1, name2):
                    coauthor_name_match_flag2 = True
                else:
                    if name1.split()[-1] == name2.split()[:-1]:
                        coauthor_lastname_match_flag2 = True

            if coauthor_lastname_match_flag and coauthor_name_match_flag2:
                break

        return [fea1, int(coauthor_name_match_flag2), int(coauthor_lastname_match_flag2)] #int(coauthor_name_match_flag2)]

