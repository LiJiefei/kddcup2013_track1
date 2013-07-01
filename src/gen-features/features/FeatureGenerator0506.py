# --encoding: utf-8 -
import sys

'''
1)paper的年份，离散化？<1600=0 >2013=-1,其他不变 (0.004+)
2) PaperAuthor.csv 和 Author.csv是否match (0.0005+)
'''


class FeatureGenerator0506:
    def __init__(self, data):
        self.data = data
        self.generate_intermediate_data()

    def generate_intermediate_data(self):
        need_pair_set = set()
        authorpaper_affi = dict()
        print '0506...' 
        print 1703937 in self.data.author_info_dict
        for (authorid, paperid, label) in self.data.train_tuples + self.data.valid_tuples:
            need_pair_set.add((authorid, paperid))

        for (paperid, authorid, name, affi) in self.data.paperauthor_tuples:
            if (authorid, paperid) in need_pair_set:
                authorpaper_affi[(authorid, paperid)] = affi
        self.authorpaper_affi = authorpaper_affi


    def get_feature(self, authorid, paperid):
        year = self.data.paper_info_dict[paperid]['year']
        if year < 1600:
            year = 0
        if year > 2013:
            year = -1

        k = (authorid, paperid)
        flag = -1
        if k in self.authorpaper_affi:
            flag = -2
            if authorid in self.data.author_info_dict:
                try:
                    if self.authorpaper_affi[k] != self.data.author_info_dict[authorid]['affi']:
                        flag = 0
                    else:
                        flag = 1
                except:
                    print >> sys.stderr, self.data.author_info_dict[authorid]
                    print >> sys.stderr, 'error!%d' % (authorid)
                    sys.exit(-1)

        return [year, flag]
