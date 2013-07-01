
import sys
import csv
from collections import defaultdict as ddict

def read_submission(submission_csv, author_paperrank):
    csv_reader = csv.reader(file(submission_csv))
    csv_reader.next()
    
    for cols in csv_reader:
        authorid = int(cols[0])
        papers = map(int, cols[1].split())
        for i in range(len(papers)):
            if papers[i] not in papers[:i]:
                author_paperrank[authorid][papers[i]] += 1.0/(i+1)
            else:
                break

def run_main(submission_dir, submission_list_file, output):
    submissions = [ submission_dir + '/' + x.strip() for x in file(submission_list_file) if len(x.strip()) > 0 and x.strip()[0] != '#' ]
    author_paperrank = ddict(lambda: ddict(float))

    for submission in submissions:
        read_submission(submission, author_paperrank)
    
    with open(output, 'w') as fw:
        print >> fw, 'AuthorId,PaperIds'
        for authorid, paper_score in author_paperrank.items():
            print >> fw, '%d,%s' % (authorid, ' '.join(map(lambda x:str(x[0]), sorted(paper_score.items(), key=lambda x:-x[1]))))


if __name__=='__main__':
    if len(sys.argv) != 4:
        print >> sys.stderr, 'usage: <submission_dir> <submission_list_file> <output>'
    else:
        run_main(sys.argv[1], sys.argv[2], sys.argv[3])
    



