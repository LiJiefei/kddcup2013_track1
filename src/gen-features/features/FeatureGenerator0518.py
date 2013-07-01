'''

1) add the feature of weige + 0517, (0.00007+)

'''

from Levenshtein import *
from collections import defaultdict as ddict


def lcsubstr_len(S1, S2):
    M = [[0]*(1+len(S2)) for i in xrange(1+len(S1))]
    longest, x_longest = 0, 0
    for x in xrange(1,1+len(S1)):
        for y in xrange(1,1+len(S2)):
            if S1[x-1] == S2[y-1]:
                M[x][y] = M[x-1][y-1] + 1
                if M[x][y]>longest:
                    longest = M[x][y]
                    x_longest  = x
            else:
                M[x][y] = 0
    return len(S1[x_longest-longest: x_longest])


def lcseq_len(a, b):
    m = len(a)
    n = len(b)
    c = ddict(lambda:ddict(lambda:0))
    for i in range(1, m+1):
        for j in range(1, n+1):
            if a[i-1] == b[j-1]:
                c[i][j] = c[i-1][j-1] + 1
            elif c[i-1][j] >= c[i][j-1]:
                c[i][j] = c[i-1][j]
            else:
                c[i][j] = c[i][j-1]
    return c[m][n]

class FeatureGenerator0518:
    def __init__(self, data):
        self.data = data
        pid_uid_name = ddict(lambda:ddict(lambda:""))
        pid_uid_affi = ddict(lambda:ddict(lambda:""))
        for (pid, uid, name, affi) in data.paperauthor_tuples:
            pid_uid_name[pid][uid] = name
            pid_uid_affi[pid][uid] = affi
        self.pid_uid_name = pid_uid_name
        self.pid_uid_affi = pid_uid_affi
        return

    def get_feature(self, authorid, paperid):
        global lcsubstr_len, lcseq_len
        pid_uid_name = self.pid_uid_name
        pid_uid_affi = self.pid_uid_affi
        uid = authorid
        pid = paperid
        if uid in self.data.author_info_dict:
            uid_name_1 = self.data.author_info_dict[uid]['name']
            uid_affi_1 = self.data.author_info_dict[uid]['affi']
        else:
            uid_name_1 = ''
            uid_affi_1 = ''

        uid_name_2 = self.pid_uid_name[pid][uid]
        uid_affi_2 = self.pid_uid_affi[pid][uid]
        len_lcseq_name = lcseq_len(uid_name_1, uid_name_2)
        len_lcseq_affi = lcseq_len(uid_affi_1, uid_affi_2)
        len_lcsub_name = lcsubstr_len(uid_name_1, uid_name_2)
        len_lcsub_affi = lcsubstr_len(uid_affi_1, uid_affi_2)

        uid_name_1_len = len(uid_name_1)
        uid_name_2_len = len(uid_name_2)
        name_sim  = -1
        name_dist = -1
        name_list_len = 1
        sim_lcseq_name = 0 
        sim_lcsub_name = 0
        name_sum_sim = 0
        name_sum_dist = 0
        name_sum_lcseq = 0
        name_sum_lcsub = 0
         
        if uid_name_1_len != 0 and uid_name_2_len != 0:
            name_sim = ratio(uid_name_1, uid_name_2)
            name_dist = distance(uid_name_1, uid_name_2)

            uid_name_len = min(uid_name_1_len, uid_name_2_len)
            sim_lcseq_name = float(len_lcseq_name) / uid_name_len
            sim_lcsub_name = float(len_lcsub_name) / uid_name_len

            for key,value in pid_uid_name[pid].items():
                name_sum_sim += ratio(uid_name_1, value)       
            for key,value in pid_uid_name[pid].items():
                name_sum_dist += distance(uid_name_1, value)       
            for key,value in pid_uid_name[pid].items():
                name_sum_lcseq += lcseq_len(uid_name_1, value)       
            for key,value in pid_uid_name[pid].items():
                name_sum_lcsub += lcsubstr_len(uid_name_1, value)       

        affi_sum_sim = 0
        affi_sum_dist = 0
        affi_sum_lcseq = 0
        affi_sum_lcsub = 0
        affi_list_len = len(pid_uid_affi[pid].items())
        affi_sim = -1
        affi_dist = -1
        sim_lcseq_affi = 0
        sim_lcsub_affi = 0
        if len(uid_affi_1) != 0 and len(uid_affi_2) != 0:
            affi_sim = ratio(uid_affi_1, uid_affi_2)
            affi_dist = distance(uid_affi_1, uid_affi_2)

            uid_affi_len = min(len(uid_affi_1), len(uid_affi_2))
            sim_lcseq_affi = float(len_lcseq_affi) / uid_affi_len
            sim_lcsub_affi = float(len_lcsub_affi) / uid_affi_len

            for key,value in pid_uid_affi[pid].items():
                affi_sum_sim += ratio(uid_affi_1, value)       
            for key,value in pid_uid_affi[pid].items():
                affi_sum_dist += distance(uid_affi_1, value)       
            for key,value in pid_uid_affi[pid].items():
                affi_sum_lcseq += lcseq_len(uid_affi_1, value)       
            for key,value in pid_uid_affi[pid].items():
                affi_sum_lcsub += lcsubstr_len(uid_affi_1, value)       

        return [name_sim, affi_sim, name_dist, affi_dist, len_lcseq_name, len_lcsub_affi, len_lcsub_name, len_lcsub_affi, sim_lcseq_name, sim_lcseq_affi, sim_lcsub_name, sim_lcsub_affi, float(name_sum_sim) / name_list_len, float(name_sum_dist) / name_list_len, float(name_sum_lcseq) / name_list_len, float(name_sum_lcsub) / name_list_len, float(affi_sum_sim) / affi_list_len, float(affi_sum_dist) / affi_list_len, float(affi_sum_lcseq) / affi_list_len, float(affi_sum_lcsub) / affi_list_len]

