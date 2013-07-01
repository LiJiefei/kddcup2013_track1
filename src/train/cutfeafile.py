

from collections import defaultdict as ddict
import csv
import argparse

def parser_feature_select_str(st):
    cols = st.split('_')
    feature_list = list()
    for sub_str in cols:
        sub_begin_end = sub_str.split('-')
        if len(sub_begin_end) == 1:
            feature_list.append(int(sub_begin_end[0]) - 1 )
        elif len(sub_begin_end) == 2:
            if sub_begin_end[1] != 'end':
                feature_list.append((int(sub_begin_end[0]) - 1, int(sub_begin_end[1]) - 1))
            else:
                feature_list.append((int(sub_begin_end[0]) - 1, 'end'))
    return feature_list

def run_main(ins_file, feature_select_str, out_ins_file):
    y = []
    x = []
    select_feature_list = None
    if feature_select_str:
        select_feature_list = parser_feature_select_str(feature_select_str)

    for line in file(ins_file):
        cols = line.strip().split()
        y.append(int(cols[0]))
        fea_values = cols[1].split(',')
        if select_feature_list:
            fea_value_list = list()
            for fea in select_feature_list:
                if type(fea) == int:
                    fea_value_list.append(fea_values[fea])
                else:
                    if fea[1] == 'end':
                        fea_value_list += fea_values[fea[0]:]
                    else:
                        fea_value_list += fea_values[fea[0]:fea[1]+1]
            x.append(fea_value_list)
        else:
            x.append(fea_values)

    with open(out_ins_file, 'w') as fw:
        for ins in x:
            print >> fw, ' '.join(ins)

if __name__=='__main__':
    parser = argparse.ArgumentParser(description='train the gbdt model')
    parser.add_argument('--feature_file', dest='feature_file', required=True, help='the path of feature file')
    parser.add_argument('--feature_select_str', dest='feature_select_str', required=True, help='the feature cut str, for example, 1-28,30-end')
    parser.add_argument('--output', dest='output', required=True, help='the output file')
    args = parser.parse_args()

    run_main(args.feature_file, args.feature_select_str, args.output)
