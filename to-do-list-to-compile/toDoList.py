# -*- coding: utf-8 -*-
"""
Created on Sun Jan 22 14:47:36 2017

@author: Jose Chong
"""
import json
import tkinter
import os

filepath = os.path.expanduser(r'~\Documents\joseDzirehChongToDoList\toDoListSaveFile.json')

def checkExistenceOfSaveFile():
    if not os.path.isdir(os.path.expanduser(r'~\Documents\joseDzirehChongToDoList')):
        os.makedirs(os.path.expanduser(r'~\Documents\joseDzirehChongToDoList'), 777)
    
    if not os.path.isfile(filepath):
        open(filepath, 'w')
        open(filepath).close()
        
checkExistenceOfSaveFile()

master = tkinter.Tk()
master.title("To-Do List")
master.geometry("300x300")

masterFrame = tkinter.Frame(master)

masterFrame.pack(fill=tkinter.X)

checkboxArea = tkinter.Frame(masterFrame, height=26)

checkboxArea.pack(fill=tkinter.X)

inputStuff = tkinter.Frame(masterFrame)

checkboxList = []

if os.path.getsize(filepath) == 0:
    with open (filepath, 'w') as outfile:
        json.dump(checkboxList, outfile)
    

with open(filepath) as infile:    
    checkboxList = json.load(infile)

def destroyCheckbox(checkbox, row):
    row.destroy()
    del checkboxList [checkboxList.index(str(checkbox))]

    with open(filepath, 'w') as outfile:
        json.dump(checkboxList, outfile)

for savedCheckbox in checkboxList:
    checkboxRow = tkinter.Frame(checkboxArea)
    checkboxRow.pack(fill=tkinter.X)
    checkbox1 = tkinter.Checkbutton(checkboxRow, text=savedCheckbox)
    checkbox1.pack(side=tkinter.LEFT)
    deleteItem = tkinter.Button(checkboxRow, text="x", bg="red", fg="white",
                                activebackground="white", activeforeground="red",
                                command=lambda c=savedCheckbox, r=checkboxRow: destroyCheckbox(c, r))
    deleteItem.pack(side=tkinter.RIGHT)

    with open(filepath, 'w') as outfile:
        json.dump(checkboxList, outfile)

def drawCheckbox():
    newCheckboxInput = entry.get()
    def destroyCheckbox():
        checkboxRow.destroy()
        del checkboxList[checkboxList.index(newCheckboxInput)]
        with open(filepath, 'w') as outfile:
            json.dump(checkboxList, outfile)                 
    checkboxList.append(newCheckboxInput)
    entry.delete(0,tkinter.END)
    checkboxRow = tkinter.Frame(checkboxArea)
    checkboxRow.pack(fill=tkinter.X)
    checkbox1 = tkinter.Checkbutton(checkboxRow, text = checkboxList[-1])
    checkbox1.pack(side=tkinter.LEFT)
    deleteItem = tkinter.Button(checkboxRow, text = "x", command=lambda c=checkbox1, r=checkboxRow: destroyCheckbox(), bg="red", fg="white", activebackground="white", activeforeground="red")
    deleteItem.pack(side=tkinter.RIGHT)

    with open(filepath, 'w') as outfile:
        json.dump(checkboxList, outfile)


def createInputStuff():
    paddingFrame = tkinter.Frame(inputStuff, height=5)
    paddingFrame.pack(fill=tkinter.X)
    buttonDone.pack()
    inputStuff.pack()
    buttonAdd.pack_forget()
    master.bind('<Return>', lambda event: drawCheckbox())

def removeInputStuff():
    inputStuff.pack_forget()
    buttonAdd.pack()
    buttonDone.pack_forget()
    master.unbind('<Return>')


buttonDone = tkinter.Button(inputStuff, text = "Close Input", command=removeInputStuff)


buttonAdd = tkinter.Button(masterFrame, text="Add Item", command=createInputStuff)
buttonAdd.pack()


topInput = tkinter.Frame(inputStuff)
bottomInput = tkinter.Frame(inputStuff)

topInput.pack()
bottomInput.pack()

prompt = tkinter.Label(topInput, text="What do you want your checkbox to be for?")
prompt.pack()
entry = tkinter.Entry(bottomInput, bd=3)
entry.pack(side=tkinter.LEFT)
buttonConfirm = tkinter.Button(bottomInput, text="Confirm", command=drawCheckbox)
buttonConfirm.pack(side=tkinter.LEFT)

master.mainloop()