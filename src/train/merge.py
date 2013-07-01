
import sys
import csv
from collections import defaultdict as ddict


def run_main(valid_csv, valid_gt_csv):
    csv_reader = csv.reader(file(valid_csv))
    csv_reader.next()
    author_papercnt = ddict(lambda :ddict(int))
    for cols in csv_reader:
        authorid = int(cols[0])
        for paperid in map(int, cols[1].split()):
            author_papercnt[authorid][paperid] += 1

    csv_reader = csv.reader(file(valid_gt_csv))
    csv_reader.next()

    print 'Authorids,ConfirmedPapers,DeletedPapers'
    for cols in csv_reader:
        authorid = int(cols[0])
        confirmedpapers = list()
        for paperid in map(int, cols[1].split()):
            confirmedpapers.append(paperid)
            author_papercnt[authorid][paperid] -= 1

        deletedpapers = list()
        for paperid, cnt in author_papercnt[authorid].items():
            if cnt < 0:
                print >> sys.stderr, 'error'
            if cnt > 0:
                for i in range(cnt):
                    deletedpapers.append(paperid)

        print '%d,%s,%s' % (authorid, ' '.join(map(str,confirmedpapers)), ' '.join(map(str,deletedpapers)))




    

run_main(sys.argv[1], sys.argv[2])
