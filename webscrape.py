#This module contains the webscraping and csv functions. webscraping is done with bs4
import requests
from bs4 import BeautifulSoup
import csv
import os
import sys
from utils import readCsv, writeCsv, appendCsv

csvfilename = 'NewsOnDemand.csv'
csvpath = ''

def getHeadlines(url):
    global csvpath

    if not csvpath:  #ensure csvpath is set
        createCsv()

    response = requests.get(url)    #returns site
    soup = BeautifulSoup(response.text, "html.parser")  #parse site

    #default to <h2> unless csv specifies otherwise
    tag = "h2"

    #read csv and check third column
    allrows = readCsv(csvpath, skipheader=True)
    for row in allrows:
            if len(row) >= 3 and row[1] == url:
                tag = "h3" if row[2] == "1" else "h2"
                break  #stop searching once we find a match

    #extract headline based on tag
    headline = soup.find(tag)
    return headline.text if headline else "No headline found."


#I wanted the file to be consistent in where it can be found by both the user and the program
def createCsv():
    global csvpath
    #gets filepath of script/exe
    if getattr(sys, 'frozen', False): #if its running as an exe
        script_dir = os.path.dirname(sys.executable)
    else: #if its running as .py
        script_dir = os.path.dirname(os.path.abspath(__file__))

    #creates filepath for csv
    csvpath = os.path.join(script_dir, csvfilename)


    fileexists = os.path.exists(csvpath)

    with open(csvpath, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        if not fileexists:
            writer.writerow(['Source', 'URL', "h3"])
            writer.writerow(['CNN', 'https://cnn.com/'])
            writer.writerow(['Fox', 'https://foxnews.com/', 1])
            writer.writerow(['AP', 'https://apnews.com/', 1])
            writer.writerow(['MSNBC', 'https://www.msnbc.com/'])
            writer.writerow(['NPR', 'https://www.npr.org/', 1])
            writer.writerow(['ABC', 'https://abcnews.go.com/', 1])


#Loops through csv file and gets sources for each entry
def listHeadlines ():
    global csvpath

    if not csvpath:
        createCsv()
    datarows = readCsv(csvpath, skipheader=True)

    headlinestext = ""

    for row in datarows:
        source = row[0]
        url = row[1]
        headline = getHeadlines(url).strip() #prevents newlines
        headlinestext += f"{source}: {headline}\n\n"
    return headlinestext



def addSource(source, url):
    appendCsv(csvpath, [source, url])



def removeSource(name):
    allrows = readCsv(csvpath)
    header = allrows[0]
    datarows = allrows[1:]

    updatedrows = [row for row in datarows if row[0] != name]
    if len(updatedrows) == len(datarows):
        raise ValueError(f'"{name}" not found')
    writeCsv(csvpath, header, updatedrows)

#indicates getHeadlines to use <h3> for a particular source
def addH3(url):
    global csvpath
    if not csvpath:
        createCsv()

    updatedrows = []
    allrows = readCsv(csvpath)
    header = allrows[0]
    datarows = allrows[1:]

    for row in datarows:
        if len(row) < 3:
            row.append("")
        if row[1] == url:
            row[2] = "1" if row[2] != "1" else "" #1 if 3rd row is blank, switches back to nothing if 3rd row is 1
        updatedrows.append(row)
    writeCsv(csvpath, header, updatedrows)



def listSources():
    global csvpath
    sourcelist = ""
    datarows = readCsv(csvpath, skipheader=True)
    for row in datarows:
        if len(row) >= 2:
            source = row[0]
            url = row[1]
            sourcelist += f"{source}: {url}\n"
    return sourcelist
