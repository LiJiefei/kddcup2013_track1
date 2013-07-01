# --encoding: gbk -

'''

1) Í¬id£¬Í¬Ãû×Ö£¬³öÏÖÁ½´Î£¬µ«ÊÇÁ½¸öµÄ×éÖ¯¶¼²»Îª¿Õ¶øÇÒ²»Ò»Ñù
2) pµÄËùÓÐcoauthorºÍaÓÐÏàÍ¬Ãû×Ö£¨ÍêÈ«Ò»Ñù or ÐÕÊÏÒ»Ñù£¬ÆäËûÊ××ÖÄ¸Ò»Ñù, or (³¤¶È²»Ò»ÑùµÄ»°£¬³¤µÄ°üº¬¶ÌµÄ), °üÀ¨ÄæÐòÒ»Ñù£¬ÈçChen Liu  ºÍ Liu Chen£©µÄ¸öÊý
3) aµÄËùÓÐÃû×Ö³öÏÖÔÚÆäËûpaperÃû×ÖµÄ×îÐ¡´ÎÊý
4) aÊÇ·ñ´æÔÚÃû×Ö£¨³ýÈ¥author.csvÖÐµÄÃû×Ö£©ÊÇ A. B. ÐÕÊÏ or  A.ÐÕÊÏ
5) coauthor´æÔÚÃû×Ö A. B. ÐÕÊÏ or A.ÐÕÊÏ µÄ¸öÊý 
6) author.csvÊÇ·ñÊÇÃû×ÖA. B. ÐÕÊÏ or A.ÐÕÊÏ
7) coauthorºÍauthor.csvµÄÃû×ÖµÄpattern(A.ÐÕÊÏ¡¢A. B. ÐÕÊÏ¡¢abc bcd ÐÕÊÏ¡¢ abcÐÕÊÏ)µÄmatch¸öÊý
8) coauthorÊÇ·ñ´æÔÚid²»Í¬£¬µ«ÊÇÃû×ÖÏàÍ¬£¨ÍêÈ«Ò»Ñù or ÐÕÊÏÒ»Ñù£¬ÆäËûÊ××ÖÄ¸Ò»Ñù or (³¤¶È²»Ò»ÑùµÄ»°£¬³¤µÄ°üº¬¶ÌµÄ)£¬ °üÀ¨ÄæÐòÒ»Ñù£¬ÈçChen Liu ºÍ Liu Chen¡£¡££©
9) aÖÐÃû×ÖÊÇ·ñÏàËÆ£¨Èç¹û´æÔÚÒ»¸öÃû×ÖºÍµ±Ç°µÄÃû×ÖºÁÎÞÏàËÆ¶È¡£¡££©

'''


from myutil import *
from collections import defaultdict as ddict

def is_same_name(name1, name2):
    name1 = name1.lower()
    name2 = name2.lower()
    if name1 == name2:
        return True
    name1_cols = name1.split()
    name2_cols = name2.split()
    if len(name1_cols) == 0 or len(name2_cols) == 0:
        return False
    name2_cols_reverse = [ x for x in name2_cols]
    name2_cols_reverse.reverse()
    if ' '.join(name1_cols) == ' '.join(name2_cols_reverse):
        return True
    if name1_cols[-1] != name2_cols[-1]:
        return False
    name1_set = set([ x[0] for x in name1_cols[0:-1]])
    name2_set = set([ x[0] for x in name2_cols[0:-1]])
    return len(name1_set & name2_set) == len(name1_set) or len(name1_set & name2_set) == len(name2_set)


class FeatureGenerator0526:
    def __init__(self, data):
        self.data = data
        need_papers = get_need_papers(self.data)
        need_authors = get_need_authors(self.data)
        paper_authorlist = ddict(lambda: ddict(list))
        author_paperlist = ddict(list)
        for (paper, author, name, affi) in data.paperauthor_tuples:
            if paper in need_papers:
                paper_authorlist[paper][author].append((name, affi))
            if author in need_authors:
                author_paperlist[author].append((paper, name, affi))

        self.paper_authorlist = paper_authorlist     
        self.author_paperlist = author_paperlist
        return

    def get_feature(self, authorid, paperid):
        fea1 = 0
        authorlist = self.paper_authorlist[paperid]
        paperlist = self.author_paperlist[authorid]

        cur_author_name = set([ x[0] for x in authorlist[authorid]])
        if len(authorlist[authorid]) == 2:
            name1,affi1 = authorlist[authorid][0]
            name2,affi2 = authorlist[authorid][1]
            if name1 == name2 and affi1 != affi2:
                fea1 = 1

        coauthor_samename_count = 0
        for coauthor, name_affi_list in self.paper_authorlist[paperid].items():
            add_flag = False
            if coauthor != authorid:
                for (co_name, co_affi) in name_affi_list:
                    for author_name in cur_author_name:
                        if is_same_name(author_name, co_name):
                            add_flag = True
                            break
                    if add_flag:
                        break
                if add_flag:
                    coauthor_samename_count += 1
        cur_author_name_count = ddict(int)
        for (co_paper, name, affi) in paperlist:
            if co_paper != paperid:
                if name in cur_author_name:
                    cur_author_name_count[name] += 1
        if len(cur_author_name_count) == 0:
            min_name_count = -1
        else:
            min_name_count = min(cur_author_name_count.values())
        
        
        fea4 = 0
        author_csv_name = ''
        if authorid in self.data.author_info_dict:
            author_csv_name = self.data.author_info_dict[authorid]['name']
            for name in cur_author_name:
                if name != author_csv_name:
                    if get_name_patternid(name) == 1 or get_name_patternid(name) == 2:
                        fea4 = 1
                        break
        else:
            fea4 = -1
        
        fea5 = 0
        author_csv_name_patternid = get_name_patternid(author_csv_name)
        fea6 = int(author_csv_name_patternid == 1 or author_csv_name_patternid == 2)
        
        if author_csv_name_patternid == 0:
            fea7 = -1
        else:
            fea7 = 0
        fea8 = 0
        for coauthor, name_affi_list in self.paper_authorlist[paperid].items():
            if coauthor != authorid:
                flag5 = False
                flag7 = False
                
                for (co_name, co_affi) in name_affi_list:
                    name_patternid = get_name_patternid(co_name)
                    if name_patternid == 1 or name_patternid == 2:
                        flag5 = True
                    if author_csv_name_patternid != 0 and name_patternid == author_csv_name_patternid:
                        flag7 = True
                    for name in cur_author_name:
                        if is_same_name(co_name, name):
                            fea8 = 1
                if flag5:
                    fea5 += 1
                if flag7:
                    fea7 += 1
        fea9 = 0
        for name in cur_author_name:
            for name2 in cur_author_name:
                if name != name2:
                    if len(set(name.split()) & set(name2.split())) == 0:
                        fea9 = 1
                        break
                if fea9 == 1:
                    break
        return [ fea1, coauthor_samename_count, min_name_count, fea4, fea5, fea6, fea7, fea8, fea9]


