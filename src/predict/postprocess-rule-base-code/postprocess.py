


import argparse
import rules
import csv
from rules import *

class MainPostProcess:
    def __init__(self, data, conf_file):
        self.process = list()
        self.read_conf_file(data, conf_file)

    def read_conf_file(self, data, conf_file):
        for line in file(conf_file):
            line = line.strip()

            if len(line) == 0 or line[0] == '#':
                continue
            try:
                tmp = globals()[line]
            except:
                print >> sys.stderr, 'create rule %s error!' % (line)
                sys.exit(-1)
            self.process.append(tmp(data))

    def postprocess(self, authorid, paperlist):
        predlist = [ x for x in paperlist]
        for post in self.process:
            predlist = post.postprocess(authorid, predlist)

        return predlist
            
    

def run_main(data, mainpostprocess, submission_file, output):
    csv_reader = csv.reader(file(submission_file))
    csv_reader.next()
    fw = open(output,'w')
    print >> fw, 'AuthorId,PaperIds'
    for cols in csv_reader:
        authorid = int(cols[0])
        paperlist = map(int, cols[1].split())
        print >> fw, '%d,%s' % (authorid, ' '.join(map(str, mainpostprocess.postprocess(authorid, paperlist))))
    fw.close()


def parser_json(setting_json):
    import json
    keys = json.loads(open(setting_json).read())
    return keys['train_csv'], keys['valid_csv'], keys['data_dir'], keys['model_path']

if __name__=='__main__':
    parser = argparse.ArgumentParser(description='Use the pa2 rules.')
    parser.add_argument('--setting', dest='setting', required=True, help='the SETTINGS.json')
    parser.add_argument('--submission_list_file', dest='submission_list_file', required=True, help='the submission list ')
    parser.add_argument('--rules_list_file', dest='rules_list_file', required=True, help='the rules list file')
    args = parser.parse_args()

    train_csv, valid_csv, info_path, model_dir = parser_json(args.setting)
    data = Data(train_csv, valid_csv, info_path)
    mainpostprocess = MainPostProcess(data, args.rules_list_file)
    
    submission_list = [ line.strip() for line in file(args.submission_list_file) if len(line.strip()) > 0 and line.strip()[0] != '#']
    for line in submission_list:
        run_main(data, mainpostprocess, model_dir + '/' + line,  model_dir + '/' + line[:-4] + '-rules.csv')


