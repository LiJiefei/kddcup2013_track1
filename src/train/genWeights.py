#! /usr/bin/python2

import sys
import csv
import argparse

def parseArgs():
    parser = argparse.ArgumentParser(description='''\
    example: ./genWeights.py < train.csv > train.w''',
                                     formatter_class=argparse.RawTextHelpFormatter)
    return parser.parse_args()

if __name__ == "__main__":
    args = parseArgs()
    csvReader = csv.reader(sys.stdin)
    csvReader.next();
    for line in csvReader:
        assert len(line) == 3
        line[1] = line[1].split()
        line[2] = line[2].split()
        papers = map(int, line[1] + line[2])
        for i, paperId in enumerate(papers):
            if paperId not in papers[:i]:
                print 1.0 / len(line[1])
            else:
                print "0.000000000000000000000000001"
