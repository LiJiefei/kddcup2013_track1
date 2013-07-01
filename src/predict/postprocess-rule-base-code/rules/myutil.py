
from Data import *
from collections import defaultdict as ddict
import re

'''
Description: Get the authorid in Train.csv and Valid.csv
Parameter: data, object of class Data;
Return: the set of authorid in the train.csv and valid.csv
'''
def get_need_authors(data):
    need_authors = set()
    for (authorid, paperid, label) in data.train_tuples + data.valid_tuples:
        need_authors.add(authorid)
    return need_authors

'''
Description: Get the paperid in Train.csv and Valid.csv
Parameter: data, object of class Data;
Return: the set of paperid in the train.csv and valid.csv
'''
def get_need_papers(data):
    need_papers = set()
    for (authorid, paperid, label) in data.train_tuples + data.valid_tuples:
        need_papers.add(paperid)
    return need_papers

'''
Description: Get the authorlist for each paper in the need_paper_set
Parameter: data, object of class Data; need_paper_set, the paper needed to be calculated
Return: a dict, {paperid: list of author in this paper}
'''
def get_paper_authorlist(data, need_paper_set):
    paper_authorlist = ddict(set)
    for (paperid, authorid, name, affi) in data.paperauthor_tuples:
        paper_authorlist[paperid].add(authorid)
    return paper_authorlist
        
'''
Description: Get the (author, paper) pair we should calculate
Parameter: data, Object of class Data
Return: the (author, paper) pair set which needed calculated
'''
def get_need_authorpaper_pair(data):
    need_authorpaper_set = set()
    for (authorid, paperid, label) in data.train_tuples + data.valid_tuples:
        need_authorpaper_set.add((authorid, paperid))
    return need_authorpaper_set
    
'''
Description: Split the keywords
Parameter: keyword
Return: the list of keywords
'''
def split_keywords(keyword):
    return [ w for w in re.split(r',|\|| |;', keyword) if w != '']


'''
Description: return the pattern id of name, (a. lastname:1, a. b. lastname: 2, abc lastname: 3, abc efg lastname: 4,  other: 0)
'''

def get_name_patternid(name):
    if re.match('[A-Za-z]\. [a-zA-Z]+', name):
        return 1
    if re.match('[A-Za-z]\. [A-Za-z]\. [a-zA-Z]+', name):
        return 2
    if re.match('[a-zA-Z]+ [a-zA-Z]+', name):
        return 3
    if re.match('[a-zA-Z]+ [a-zA-Z]+ [a-zA-Z]+', name):
        return 4
    return 0

'''

'''
def read_predictions_file(pred_csv):
    csv_reader = csv.reader(file(pred_csv))
    csv_reader.next()
    authorpaper_preds = dict()
    for cols in csv_reader:

        authorid = int(cols[0])
        paperid = int(cols[1])
        preds = map(float, cols[2:])
        authorpaper_preds[(authorid, paperid)] = preds
    return authorpaper_preds 



