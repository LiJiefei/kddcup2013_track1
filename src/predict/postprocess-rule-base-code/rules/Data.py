from collections import defaultdict as ddict
import csv

class Data:
    def __init__(self, train_csv, valid_csv, info_input):
        self.info_input = info_input
        self.train_csv = train_csv
        self.valid_csv = valid_csv
        self.paperauthor_csv = info_input + '/PaperAuthor.csv'
        self.author_csv = info_input + '/Author.csv'
        self.paper_csv = info_input + '/Paper.csv'
        self.dading_authorpaper_simi_train_csv = info_input + '/dading_data/similarity.Train.csv'
        self.dading_authorpaper_simi_valid_csv = info_input + '/dading_data/similarity.Valid.csv'
        self.dading_0519_simi_csv = info_input + '/dading_data/0519_similarity/similarity.feature.csv'
        self.dading_0523_simi_csv = info_input + '/dading_data/0523_similarity/similarity.feature.csv'
        self.dading_topic_simi_csv = info_input + '/dading_data/topic_similarity/topic.feature.csv'
        self.Conference_csv = info_input + '/Conference.csv'
        self.Journal_csv = info_input + '/Journal.csv'

        self.train_tuples = self.read_train_csv(self.train_csv)
        self.valid_tuples = self.read_valid_csv(self.valid_csv)
#        self.paper_info_dict = self.read_paper_csv(self.paper_csv)
#        self.author_info_dict = self.read_author_csv(self.author_csv)
        self.paperauthor_tuples = self.read_paperauthor_csv(self.paperauthor_csv)
#        self.cid_info_dict = self.read_conference_jorunal_csv(self.Conference_csv)
#        self.jid_info_dict = self.read_conference_jorunal_csv(self.Journal_csv)


    '''
    Description: Load the Train.csv 
    Parameter: train_csv, the path of Train.csv file
    Return: the (authorid, paperid, label) tuples
    '''
    def read_train_csv(self, train_csv):
        train_tuples = list()
        train_csv_reader = csv.reader(file(train_csv,'r'))
        train_csv_reader.next()
        for cols in train_csv_reader:
            authorid = int(cols[0])
            confirmPapers = map(lambda x:int(x), cols[1].split())
            deletedPapers = map(lambda x:int(x), cols[2].split())
            for paperid in confirmPapers:
                train_tuples.append([authorid, paperid, 1])
            for paperid in deletedPapers:
                train_tuples.append([authorid, paperid, 0])
        return train_tuples
    '''
    Description: Load the Valid.csv 
    Parameter: valid_csv, the path of Valid.csv file
    Return: the (authorid, paperid, label) tuple
    '''
    def read_valid_csv(self, valid_csv):
        valid_tuples = list()
        valid_csv_reader = csv.reader(file(valid_csv, 'r'))
        valid_csv_reader.next()
        for cols in valid_csv_reader:
            authorid = int(cols[0])
            Papers = map(lambda x: int(x), cols[1].split())
            for paperid in Papers:
                valid_tuples.append([authorid, paperid, 0]) 
        return valid_tuples
        
    '''
    Description: Load the Paper.csv
    Parameter: paper_csv, the path of Paper.csv file
    Return: information dict of paper, ('conferenceid', 'journalid', 'title', 'year', 'keyword')
    '''
    def read_paper_csv(self, paper_csv):
        paper_csv_reader = csv.reader(file(paper_csv, 'r'))
        paper_csv_reader.next()
        paper_info_dict = ddict(lambda : dict())
        for cols in paper_csv_reader:
            paperid = int(cols[0])
            conferenceid = int(cols[3])
            journalid = int(cols[4])
            paper_info_dict[paperid]['conferenceid'] = conferenceid
            paper_info_dict[paperid]['journalid'] = journalid
            paper_info_dict[paperid]['title'] = cols[1]
            paper_info_dict[paperid]['year'] = int(cols[2])
            paper_info_dict[paperid]['keyword'] = cols[5]
        return paper_info_dict
    

    '''
    Description: Load the Author.csv
    Parameter: author_csv, the path of author.csv file
    Return: information dict of author, ('name', 'affi')
    '''
    def read_author_csv(self, author_csv):
        author_csv_reader = csv.reader(file(author_csv, 'r'))
        author_csv_reader.next()
        author_info_dict = ddict(lambda : dict())
        for cols in author_csv_reader:
            authorid = int(cols[0])
            name = cols[1]
            affi = cols[2]
            author_info_dict[authorid]['name'] = name
            author_info_dict[authorid]['affi'] = affi
        print 'reading author csv...'
#print 1703937 in author_info_dict
        return author_info_dict
    
    
    '''
    Description: Load the PaperAuthor.csv
    Parameter: paperauthor_csv, the path of file PaperAuthor.csv
    Return: the list of (paperid, authorid, name, affi)
    '''
    def read_paperauthor_csv(self, paperauthor_csv):
        paperauthor_csv_reader = csv.reader(file(paperauthor_csv, 'r'))
        paperauthor_csv_reader.next()
        
        paperauthor_tuples = list()
        for cols in paperauthor_csv_reader:
            paperid = int(cols[0])
            authorid = int(cols[1])
            name = cols[2]
            affi = cols[3]
            paperauthor_tuples.append((paperid, authorid, name, affi))
    
        return paperauthor_tuples

    '''
    Description: Load the Conference.csv or Journal.csv
    Parameter: Conference.csv or Journal
    Return: the dict of cid or jid, value: (short_name, long_name)
    '''
    def read_conference_jorunal_csv(self, conference_csv):
        csv_reader = csv.reader(file(conference_csv, 'r'))
        csv_reader.next()
        cid_info_dict = ddict(lambda:ddict())
        for cols in csv_reader:
            cid = int(cols[0])
            cid_info_dict[cid]['shortname'] = cols[1]
            cid_info_dict[cid]['longname'] = cols[2]
        return cid_info_dict

    

