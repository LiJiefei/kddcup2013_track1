# --encoding: gbk -
'''

1) add bug lcs, mean([coauthor and author name lcs, coauthor and author affi lcs])

'''

from collections import defaultdict as ddict
import re
from myutil import *

def get_bug_lcs_simi(name1, name2):
    str1 = re.sub(r'\s', '', name1.lower())
    str2 = re.sub(r'\s', '', name2.lower())
    if len(str1)==0 or len(str2)==0:
        return 0
    r1 = range(len(str1))
    r2 = range(len(str2))
    dp=[[0 for y in r2] for x in r1]
    dp[0][0] = 1 if str1[0]==str2[0] else 0
    for x in r1:
        dp[x][0] = dp[x-1][0] if str1[x] != str2[0] else 1
    for y in r2:
        dp[0][y] = dp[0][y-1] if str1[0] != str2[y] else 1
    for x in r1:
        for y in r2:
            dp[x][y] = dp[x-1][y-1] + 1 if str1[x]==str2[y] else max(dp[x-1][y], dp[x][y-1])
    return float(dp[-1][-1])/min(len(str1), len(str2))

    

class FeatureGenerator0527:
    def __init__(self, data):
        self.data = data
        need_papers = get_need_papers(self.data)
        paper_author_list = ddict(lambda :ddict(list))
        for (paper, author, name, affi) in self.data.paperauthor_tuples:
            if paper in need_papers:
                paper_author_list[paper][author].append((name, affi))
        self.paper_author_list = paper_author_list
        return

    def get_feature(self, authorid, paperid):
        author_list = self.paper_author_list[paperid]
        min_name_lcs = 100000
        max_name_lcs = -1
        mean_name_lcs = 0
        min_affi_lcs = 100000
        max_affi_lcs = -1
        mean_affi_lcs = 0
        
        co_author_num = 0
        for (name, affi) in author_list[authorid]:
            co_author_num = 0
            name_lcs = 0
            affi_lcs = 0
            cnt = 0
            for co_author, name_affi_list in author_list.items():
                if co_author == authorid:
                    continue
                co_author_num += 1
                for (co_name, co_affi) in name_affi_list:
                    name_lcs += get_bug_lcs_simi(co_name, name)
                    affi_lcs += get_bug_lcs_simi(co_affi, affi)
                    cnt += 1
            if cnt > 0:
                name_lcs /= cnt
                affi_lcs /= cnt
                min_name_lcs = min(min_name_lcs, name_lcs)
                max_name_lcs = max(max_name_lcs, name_lcs)
                mean_name_lcs += name_lcs
                min_affi_lcs = min(min_affi_lcs, affi_lcs)
                max_affi_lcs = max(max_affi_lcs, affi_lcs)
                mean_affi_lcs += affi_lcs
        
        if co_author_num == 0:
            return [-1] * 6

        mean_name_lcs /= len(author_list[authorid])
        mean_affi_lcs /= len(author_list[authorid])
        return [min_name_lcs, max_name_lcs, mean_name_lcs, min_affi_lcs, max_affi_lcs, mean_affi_lcs]

