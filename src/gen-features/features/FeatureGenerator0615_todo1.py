# --encoding: gbk -
'''

1) add the feature of dading, base on my fold
2) add the feature of dading, base on dading fold

'''
import csv
from collections import defaultdict as ddict

def read_dading_simi_csv(dading_simi_csv):
    select_feaid_str = [86, 281, 282, 283, 284, 161, 185, 186, 187, 188, 521, 522, 523, 524, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 39, 285, 286, 287, 288, 237, 238, 239, 240, 525, 526, 527, 528, 40, 289, 290, 291, 292, 193, 194, 195, 196, 529, 530, 531, 532, 241, 242, 243, 244, 385, 386, 387, 388, 41, 293, 294, 295, 296, 245, 246, 247, 248, 485, 486, 487, 488, 42, 441, 442, 443, 444, 43, 541, 542, 543, 544, 205, 206, 207, 208, 545, 546, 547, 548, 497, 498, 499, 500, 501, 502, 503, 504, 213, 214, 215, 216, 405, 406, 407, 408, 457, 458, 459, 460, 65, 361, 362, 363, 364, 409, 410, 411, 412, 509, 510, 511, 512, 513, 514, 515, 516, 225, 226, 227, 228, 417, 418, 419, 420, 517, 518, 519, 520, 229, 230, 231, 232, 421, 422, 423, 424, 373, 374, 375, 376, 277, 278, 279, 280]

    csv_reader = csv.reader(file(dading_simi_csv))
    csv_reader.next()
    authorpaper_simi_dict = dict()
    for cols in csv_reader:
        authorid = int(cols[0])
        paperid = int(cols[1])
        fealist = list()
        for idx in select_feaid_str:
            fealist.append(float(cols[idx]))

        authorpaper_simi_dict[(authorid, paperid)] = fealist

    return authorpaper_simi_dict

class FeatureGenerator0615_todo1:
    def __init__(self, data):
        self.data = data
        self.authorpaper_simi_dict = read_dading_simi_csv(self.data.info_input + '/dading_data/0611_similarity/features.csv')
        return

    def get_feature(self, authorid, paperid):
        return self.authorpaper_simi_dict[(authorid, paperid)]

