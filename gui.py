from tkinter import *
from tkinter import ttk
from requests import options
import webscrape
import customtkinter as ctk
from webscrape import listHeadlines

#gui root
root = ctk.CTk()
root.title("News on Demand")
root.geometry('720x540')

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
lbl.pack(pady=80, padx=20)

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
optionslbl = ctk.CTkLabel(optionsframe, text="This is the options page")
optionslbl.pack()
sourcebox = ctk.CTkEntry(optionsframe)
sourcebox.pack()

errorlabel = ctk.CTkLabel(optionsframe)
global newinput

def addUserSource():
    userinput = sourcebox.get()
    global newinput
    newinput = userinput.split()
    if len(newinput) < 2:
        errorlabel.configure(text="Enter a name and a URL separated with a space.")
        errorlabel.pack()
        return
    webscrape.addSource(newinput[0], newinput[1])

addbutton = ctk.CTkButton(optionsframe, text="Add", command=addUserSource)
addbutton.pack(pady=10)

def mainLoop():
    root.mainloop()