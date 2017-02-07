# -*- coding: utf-8 -*-
"""
Created on Sun Jan 22 14:47:36 2017

@author: Jose Chong
"""
import json
import tkinter

master = tkinter.Tk()
master.title("To-Do List (with saving!)")
master.geometry("300x300")

masterFrame = tkinter.Frame(master)

masterFrame.pack(fill=tkinter.X)

checkboxArea = tkinter.Frame(masterFrame, height=26)

checkboxArea.pack(fill=tkinter.X)

inputStuff = tkinter.Frame(masterFrame)

checkboxList = []

with open('toDoListSaveFile.json') as infile:    
    checkboxList = json.load(infile)
    
def destroyCheckbox(checkbox, row):
    row.destroy()
    del checkboxList [checkboxList.index(str(checkbox))]

for savedCheckbox in checkboxList:
    checkboxRow = tkinter.Frame(checkboxArea)
    checkboxRow.pack(fill=tkinter.X)
    checkbox1 = tkinter.Checkbutton(checkboxRow, text=savedCheckbox)
    checkbox1.pack(side=tkinter.LEFT)
    deleteItem = tkinter.Button(checkboxRow, text="x", bg="red", fg="white",
                                activebackground="white", activeforeground="red",
                                command=lambda c=savedCheckbox, r=checkboxRow: destroyCheckbox(c, r))
    deleteItem.pack(side=tkinter.RIGHT)

def drawCheckbox():
    newCheckboxInput = entry.get()
    def destroyCheckbox():
        checkboxRow.destroy()
        del checkboxList[checkboxList.index(newCheckboxInput)]
    checkboxList.append(newCheckboxInput)
    entry.delete(0,tkinter.END)
    checkboxRow = tkinter.Frame(checkboxArea)
    checkboxRow.pack(fill=tkinter.X)
    checkbox1 = tkinter.Checkbutton(checkboxRow, text = checkboxList[-1])
    checkbox1.pack(side=tkinter.LEFT)
    deleteItem = tkinter.Button(checkboxRow, text = "x", command=destroyCheckbox, bg="red", fg="white", activebackground="white", activeforeground="red")
    deleteItem.pack(side=tkinter.RIGHT)
    with open("toDoListSaveFile.json", 'w') as outfile:
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