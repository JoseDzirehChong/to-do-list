#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 22 14:47:36 2017

@author: Jose Chong
"""
import json
try:
    import tkinter as tk
except ImportError:
    import Tkinter as tk

import os
import pymsgbox

filepath = os.path.expanduser(r'~\Documents\joseDzirehChongToDoList\toDoListSaveFile.json')

checkboxList = []
        
def checkSaveFile():
    
    def checkExistenceOfSaveFile():
        if not os.path.isdir(os.path.expanduser(r'~\Documents\joseDzirehChongToDoList')):
            os.makedirs(os.path.expanduser(r'~\Documents\joseDzirehChongToDoList'), 777)
    
        if not os.path.isfile(filepath):
            open(filepath, 'w')
            open(filepath).close()
        
    def checkIfSaveFileIsEmpty():
        global checkboxList
        if os.path.getsize(filepath) == 0:
            with open (filepath, 'w') as outfile:
                    json.dump(checkboxList, outfile)
    

        with open(filepath) as infile:    
             checkboxList = json.load(infile)
    checkExistenceOfSaveFile()
    checkIfSaveFileIsEmpty()
    try:
        open(filepath, 'w')
        open(filepath).close()
    except (IOError, ValueError):
        
        pymsgbox.alert("""You're not supposed to see this message ever. If you do, that means your save file is either missing or corrupted, and my methods of stopping that have failed. Please email me at 'josedzirehchong@gmail.com' with a copy of your save file so I can tell what went wrong.

Click the button below to exit, the red button in the corner doesn't work.""", 'Broken Save File')

var = "placeholder"

checkSaveFile()

master = tk.Tk()
master.title("To-Do List")
master.geometry("300x300")

masterFrame = tk.Frame(master)

masterFrame.pack(fill=tk.X)

checkboxArea = tk.Frame(masterFrame, height=26)

checkboxArea.pack(fill=tk.X)

inputStuff = tk.Frame(masterFrame)

var = tk.IntVar()

def loadToJSON():
    with open(filepath, 'w') as outfile:
        json.dump(checkboxList, outfile)

class CheckboxRow(tk.Frame):
    def __init__(self, master, text):
        self.text = text
        tk.Frame.__init__(self, master)
        checkbox = tk.Checkbutton(self, text=text, variable=var)
        checkbox.pack(side=tk.LEFT)
        
        deleteItem = tk.Button(self, text="x", bg="red", fg="white",
                                activebackground="white", activeforeground="red",
                                command=self.destroyCheckbox)
        deleteItem.pack(side=tk.RIGHT)
        self.master.master.checkboxList.append([self.name, var.get()])
        loadToJSON()
        
    def destroyCheckbox(self):
        self.master.master.checkboxList.remove(self.name)
        self.destroy()
        loadToJSON()
        
def destroyCheckbox(checkbox, row):
    row.destroy()
    del checkboxList[-1]
    loadToJSON()

for savedCheckbox in checkboxList:
    checkboxRow = tk.Frame(checkboxArea)
    checkboxRow.pack(fill=tk.X)
    checkbox1 = tk.Checkbutton(checkboxRow, text=savedCheckbox[0], variable=var)
    checkbox1.pack(side=tk.LEFT)
    deleteItem = tk.Button(checkboxRow, text="x", bg="red", fg="white",
                                activebackground="white", activeforeground="red",
                                command=lambda c=savedCheckbox, r=checkboxRow: destroyCheckbox(c, r))
    deleteItem.pack(side=tk.RIGHT)

    loadToJSON()

def drawCheckbox():
    newCheckboxInput = entry.get()               
    checkboxList.append([newCheckboxInput, 0])
    entry.delete(0,tk.END)
    checkboxRow = tk.Frame(checkboxArea)
    checkboxRow.pack(fill=tk.X)
    checkbox1 = tk.Checkbutton(checkboxRow, text = checkboxList[-1][0], variable = var)
    checkbox1.pack(side=tk.LEFT)
    deleteItem = tk.Button(checkboxRow, text = "x", command=lambda c=checkbox1, r=checkboxRow: destroyCheckbox(c,r), bg="red", fg="white", activebackground="white", activeforeground="red")
    deleteItem.pack(side=tk.RIGHT)

    loadToJSON()


def createInputStuff():
    paddingFrame = tk.Frame(inputStuff, height=5)
    paddingFrame.pack(fill=tk.X)
    buttonDone.pack()
    inputStuff.pack()
    buttonAdd.pack_forget()
    master.bind('<Return>', lambda event: drawCheckbox())

def removeInputStuff():
    inputStuff.pack_forget()
    buttonAdd.pack()
    buttonDone.pack_forget()
    master.unbind('<Return>')


buttonDone = tk.Button(inputStuff, text = "Close Input", command=removeInputStuff)


buttonAdd = tk.Button(masterFrame, text="Add Item", command=createInputStuff)
buttonAdd.pack()


topInput = tk.Frame(inputStuff)
bottomInput = tk.Frame(inputStuff)

topInput.pack()
bottomInput.pack()

prompt = tk.Label(topInput, text="What do you want your checkbox to be for?")
prompt.pack()
entry = tk.Entry(bottomInput, bd=3)
entry.pack(side=tk.LEFT)
buttonConfirm = tk.Button(bottomInput, text="Confirm", command=drawCheckbox)
buttonConfirm.pack(side=tk.LEFT)
master.mainloop()