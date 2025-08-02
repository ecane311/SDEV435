#this module configures the gui. it uses customtkinter and functions from webscrape.py
import os
import sys
from PIL import Image
import webscrape
import customtkinter as ctk
from webscrape import listHeadlines

def getAssets(filename):
    if getattr(sys, 'frozen', False): #checks if packaged with pyinstaller
        basepath = sys._MEIPASS #only relevant when frozen
    else: #running as .py
        basepath = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(basepath, filename)

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

logo = Image.open(getAssets("NOD.png"))
image = ctk.CTkImage(light_image=logo, dark_image=logo, size=(200, 200))
imagelbl = ctk.CTkLabel(mainframe,text="", image=image)
imagelbl.pack(pady=(0,20))

headlinesList = webscrape.listHeadlines()
global lbl
lbl = ctk.CTkLabel(mainframe, text=headlinesList, font=("Arial", 16))
lbl.pack(pady=(40, 0), padx=20)

def refreshHeadlines():
    global lbl
    headlines = listHeadlines()
    lbl.configure(text=headlines)


refreshbtn = ctk.CTkButton(mainframe, text="Refresh", command=refreshHeadlines)
refreshbtn.pack()

#Auto-refreshes headlines, includes toggle button
autoupdate = True
def autoRefresh():
    if autoupdate:
        refreshHeadlines()
        root.after(600000, autoRefresh())

refreshstatus = ctk.CTkLabel(mainframe, text='')

def toggleRefresh():
    global autoupdate
    autoupdate = not autoupdate
    status = "Auto-Refresh turned on" if autoupdate else "Auto-Refresh turned off"
    refreshstatus.configure(text=status)
    refreshstatus.pack()


togglebutton = ctk.CTkButton(mainframe, text="Toggle Auto-Refresh", command = toggleRefresh)
togglebutton.pack(pady=5)


##---------------------------------
#Options/settings page
optionsframe = notebook.tab("Options")

themelbl = ctk.CTkLabel(optionsframe, text="Change theme of application:", pady=5)
themelbl.pack()

def changeTheme(theme):
    ctk.set_appearance_mode(theme)

thememenu = ctk.CTkOptionMenu(optionsframe, values=["Light", "Dark"], command=changeTheme)
thememenu.set("Dark")
thememenu.pack(pady=10)

optionslbl = ctk.CTkLabel(optionsframe, text="Add a source: enter a name and a URL separated with a space to add it to News on Demand", pady=5)
optionslbl.pack()
sourcebox = ctk.CTkEntry(optionsframe)
sourcebox.pack()

errorlabel = ctk.CTkLabel(optionsframe)


#adds source
def addUserSource():
    userinput = sourcebox.get()
    newinput = userinput.split()
    if len(newinput) < 2: #if only one item
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


#remove source
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
#textbox so users can copy-paste in the gui
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
listbtn.pack(pady=5)

#gui driver
def mainLoop():
    root.mainloop()