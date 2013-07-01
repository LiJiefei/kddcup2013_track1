
import sys
import pickle
from mylogger import *
import argparse
from MainFeatureGenerator import *
import features

'''
Description: generate the features from tuples of (autorid, paperid, label) to the file outfile
Parameter: \
           tuples: instance_tuples; \
           feature_generators: the list of feature_generator; \
           outfile: the output feature file; \
           old_feature_file: the feature file of last time
Return: None
'''
def run(instance_tuples, feature_generator, outfile, old_feature_file=None):
    fw = open(outfile, 'w')
    fp = None
    if old_feature_file:
        fp = open(old_feature_file, 'r')
    cnt = 0
    for (authorid, paperid, label) in instance_tuples:
        fea_list = feature_generator.get_feature(authorid, paperid)
        if fp:
            last_fea_list = fp.readline().strip()
            print >> fw, '%s,%s' % (last_fea_list, ','.join([str(x) for x in fea_list]))
        else:
            print >> fw, '%d\t%s' % (label, ','.join([str(x) for x in fea_list]))
    fw.close()
    if fp:
        fp.close()

def main(train_csv, valid_csv, info_path, train_outfile, valid_outfile, train_old_feature_file, valid_old_feature_file, generators_list_file):
    mylogger = MyLogger()
    mylogger.info('loading the datas...')
    data = Data(train_csv, valid_csv, info_path)
    main_feature_generator = MainFeatureGenerator(data, generators_list_file)
    mylogger.info('generate the feature file of train...')
    run(data.train_tuples, main_feature_generator, train_outfile, train_old_feature_file)
    mylogger.info('generate the feature file of valid...')
    run(data.valid_tuples, main_feature_generator, valid_outfile, valid_old_feature_file)
    return 0

def parser_json(setting_json):
    import json
    keys = json.loads(open(setting_json).read())
    return keys['train_csv'], keys['valid_csv'], keys['data_dir'], keys['train_feature_file'], keys['valid_feature_file']

if __name__=='__main__':
    parser = argparse.ArgumentParser(description='Generate the feature files.')

    parser.add_argument('--setting', dest='setting_json', required=True, help='the path of SETTING.json')
    args = parser.parse_args() 
    train_csv, valid_csv, info_path, train_outfile, valid_outfile = parser_json(args.setting_json)
    
    old_train=None
    old_valid=None
    generators_list_file='src/gen-features/generators.list'
    
    main(train_csv, valid_csv, info_path, train_outfile, valid_outfile, old_train, old_valid, generators_list_file)
