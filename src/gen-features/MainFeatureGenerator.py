
from features import *

class MainFeatureGenerator:
    def __init__(self, data, conf_file):
        self.feature_generators = list()
        self.read_conf_file(data, conf_file)

    def read_conf_file(self, data, conf_file):
        for line in file(conf_file):
            line = line.strip()

            if len(line) == 0 or line[0] == '#':
                continue
            try:
                tmp = globals()[line]
            except:
                print >> sys.stderr, 'create feature generator %s error!' % (line)
                sys.exit(-1)
            print line
            self.feature_generators.append(tmp(data))

    def get_feature(self, authorid, paperid):
        fea_list = list()
        for feature_generator in self.feature_generators:
            fea_list += feature_generator.get_feature(authorid, paperid)
        return fea_list

