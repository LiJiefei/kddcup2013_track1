### Model description

### Basic algorithm
GBDT(package sklearn in python) <br/>
RGF(Regularization Greedy forest, http://stat.rutgers.edu/home/tzhang/software/rgf/) <br/>


### Features
1) count paper published by the author in this paper journal <br/> 
2) count paper published by the author in this paper conference <br/>
3) count paper published by the author <br/>
4) count author of this paper <br/>
5) count papers with coauthor <br/>
6) 5)/4) <br/>
7) count times <authorid, paperid> appear in PaperAuthor.csv  <br/>
8) count paper published by the author in this paper year <br/>
9) count paper published in journal by the author <br/>
10) count paper published in conference by the author <br/>
11) 1)/9) <br/>
12) 2)/10) <br/>
13) count paper appeared in the predict paperlist of the author <br/>
14) the year of paper, if year>=2013, value=-1, if year ￡lt 1600, value = 0  <br/>
15) The affication of PaperAuthor.csv == the affication of the author in Author.csv <br/>
16) count of coauthor whose affication is the same with the author <br/>
17) the conferenceid of the paper <br/>
18) the journalid of the paper <br/>
19) count of the different affication in this paper <br/>
20) The name of PaperAuthor.csv == the name of the author in Author.csv <br/>
21) count of coauthor whose  affication is the same with author (affication in the PaperAuthor.csv) <br/>
22) The affication of PaperAuthor.csv == the affication of the author in Author.csv  <br/>
23) 3)/(count of different affication of paper) <br/>
24) whether the coauthor have the same name with author <br/>
25) count of the coauthor which does not appear in the author.csv <br/>
26) count of the same keyword between paper and author <br/>
27) count of paper keywords <br/>
28) 26)/27) <br/>
29) for the (authorid, paperid), we find the (other_authorid, paperid) which appear in PaperAuthor.csv twice, find the all paper published by the author, we say te set in S1. And then we find all paper published by the other_authorid, we say the set S2. the feature value is the count of common id between S1 and S2. <br/>
30) whether there is one coauthor whose name is the same with the author <br/>
31) whether there is one coauthor whose last name is same with the author, but the first name is not. <br/>
32-35) the mean, max, min, stdev of name similarity between coauthor and the author <br/>
35-39) the mean, max, min, stdev of other name similarity between coauthor and the author <br/>


