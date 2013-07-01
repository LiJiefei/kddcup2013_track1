# --encoding: gbk -

'''

1) ×÷Õß·¢±í¹ýµÄpaperµÄkeywords Óë µ±Ç°paperµÄkeywordµÄmax,min,mean,stdev,sum
2) ×÷Õß·¢±í¹ýµÄpaperµÄtitle Óë µ±Ç°paperµÄtitleµÄmax,min,mean,stdev,sum
#3) ×÷Õß·¢±í¹ýµÄpaperµÄkeywords & title Óë µ±Ç°paperµÄkeyword & titleµÄmax,min,mean,stdev,sum
3) ×÷Õß·¢±í¹ýµÄpaperµÄ»áÒéµÄÃû³ÆµÄËõÐ´Óëµ±Ç°paperµÄ»áÒéµÄÃû³ÆµÄËõÐ´µÄmax,min,mean,stdev,sum
4) ×÷Õß·¢±í¹ýµÄpaperµÄ»áÒéµÄÃû³ÆµÄÈ«³ÆÓëµ±Ç°paperµÄ»áÒéµÄÃû³ÆµÄËõÐ´µÄmax,min,mean,stdev,sum

'''

from collections import defaultdict as ddict
from myutil import *

import Levenshtein
import math

def keywordSimi(k1, k2):
    k1_words = split_keywords(k1.lower())
    k2_words = split_keywords(k2.lower())
    return Levenshtein.setratio(k1_words, k2_words)

def titleSimi(t1, t2):
    t1_words = t1.lower().split()
    t2_words = t2.lower().split()
    return Levenshtein.setratio(t1_words, t2_words)

def long_seq(s1, s2):
    ans = -1
    dp = dict()
    for i in range(len(s1)):
        dp[(i,-1)] = 0 
    for j in range(len(s2)):
        dp[(-1,j)] = 0 
    dp[(-1,-1)] = 0 
    for i in range(len(s1)):
        for j in range(len(s2)):
            if s1[i] == s2[j]:
                dp[(i,j)] = dp[(i-1,j-1)] + 1 
                ans = max(dp[(i,j)], ans)
            else:
                dp[(i,j)] = 0 
    return ans 

def shortnameSimi(sname1, sname2):
    if sname1 == '' or sname2 == '':
        return 0.0
    cut_name1 = ''
    if len(sname1) >= 4:
        cut_name1 = sname1[2:]
    else:
        cut_name1 = sname1
    cut_name2 = ''
    if len(sname2) >= 4:
        cut_name2 = sname2[2:]
    else:
        cut_name2 = sname2
    return long_seq(cut_name1, cut_name2)/float(min(len(cut_name1), len(cut_name2)))

def longnameSimi(lname1, lname2):
    if lname1 == '' or lname2 == '':
        return 0.0
    cut_name1 = lname1[lname1.find('on ') + 3:].split()
    cut_name2 = lname2[lname2.find('on ') + 3:].split()
    return Levenshtein.setratio(cut_name1, cut_name2)

def cal_max_min_mean_std_sum(similist):
    if len(similist) == 0:
        return [-1] * 5
    min_simi = 10.0
    max_simi = -1
    mean_simi = 0
    stddev = 0.0
    for simi in similist:
        min_simi = min(simi, min_simi)
        max_simi = max(simi, max_simi)
        mean_simi += simi
    sum_simi = mean_simi
    mean_simi/= len(similist)
    for simi in similist:
        stddev += (simi-mean_simi)**2

    stddev /= len(similist)
    stddev = math.sqrt(stddev)
    return [max_simi, min_simi, mean_simi, stddev, sum_simi]

        

class FeatureGenerator0610:
    def __init__(self, data):
        self.data = data
        need_authors = get_need_authors(data)
        need_papers = get_need_papers(data)
        paper_info_dict = data.paper_info_dict
        author_paperkey_tit_csname_clname = ddict(lambda: ddict())
        paper_key_tit_csname_clname = dict()
        for (paperid, authorid, name, affi) in data.paperauthor_tuples:
            if authorid in need_authors:
                if paperid not in paper_info_dict:
                    continue
                keyword = paper_info_dict[paperid]['keyword']
                title = paper_info_dict[paperid]['title']
                cid = paper_info_dict[paperid]['conferenceid']
                jid = paper_info_dict[paperid]['journalid']
                if cid <= 0 and jid <= 0:
                    csname = ''
                    clname = ''
                else:
                    if cid > 0:
                        if cid in data.cid_info_dict:
                            csname = data.cid_info_dict[cid]['shortname']
                            clname = data.cid_info_dict[cid]['longname']
                        else:
                            csname = ''
                            clname = ''
                    else:
                        if jid in data.jid_info_dict:
                            csname = data.jid_info_dict[jid]['shortname']
                            clname = data.jid_info_dict[jid]['longname']
                        else:
                            csname = ''
                            clname = ''
                
                author_paperkey_tit_csname_clname[authorid][paperid] = (keyword, title, csname, clname)
                if paperid in need_papers:
                    paper_key_tit_csname_clname[paperid] = (keyword, title, csname, clname) 

        self.author_paperkey_tit_csname_clname = author_paperkey_tit_csname_clname
        self.paper_key_tit_csname_clname = paper_key_tit_csname_clname

    def get_feature(self, authorid, paperid):
        if paperid not in self.paper_key_tit_csname_clname or authorid not in self.author_paperkey_tit_csname_clname:
            return [-2] * 25
        key_similist = list()
        tit_similist = list()
        sname_similist = list()
        lname_similist = list()
        cur_key, cur_tit, cur_csname, cur_clname = self.paper_key_tit_csname_clname[paperid]
        for copaper,key_tit_csanme_clname in self.author_paperkey_tit_csname_clname[authorid].items():
            if copaper != paperid:
                co_key, co_tit, co_csname, co_clname = key_tit_csanme_clname
                key_similist.append(keywordSimi(co_key, cur_key))
                tit_similist.append(titleSimi(co_tit, cur_tit))
                sname_similist.append(shortnameSimi(co_csname, cur_csname))
                lname_similist.append(longnameSimi(co_clname, cur_clname))


        return cal_max_min_mean_std_sum(key_similist) + cal_max_min_mean_std_sum(tit_similist) + cal_max_min_mean_std_sum(sname_similist) + cal_max_min_mean_std_sum(lname_similist)


    
