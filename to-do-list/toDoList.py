#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on Sun Jan 22 14:47:36 2017
@author: Jose Dzireh Chong
"""

#<IMPORTS>

import json

try:
    import tkinter as tk
except ImportError:
    import Tkinter as tk
import os
import pymsgbox

#</IMPORTS>

class CheckboxRow(tk.Frame): #row the list item is on, includes checkbox, text and delete button
    def __init__(self, master, name, **kwargs):
        tk.Frame.__init__(self, master)
        
        self.name = name
        self.checkedStatus = tk.IntVar()
        
        if kwargs.get("variable") == 1:
                self.checkedStatus.set(1)
                
        self.master.master.checkboxList.append([name, self.checkedStatus.get()])
        
        checkbox = tk.Checkbutton(self, text=name, variable=self.checkedStatus, command=self.toggleStatus)
        checkbox.pack(side=tk.LEFT)

        deleteItem = tk.Button(self, text="x", bg="red", fg="white",
                                activebackground="white", activeforeground="red",
                                command=self.destroyCheckbox)
        deleteItem.pack(side=tk.RIGHT)
        

    def destroyCheckbox(self): #function to destroy the checkbox and the text and delete button that go with it
        destroyCheckbox_checkboxList = self.master.master.checkboxList
        
        try:
            destroyCheckbox_checkboxList.remove([self.name, 0])
        except ValueError:
            destroyCheckbox_checkboxList.remove([self.name, 1])

        self.destroy()
        self.master.master.saveToJSON()
        
    def toggleStatus(self, event=None):
        toggleStatus_checkboxList = self.master.master.checkboxList
        try:
            toggleStatus_checkboxList[toggleStatus_checkboxList.index([self.name, 0])][1] = 1

        except ValueError:
            toggleStatus_checkboxList[toggleStatus_checkboxList.index([self.name, 1])][1] = 0
                 
        self.master.master.saveToJSON()

class CheckboxArea(tk.Frame):
    def add(self, name, **kwargs):
        row = CheckboxRow(self, name, **kwargs)
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
        
        #<define filepaths>
        self.SAVEFILE_DIR_FILEPATH = os.path.expanduser(os.path.join("~", "Documents", "joseDzirehChongToDoList"))
        self.SAVEFILE_FILEPATH = os.path.join(self.SAVEFILE_DIR_FILEPATH, "toDoListSaveFile.json")
        #</define filepaths>
        
        self.checkboxList = []

        self.checkboxArea = CheckboxArea(self)
        self.checkboxArea.pack(fill=tk.X)

        self.inputStuff = InputStuff(self)
        self.addButton = tk.Button(self, text="Add Item", command=self.showInputStuff)

        self.hideInputStuff() # start with "add" button active

        self.load()
        
    def saveToJSON(self):
        with open (self.SAVEFILE_FILEPATH, 'w') as outfile:
            json.dump(self.checkboxList, outfile)
            
        print(self.checkboxList) #for debugging purposes

    def add(self, name, **kwargs):
        self.checkboxArea.add(name, **kwargs)
        self.saveToJSON()

    def showInputStuff(self):
        self.addButton.pack_forget()
        self.inputStuff.pack()
        self.inputStuff.entry.focus()
        self.master.bind('<Return>', self.inputStuff.drawCheckbox)

    def hideInputStuff(self):
        self.inputStuff.pack_forget()
        self.addButton.pack()
        self.master.unbind('<Return>')

    def load(self):
        
        #<check if savefile and its parent directory exist, if not, create them>
        def createFile():
            if not os.path.isdir(self.SAVEFILE_DIR_FILEPATH):
                os.makedirs(self.SAVEFILE_DIR_FILEPATH, 0o0777)

            if not os.path.isfile(self.SAVEFILE_FILEPATH):
                f = open(self.SAVEFILE_FILEPATH, 'w')
                f.close()
                os.chmod(self.SAVEFILE_FILEPATH, 0o0666)
        #</check if savefile and its parent directory exist, if not, create them>
                            
        def checkIfSaveFileIsEmpty():
            if os.path.getsize(self.SAVEFILE_FILEPATH) == 0:
                self.saveToJSON()
                
        def lastStand():
            try:
                with open(self.SAVEFILE_FILEPATH) as infile:    
                    checkboxList = json.load(infile)
                for savedCheckbox in checkboxList:
                    self.checkboxArea.add(savedCheckbox[0], variable=savedCheckbox[1])
            except (ValueError, IOError, PermissionError):
                pymsgbox.alert("""You're not supposed to see this message. If you do, something's wrong with your save file and this program couldn't fix it. Please email me at "josedzirehchong@gmail.com" with a copy of your save file attached (if it doesn't exist just tell me). It can be found at """ + self.SAVEFILE_FILEPATH + """.""", 'Broken Save File')

        createFile()
        checkIfSaveFileIsEmpty()
        lastStand()
        
def main():
    WIDTH = 300
    HEIGHT = 300
    master = tk.Tk()
    master.title("To-Do List")
    master.geometry("{}x{}".format(WIDTH, HEIGHT))
    win = MainWindow(master)
    win.pack(fill=tk.X)
    master.mainloop()
    win.saveToJSON()

if __name__ == '__main__':
    main()
