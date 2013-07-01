# --encoding: gbk -
'''

1) 统计当前的作者与coauthor名字共同发表过的文章的个数的总和


'''

from myutil import *

class FeatureGenerator0606:
    def __init__(self, data):
        self.data = data
        need_authors = get_need_authors(data)
        paper_author_name = ddict(list)
        
        author_paperset = ddict(set)
        for (paperid, authorid, name, affi) in self.data.paperauthor_tuples:
            paper_author_name[paperid].append((authorid, name))
            if authorid in need_authors:
                author_paperset[authorid].add(paperid)
        
        author_name_cnt = ddict(int)
        for authorid, paperset in author_paperset.items():
            for paper in paperset:
                for (coauthorid, name) in paper_author_name[paper]:
                    if coauthorid != authorid:
                        author_name_cnt[(authorid, name)] = 0

        for (paperid, authorid, name, affi) in self.data.paperauthor_tuples:
            if (authorid, name) in author_name_cnt:
                author_name_cnt[(authorid, name)] += 1

        self.author_name_cnt = author_name_cnt
        self.paper_author_name = paper_author_name


    def get_feature(self, authorid, paperid):
        sum_cnt = 0
        for (coauthor, name) in self.paper_author_name[paperid]:
            sum_cnt += self.author_name_cnt[(authorid, name)]

        return [sum_cnt]
                
