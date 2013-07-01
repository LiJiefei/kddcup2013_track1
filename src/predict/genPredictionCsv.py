#! /usr/bin/python2

import argparse
import csv

def parseArgs():
    parser = argparse.ArgumentParser(description='''\
    example: ./genPredictionCsv.py -p test.y -i test.csv -o submit.csv''',
    formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-p',
                        dest='pred',
                        type=argparse.FileType('r'),
                        help='predict file from rgf',
                        required=True)

    parser.add_argument('-i',
                        dest='csv',
                        type=argparse.FileType('r'),
                        help='csv file',
                        required=True)
         
    parser.add_argument('-o',
                        dest='submit',
                        type=argparse.FileType('w'),
                        help='file for submission',
                        required=True)
    
    return parser.parse_args()

if __name__ == "__main__":
    args = parseArgs()
    predfile = args.pred
    csvReader = csv.reader(args.csv)
    csvReader.next()
    submitfile = args.submit
    submitfile.write('AuthorId,PaperIds\n')
    for cols in csvReader:
        authorId = cols[0]
        rankPaperId = []
        papers = ' '.join(cols[1:]).split()
        for i, paperId in enumerate(papers):
            if paperId not in papers[:i]:
                rankPaperId.append((float(predfile.readline()), paperId))
            else:
                predfile.readline()
                rankPaperId.append((-(10**100), paperId))
        rankPaperId.sort(reverse=True);
        submitfile.write(authorId + ',' +' '.join(zip(*rankPaperId)[1]) + '\n')
    args.pred.close()
    args.csv.close()
    args.submit.close()
