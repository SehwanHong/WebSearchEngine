from nltk.stem import PorterStemmer
import json
import html2text
import re
from collections import defaultdict
from sys import getsizeof
import codecs
import os

stem_dict = defaultdict(set)
count = 0


def readJson(file) -> str:
    #read file from the json file and change it into a string
    global count
    count += 1
    file = open(file)
    data = json.load(file)
    htmlContent = data["content"]
    return htmlContent


def parseHtml(htmlContent, fileName):
    # From html str parse the html into tokens and make a dictionary
    html2txt = html2text.HTML2Text()
    html2txt.ignore_links = True
    html2txt.ignore_images = True
    tokens = re.findall("[\w']+", html2txt.handle(htmlContent), re.ASCII)
    stem(tokens, fileName)


def stem(tokens: list , url: str):
    #from list of string make a dictionary based on token
    stemmer = PorterStemmer()
    for token in tokens:
        stem_dict[stemmer.stem(token)].add(url)
    

def saveFile(stemDict: dict):
    #save stem dictionary into index.txt
    file = codecs.open("index.txt", 'w', encoding="utf8")
    stemStr = dictToStr(dict(stemDict))
    file.write(stemStr)
    file.close()

def saveReport():
    dict_size = getsizeof(stem_dict)
    file = codecs.open("report.txt", 'w', encoding="utf8")
    file.write("Number of Documents : " + str(count) + "\n")
    file.write("Number of Unique words : " + str(len(stem_dict.keys())) + "\n")
    file.write("Size of index in bytes: " + str(dict_size) + " bytes\n")
    file.write("Size of index in KB: " + str(dict_size/1000) + " KB\n")
    file.write("Size of index in KiB: " + str(dict_size/1024) + " KiB\n")
    file.close()

def dictToStr(dictionary: dict) -> str:
    dictstr = ''
    for k,v in dictionary.items():
        dictstr += k
        dictstr += " : "
        dictstr += str(v)
        dictstr += '\n'
    return dictstr

if __name__ == "__main__":
    basedir = "/home/lopes/Datasets/IR/DEV"
    for directory in os.listdir(basedir):
        for file in os.listdir(basedir + "/" + directory):
            htmlContent = readJson(basedir + '/' + directory+ '/' + file)
            parseHtml(htmlContent, file)
    saveFile(stem_dict)
    saveReport()
    