


'''
add the topic feature of dading 0606

'''


def load_topic_simi(topic_file):
    fp = open(topic_file, 'r')
    fp.readline()
    authorpaper_topic_dict = dict()
    for line in fp:
        cols = line.strip().split(',')
        authorid = int(cols[0])
        paperid = int(cols[1])
        authorpaper_topic_dict[(authorid, paperid)] = map(float, cols[2].split()[:88])

    return authorpaper_topic_dict

class FeatureGenerator0607:
    def __init__(self, data):
        self.data = data
        self.authorpaper_topic_dict = load_topic_simi(data.dading_topic_simi_csv)

    def get_feature(self, authorid, paperid):
        return self.authorpaper_topic_dict[(authorid, paperid)]

    
