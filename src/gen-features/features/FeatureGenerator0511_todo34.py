# --encoding: utf-8 -

from Data import *

'''
todo:
1) paper title 是否为空
2) paper keywords 是否为空
3) paper cid
4) paper jid
'''
class FeatureGenerator0511_todo34:
    def __init__(self, data):
        self.data = data
    
    def get_feature(self, authorid, paperid):
        paper_title_empty_flag = 0
        paper_keyword_empty_flag = 0
        paper_cid = -1
        paper_jid = -1
        if paperid not in self.data.paper_info_dict:
            paper_title_empty_flag = 1
            paper_keyword_empty_flag = 1
        else:
            if self.data.paper_info_dict[paperid]['title'].strip() == '':
                paper_title_empty_flag = 1
            else:
                paper_title_empty_flag = 0

            if self.data.paper_info_dict[paperid]['keyword'].strip() == '':
                paper_keyword_empty_flag = 1
            else:
                paper_keyword_empty_flag = 0
            paper_cid = self.data.paper_info_dict[paperid]['conferenceid']
            paper_jid = self.data.paper_info_dict[paperid]['journalid']
        return [paper_cid, paper_jid]
#        return [paper_title_empty_flag, paper_keyword_empty_flag]
            
    
