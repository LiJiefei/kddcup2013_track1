 Model description.

Basic algorithm: GBDT(package sklearn in python), RGF(Regularization Greedy forest, http://stat.rutgers.edu/home/tzhang/software/rgf/)


Features:
1) count paper published by the author in this paper journal
2) count paper published by the author in this paper conference 
3) count paper published by the author
4) count author of this paper
5) count papers with coauthor
6) 5)/4)
7) count times <authorid, paperid> appear in PaperAuthor.csv 
8) count paper published by the author in this paper year
9) count paper published in journal by the author
10) count paper published in conference by the author
11) 1)/9)
12) 2)/10)
13) count paper appeared in the predict paperlist of the author
14) the year of paper, if year>=2013, value=-1, if year <1600, value = 0 
15) The affication of PaperAuthor.csv == the affication of the author in Author.csv
16) count of coauthor whose affication is the same with the author
17) the conferenceid of the paper
18) the journalid of the paper
19) count of the different affication in this paper
20) The name of PaperAuthor.csv == the name of the author in Author.csv
21) count of coauthor whose  affication is the same with author (affication in the PaperAuthor.csv)
22) The affication of PaperAuthor.csv == the affication of the author in Author.csv 
23) 3)/(count of different affication of paper)
24) whether the coauthor have the same name with author
25) count of the coauthor which does not appear in the author.csv
26) count of the same keyword between paper and author
27) count of paper keywords
28) 26)/27)
29) for the (authorid, paperid), we find the (other_authorid, paperid) which appear in PaperAuthor.csv twice, find the all paper published by the author, we say te set in S1. And then we find all paper published by the other_authorid, we say the set S2. the feature value is the count of common id between S1 and S2.
30) whether there is one coauthor whose name is the same with the author
31) whether there is one coauthor whose last name is same with the author, but the first name is not.
32-35) the mean, max, min, stdev of name similarity between coauthor and the author
35-39) the mean, max, min, stdev of other name similarity between coauthor and the author





