import requests
from bs4 import BeautifulSoup
import csv
import os
import sys

csvfilename = 'NewsOnDemand.csv'
csvpath = ''

#function for getting headlines
def getHeadlines(url):
    global csvpath

    if not csvpath:  #ensure csvpath is set
        createCsv()

    response = requests.get(url)    #returns site
    soup = BeautifulSoup(response.text, "html.parser")  #parse site

    #default to <h2> unless csv specifies otherwise
    tag = "h2"

    #read csv and check third column
    with open(csvpath, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader, None)  #skip header
        for row in reader:
            if len(row) >= 3 and row[1] == url:
                tag = "h3" if row[2] == "1" else "h2"
                break  #stop searching once we find a match

    #extract headline based on tag
    headline = soup.find(tag)
    return headline.text if headline else "No headline found."



#creates csv file in the same path as executable / project
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

    #print(f"Debug: csvpath is set to {csvpath}")

    #checks if file exists
    fileexists = os.path.exists(csvpath)

    with open(csvpath, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        #if it doesn't exist, create one
        if not fileexists:
            writer.writerow(['Source', 'URL'])
            writer.writerow(['CNN', 'https://cnn.com/'])
            writer.writerow(['Fox', 'https://foxnews.com/', 1])
            writer.writerow(['NYT', 'https://nytimes.com/'])
            writer.writerow(['MSNBC', 'https://www.msnbc.com/'])
            ##ADD FIXED SOURCES HERE
        #print functions used for testing
        #print(f'file saved at: {csvpath}')

#Loops through csv file and gets sources for each entry
def listHeadlines ():
    global csvpath

    if not csvpath:
        createCsv()
    with open(csvpath, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader, None) #skips header

        headlinestext = ""

        for row in reader:
            source = row[0]
            url = row[1]
            headline = getHeadlines(url).strip() #prevents newlines
            headlinestext += f"{source}: {headline}\n"
    return headlinestext


#adds source to csv
def addSource(source, url):
    with open(csvpath, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([source, url])
    #print(f'added {source} - {url}')

#remmoves source
def removeSource(name):
    updatedrows = []
    with open(csvpath, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        header = next(reader)
        for row in reader:
            if row[0] != name:
                updatedrows.append(row)
    with open(csvpath, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([header])
        writer.writerows(updatedrows)
    #print(f'deleted {name}')


def addH3(url):
    global csvpath
    if not csvpath:
        createCsv()
    with open(csvpath, mode='a', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        header = next(reader)  #skip header
        for row in reader:
            if row[1] == url:
                while len(row) < 3:
                    row.append("")
                row[2] = "1"  #sets third column to 1 (h3)



# def listSources():
#     global csvpath
#     with open(csvpath, mode='r', newline='', encoding='utf-8') as file:
#         for item in file:
#             print(item)
