from nltk.stem import PorterStemmer
import json
import html2text
import re
from collections import defaultdict
from sys import getsizeof
import codecs
import os
from index import index
from urllib.parse import urldefrag
from bs4 import BeautifulSoup



def readJson(file) -> (str, str):
    #read file from the json file and change it into a string
    file = open(file)
    data = json.load(file)
    if data["encoding"] not in ["utf-8", "ascii"]:
    	return None
    htmlContent = data["content"]
    url = data["url"]
    url = urldefrag(url)[0]
    file.close()
    return htmlContent, url


def parseHtml(htmlContent):
    # From html str parse the html into tokens and make a dictionary
    html2txt = html2text.HTML2Text()
    html2txt.ignore_links = True
    html2txt.ignore_images = True
    importantWords = []
    soup = BeautifulSoup(htmlContent, 'html.parser')
    for title in soup.find_all('title'):
        importantWords = re.findall("[\w]+", title.text, re.ASCII)
    for bold in soup.find_all('b'):
        importantWords = importantWords + re.findall("[\w]+", bold.text, re.ASCII)
    for header in soup.find_all('h1'):
        importantWords = importantWords + re.findall("[\w]+", header.text, re.ASCII)
    for header in soup.find_all('h2'):
        importantWords = importantWords + re.findall("[\w]+", header.text, re.ASCII)
    for header in soup.find_all('h3'):
        importantWords = importantWords + re.findall("[\w]+", header.text, re.ASCII)
    tokens = re.findall("[\w]+", html2txt.handle(htmlContent), re.ASCII)
    return tokens, importantWords 

def saveFile(report: str):
    #save stem dictionary into index.txt
    file = codecs.open("index.txt", 'w', encoding="utf8")
    file.write(report)
    file.close()

def saveReport(count, term_dict):
    dict_size = getsizeof(term_dict)
    file = codecs.open("report.txt", 'w', encoding="utf8")
    file.write("Number of Documents : " + str(count) + "\n")
    file.write("Number of Unique words : " + str(len(term_dict.keys())) + "\n")
    file.write("Size of index in bytes: " + str(dict_size) + " bytes\n")
    file.write("Size of index in KB (1000): " + str(dict_size/1000) + " KB\n")
    file.write("Size of index in KiB (1024): " + str(dict_size/1024) + " KiB\n")
    file.close()


if __name__ == "__main__":
    basedir = "/home/lopes/Datasets/IR/DEV"
    newIndex = index()
    for directory in os.listdir(basedir):
        dirLinks = []
        for file in os.listdir(basedir + "/" + directory):
            tup = readJson(basedir + '/' + directory+ '/' + file)
            if tup == None:
                continue
            if tup[1] in dirLinks:
                continue
            dirLinks.append(tup[1])
            tokens, importantWords = parseHtml(tup[0])
            newIndex.index(tokens, tup[1], importantWords)
            print('this the the {}th file'.format(newIndex.count))
    newIndex.write()
    newIndex.write_idurl()
    file = codecs.open("idf.txt", 'w', encoding="utf8")
    file.write(str(dict(newIndex.idfDict)))
    file.close()
    
