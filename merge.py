import codecs
from collections import defaultdict
import math
import os
import re

count = 50553

def getfilenames():
    filenamelist = []
    pattern = re.compile("index[0-9]+\.txt")
    for file in os.listdir(os.curdir):
        if pattern.match(file):
            filenamelist.append(file)
    return filenamelist

def openfiles():
    files = getfilenames()
    openfiles = []
    for file in files:
        openfiles.append(codecs.open(file, 'r', encoding="utf8"))
    return openfiles

def closefiles(openfiles: list):
    for file in openfiles:
        file.close()
    return

def main():
    openfilelist = openfiles()
    #print("before idfdict")
    idfdict = getidfdict()
    #print("after idfdict")
    filelength = len(openfilelist)
    linelist = [None] * filelength
    indexfile = codecs.open("index.txt", "w", encoding="utf8")
    getnewline = set(range(filelength))
    x = 1
    finished = set()
    indexdict = codecs.open("indexDict.txt", 'w', encoding='utf8')
    indexdict.write('{')
    while(True):
        print(getnewline)
        for i in getnewline:
            linelist[i] = eval("{" + getline(openfilelist[i]) + "}")
        if checklinelistempty(linelist):
            break
        report, key, getnewline = merge(linelist, idfdict, filelength)
        for i in range(filelength):
            if i in getnewline: 
                linelist[i] = None
        indexfile.write(report)
        indexdict.write(f"'{key}' : {x} ,\n")
        print(f"printed the {x}th word")
        x += 1
    indexdict.write('}')
    closefiles(openfilelist)
    indexdict.close()
    #print("finished")
        

def merge(linelist:list, idfdict:dict, filelength) -> (str, str, {int}):
    merged = defaultdict(list)
    key = getcurrentkey(linelist, filelength)
    getnewline = set()
    for i in range(filelength):
        if (linelist[i] != None and key in linelist[i].keys()):
            getnewline.add(i)
            merged[key].extend(linelist[i][key])
    return report(merged, count/idfdict[key]), key, getnewline

def report(mergedict:dict, idf) -> str:
    report = ''
    for key, value in mergedict.items():
        report += '"' + key + '"' + " : ["
        for urlid, tf, field in value:
            report += '(' + str(urlid) + ', '
            report += str(tf*math.log10(idf)) + ', '
            report += str(field) + '), '
        report = report[:-2] + ']\n'
    return report

def getcurrentkey(linelist:list, filelength) -> set:
    keys = set()
    for i in range(filelength):
        if bool(linelist[i]):
            keys.add(list(linelist[i].keys())[0])
    if bool(keys):
        return sorted(keys)[0]
    else:
        return None

def checklinelistempty(linelist:list):
    tf = True
    for line in linelist:
        tf *= not bool(line)
    return tf

def getidfdict():
    idfdict = eval(codecs.open("idf.txt",'r',encoding="utf8").readline())
    return idfdict

def getline(openfile):
    line = openfile.readline()
    return line

if __name__ == "__main__":
    main()
