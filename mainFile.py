from win32 import win32gui as w
import time
import keyboard
import pyautogui as pya
import pyperclip
from tkinter import *
import scraper
import os




#myShortcut = 'ctrl+c'
#window2 = Tk()
def checkWindow():
    windowName = w.GetWindowText(w.GetForegroundWindow()).lower()
    windowNameWords = windowName.split()

    expectedWordsList = ['adobe', 'acrobat', 'reader']

    for word in expectedWordsList:
        if word not in windowNameWords:
            return 0

    return 1

def createMeaningWindow(meaningString, word):
    window = Tk()
    #pos = pya.position()
    #window.geometry('%dx%d+%d+%d' % (504, 650, pos.x, pos.y))
    window.geometry('700x500')
    print('WORD: '+word)
    window.title(word)
    #frame = Frame(window, width=400, height=400)
    #frame.grid(row=0, column=0, sticky="nsew")
    print('MEANING STRING: '+meaningString)
    baseFont = 'Verdana'
    frame=Frame(window, width=100, height=50).pack(fill=BOTH, expand=YES)#.place(x=700,y=0)
    lb = Label(frame, text=meaningString, wraplength=650)#, width=120, height=10)
    lb.config(font = baseFont)
    lb.pack(fill=BOTH, expand=YES)
    #lb.pack()
    #lb.grid(row=0, column=0)
    window.lift()
    window.attributes('-topmost',True)
    window.after_idle(window.attributes,'-topmost',False)
    window.focus_set()
    window.focus_force()
    window.mainloop()

def onButtonClick(name, window2):
    print('The new, corrected name: '+name)
    window2.destroy()
    getMeaning(name)

def printOptionsWindow(options):
    window2 = Tk()
    window2.geometry("504x650")
    window2.title("Did you mean:")
    frame = Frame(window2, width=400, height=400)
    #frame.pack()
    frame.grid(row=0, column=0, sticky="nsew")
    window2.grid_rowconfigure(0, minsize=400, weight=1)
    window2.grid_columnconfigure(0, minsize=400, weight=1)
    rowCount = 0
    for item in options:
        button = Button(frame, text=item, command=lambda x=item: onButtonClick(x, window2))
        button.grid(row=rowCount, column=1)
        rowCount += 1
    window2.lift()
    window2.attributes('-topmost',True)
    #window2.after_idle(window.attributes,'-topmost',False)
    window2.focus_set()
    window2.focus_force()
    window2.mainloop()

def storeWordInFile(word):
    file = open("words.txt", "a+")
    alreadyStoredWords = file.readlines()
    if len(alreadyStoredWords) > 0:
        if word not in alreadyStoredWords:
            file.write(word+'\n')
    else:
        file.write(word+'\n')
    file.close()

def getMeaning(word):
        
    print('Hello2')
    obj = scraper.meaning(word)
    if obj.wordNotAvailableFlag == 1:
        #options = "\n".join(obj.possibleCorrectWords)
        printOptionsWindow(obj.possibleCorrectWords)
        storeWordInFile(word)
        return
    print('Hello3')
    print('url: '+obj.url)
    obj.buildMeanings()
    obj.printMeaningsWithLessInfo()
    print(obj.allInfoAsAString)
    print('Hello4')
    createMeaningWindow(obj.allInfoAsAString, word)
    print('Hello5')

    storeWordInFile(word)

    
    
def findMeaning():
    flag = checkWindow()
    if flag == 1:
        word = pyperclip.paste()

        word = word.lower()
        print(word)
        
        
        check = word.split()
        if len(check) == 1:
            getMeaning(word)
        
    
    
    

#keyboard.add_hotkey(myShortcut, getMeaning)
startKey = 'ctrl'
endKey = 'c'
word = ''
while True:
    if keyboard.is_pressed(startKey):
        #time.sleep(0.25)
        if keyboard.is_pressed(endKey):
            time.sleep(0.25)
            print('Hello1')
            findMeaning()
    
