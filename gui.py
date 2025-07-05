from tkinter import *
from tkinter import ttk
from requests import options
import webscrape
import customtkinter as ctk
from webscrape import listHeadlines

#gui root
root = ctk.CTk()
root.title("News on Demand")
root.geometry('800x700')

#create notebook for tabbed view
notebook = ctk.CTkTabview(root)
notebook.pack(expand=True, fill="both")
notebook.add("Home")
notebook.add("Options")


#main page
mainframe = notebook.tab("Home")
headlinesList = webscrape.listHeadlines()
global lbl
lbl = ctk.CTkLabel(mainframe, text=headlinesList, font=("Arial", 16))
lbl.pack(pady=(80, 0), padx=20)

def refreshHeadlines():
    global lbl
    headlines = listHeadlines()
    lbl.configure(text=headlines)
    #testlabel = ctk.CTkLabel(mainframe, text="refresh pressed")
    #testlabel.pack()

refreshbtn = ctk.CTkButton(mainframe, text="Refresh", command=refreshHeadlines)
refreshbtn.pack()


#Options/settings page
optionsframe = notebook.tab("Options")
optionslbl = ctk.CTkLabel(optionsframe, text="Add a source: enter a name and a URL separated with a space to add it to News on Demand", pady=5)
optionslbl.pack()
sourcebox = ctk.CTkEntry(optionsframe)
sourcebox.pack()

errorlabel = ctk.CTkLabel(optionsframe)

def addUserSource():
    userinput = sourcebox.get()
    newinput = userinput.split()
    if len(newinput) < 2:
        errorlabel.configure(text="Enter a name and a URL separated with a space.", text_color="red")
        errorlabel.pack()
        sourcebox.delete(0, ctk.END)
        return
    if not newinput[1].startswith(("http://", "https://")):
        errorlabel.configure(text="URL must start with http:// or https://", text_color="red")
        errorlabel.pack()
        sourcebox.delete(0, ctk.END)
        return
    webscrape.addSource(newinput[0], newinput[1])
    sourcebox.delete(0, ctk.END)

addbutton = ctk.CTkButton(optionsframe, text="Add", command=addUserSource)
addbutton.pack(pady=15)


#removes a news source using removeSource from webscrape.py
removelbl = ctk.CTkLabel(optionsframe, text="Remove a source: enter a source name to remove it from the program", pady=5)
removelbl.pack()

deletebox = ctk.CTkEntry(optionsframe)
deletebox.pack()

def removeUserSource():
    userinput = deletebox.get()
    try:
        webscrape.removeSource(userinput)
    except ValueError as e:
        errorlabel.configure(text=str(e), text_color="red")
        errorlabel.pack()
    deletebox.delete(0, ctk.END)

removebutton = ctk.CTkButton(optionsframe, text="Remove", command=removeUserSource)
removebutton.pack(pady=15)

#modifies the csv file to indicate to the webscraper to look for h3 instead of h2
h3lbl= ctk.CTkLabel(optionsframe, text="Try getting <h3>: If a source is not working properly, enter the URL here to try a different method of getting headlines", pady=5)
h3lbl.pack()

h3box = ctk.CTkEntry(optionsframe)
h3box.pack()

def tryH3():
    userinput = h3box.get()
    if not userinput.startswith(("http://", "https://")):
        errorlabel.configure(text="URL must start with http:// or https://", text_color="red")
        errorlabel.pack()
        h3box.delete(0, ctk.END)
        return
    webscrape.addH3(userinput)
    h3box.delete(0, ctk.END)

h3button = ctk.CTkButton(optionsframe, text="Try H3", command=tryH3)
h3button.pack(pady=15)

#lists current sources in the gui
listlbl = ctk.CTkLabel(optionsframe, text="List of current sources", pady=10)
listlbl.pack()

global source
startsourcelist = webscrape.listSources()
source = ctk.CTkTextbox(optionsframe, width=300, height=150)
source.tag_config("center", justify="center")
source.pack()
source.insert("1.0", startsourcelist, "center")
source.configure(state="disabled")

def listSources():
    sourcelist = webscrape.listSources()
    source.configure(state="normal")
    source.delete("1.0", "end")
    source.insert("1.0", sourcelist, "center")
    source.configure(state="disabled")
    source.pack()
listbtn = ctk.CTkButton(optionsframe, text="Update List", command=listSources)
listbtn.pack()

#gui driver
def mainLoop():
    root.mainloop()