from collections import defaultdict
import math
from nltk.stem import PorterStemmer
import codecs

class index:
    def __init__(self):
        self.termDict = defaultdict(set)
        self.idUrl = defaultdict(str)
        self.count = 0
        self.idfDict = defaultdict(float)
        self.urlTfIdfDict = defaultdict(dict)

    def index(self, tokens, url, importantWords):
        stemmer = PorterStemmer()
        raw_count_dict = defaultdict(int)
        word_count = 0
        self.count += 1
        self.idUrl[self.count] = url
        for token in tokens:
            raw_count_dict[stemmer.stem(token)] += 1
            word_count += 1
        for key, value in raw_count_dict.items():
            self.termDict[key].add((self.count, 1 + math.log10(value), importantWords.count(key)))
            self.idfDict[key] += 1
        if self.count % 10000 == 0:
            self.write()
            self.write_idurl()
            print("len of termDict = {}".format(len(self.termDict)))
    
    def write(self):
        report = self.report()
        file = codecs.open("index" + str(self.count//10000) +".txt", 'w', encoding="utf8")
        file.write(report)
        file.close()
        self.termDict = defaultdict(set)

    def write_idurl(self):
        idurl = self.idurl()
        file = codecs.open("idurl.txt", 'a', encoding="utf8")
        file.write(idurl)
        file.close()
        self.idUrl = defaultdict(int)

    def idurl(self):
        report = ''
        for k, v in self.idUrl.items():
            report += f'{k}: "{v}",'
            report += '\n'
        return report
   
    def calculate(self):
        self.tfidf()

    def report(self):
        report = ''
        for term, urlSet in sorted(self.termDict.items()):
            word_report = f'"{term}"' + ": ["
            for urlId in sorted(urlSet):
                word_report += f'{str(urlId)},'
            report += word_report[:-1]
            report += "]\n"
        return report
