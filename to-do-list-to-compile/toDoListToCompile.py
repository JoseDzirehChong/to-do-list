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

checkSaveFile()

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
        newItem = [self.text, var.get()]
        self.master.master.checkboxList.append(newItem)
        loadToJSON()
        
    def destroyCheckbox(self, text):
        self.text = text
        newItem = [self.text, var.get()]
        self.master.master.checkboxList.remove(newItem)
        self.destroy()
        loadToJSON()
        

class CheckboxArea(tk.Frame):
    def add(self, name):
        row = CheckboxRow(self, name)
        row.pack(fill=tk.X)
        
class InputStuff(tk.Frame):
    def __init__(self, master=None, **kwargs):
        tk.Frame.__init__(self, master, **kwargs)

        prompt = tk.Label(self, text="What do you want your checkbox to be for?")
        prompt.pack()

        bottomInput = tk.Frame(self)
        self.entry = tk.Entry(bottomInput, bd=3)
        self.entry.pack(side=tk.LEFT)
        buttonConfirm = tk.Button(bottomInput, text="Confirm", command=self.drawCheckbox)
        buttonConfirm.pack(side=tk.LEFT)
        bottomInput.pack()

        buttonDone = tk.Button(self, text = "Close Input", command=master.hideInputStuff)
        buttonDone.pack()

    def drawCheckbox(self, event=None):
        self.master.add(self.entry.get())
        self.entry.delete(0, tk.END)
        
class MainWindow(tk.Frame):
    def __init__(self, master=None, **kwargs):
        tk.Frame.__init__(self, master, **kwargs)

        self.checkboxList = []

        self.checkboxArea = CheckboxArea(self)
        self.checkboxArea.pack(fill=tk.X)

        self.inputStuff = InputStuff(self)
        self.addButton = tk.Button(self, text="Add Item", command=self.showInputStuff)

        self.hideInputStuff() # start with "add" button active

        self.load()
        
    def load(self):
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

    def add(self, name):
        self.checkbox_area.add(name)
        self.checkboxList.append(name)

    def showInputStuff(self):
        self.addButton.pack_forget()
        self.input_stuff.pack()
        self.input_stuff.entry.focus()
        self.master.bind('<Return>', self.input_stuff.drawCheckbox)

    def hideInputStuff(self):
        self.inputStuff.pack_forget()
        self.addButton.pack()
        self.master.unbind('<Return>')
    
def main():
    master = tk.Tk()
    master.title("To-Do List (with saving!)")
    master.geometry("300x300")
    win = MainWindow(master)
    win.pack(fill=tk.X)
    master.mainloop()

if __name__ == "__main__":
    main()