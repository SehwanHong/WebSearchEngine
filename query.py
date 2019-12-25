import linecache
import os
import time
import gui
import math
from nltk.stem import PorterStemmer
import re

if __name__ == "__main__":
    print("Starting up...")
indexDict = eval(open("indexDict.txt").read())
idUrlDict = eval(open("idurl2.txt").read()) 
dfDict = eval(open("idf2.txt").read()) 
#idfDict = eval(open("finalIdf.txt").read())
stemmer = PorterStemmer()
count = 0
def findCommonDocuments(postingList1, postingList2):
    commonDocs = []
    i = 0 #index for postingList1
    j = 0 #index for postingList2
    while (i < len(postingList1) and j < len(postingList2)):
        if (postingList1[i][0] == postingList2[j][0]):
            newValue = postingList1[i][1] + postingList2[j][1]
            try:
                importantWeight = postingList1[i][2] + postingList2[j][2]
                #newValue = newValue + 1.5*importantWeight
            except:
                pass
            commonDocs.append((postingList1[i][0], newValue, importantWeight))
            i += 1
            j += 1
        elif (postingList1[i][0] < postingList2[j][0]):
            i += 1
        else:
            j += 1
    return commonDocs

def sortList(lst):
    try:
        lst.sort(key = lambda x: dfDict[x])
    except:
        return "No documents found for one keyword"
    
def printResults(docs):
    counter = 1
    resultStr = ""
    for tup in sorted(docs, key = lambda x: x[1] + .5*x[2], reverse = True):
        if counter > 10:
            break
        resultStr += (str(counter) + ". " + idUrlDict[int(tup[0])] + "\n")
        #print((str(counter) + ". " + idUrlDict[int(tup[0])] + "\n"))
        counter += 1
    if counter == 1:
        return "No results"
    return resultStr

def processQuery(string):
    global indexDict
    global idUrlDict
    global stemmer
    global count
    count = 0
    terms = string.split(" ")
    start = time.time()
    for i in range(len(terms)):
        terms[i] = stemmer.stem(terms[i])
    terms = list(set(terms))
    sortList(terms)
    listOfPostings = []
    try:
        for i in range(len(terms)):
            lineNum = indexDict[terms[i]]
            termDic = eval("{" + linecache.getline("index.txt", lineNum) + "}")
            listOfPostings.append(termDic[terms[i]])
        if len(terms) > 1:
            docs = listOfPostings[0]
            for i in range(1, len(terms)):
                docs = findCommonDocuments(docs, listOfPostings[i])
            resultStr = printResults(docs)
            end = time.time()
            resultStr += str((end - start))
            return resultStr
        else:
            resultStr = printResults(listOfPostings[0])
            end = time.time()
            resultStr += str((end - start))
            return resultStr
    except KeyError:
        return "No documents found for one keyword"
            
if __name__ == "__main__":
    gui = gui.GUI()
    gui.createDisplay()
    linecache.getline("index.txt", 0)
    print("Ready to process queries!")
    gui.run()
    
