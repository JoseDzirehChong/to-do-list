#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on Sun Jan 22 14:47:36 2017
@author: Jose Dzireh Chong
"""

#TODO:
    #Add scrollbar
    #Possibly add ability to modify and rearrange list items
    #Option for cloud or local JSON backup in case of file corruption (perhaps user could initiate it, it could be automated, or both)
    #Flesh out SettingsWin

#greatly improved by https://github.com/novel-yet-trivial

#imports
import json
try:
    import tkinter as tk
except ImportError:
    import Tkinter as tk
import os
import pymsgbox

#credit to /u/Dviv for this class
class WrappingCheckbutton(tk.Checkbutton):
    '''a type of Checkbutton that automatically adjusts the wrap to the size'''
    def __init__(self, master=None, **kwargs):
        tk.Checkbutton.__init__(self, master, **kwargs)
        self.bind('<Configure>', lambda e: self.config(wraplength=master.winfo_width()-65))

#credit to /u/novel_yet_trivial for this class
class WrappingLabel(tk.Label):
    '''a type of Label that automatically adjusts the wrap to the size'''
    def __init__(self, master=None, **kwargs):
        tk.Label.__init__(self, master, **kwargs)
        self.bind('<Configure>', lambda e: self.config(wraplength=master.winfo_width()))
        
class CheckboxRow(tk.Frame): #row the list item is on, includes checkbox, text and delete button
    def __init__(self, master, name, **kwargs):
        tk.Frame.__init__(self, master)
        
        MainWin = self.master.master
                
        self.name = name
        self.checkedStatus = tk.IntVar()  
        self.number = MainWin.checkboxNumber
        
        if kwargs.get("variable") == 1:
                self.checkedStatus.set(1)
                
        MainWin.checkboxList[self.number] = [name, self.checkedStatus.get()]
        MainWin.checkboxNumber += 1
        
        checkbox = WrappingCheckbutton(self, text=name, variable=self.checkedStatus, command=self.toggleStatus)
        checkbox.pack(side=tk.LEFT)

        deleteItem = tk.Button(self, text="x", bg="red", fg="white",
                                activebackground="white", activeforeground="red",
                                command=self.destroyCheckbox)
        deleteItem.pack(side=tk.RIGHT)
        

    def destroyCheckbox(self): #function to destroy the checkbox and the text and delete button that go with it
        destroyCheckbox_list = self.master.master.checkboxList
        
        destroyCheckbox_list.pop(self.number)

        self.destroy()
        self.master.master.saveToJSON()
        
    def toggleStatus(self, event=None):
        MainWin = self.master.master
        toggleStatus_list = MainWin.checkboxList
        if toggleStatus_list[self.number][1] == 1:
            toggleStatus_list[self.number][1] = 0

        elif toggleStatus_list[self.number][1] == 0:
            toggleStatus_list[self.number][1] = 1
                 
        self.master.master.saveToJSON()

class CheckboxArea(tk.Frame):
    def add(self, name, **kwargs):
        row = CheckboxRow(self, name, **kwargs)
        row.pack(fill=tk.X)

class InputStuff(tk.Frame):
    def __init__(self, master=None, **kwargs):
        tk.Frame.__init__(self, master, **kwargs)

        prompt = WrappingLabel(self, text="What do you want your checkbox to be for?")
        prompt.pack()

        bottomInput = tk.Frame(self)
        self.entry = tk.Entry(bottomInput, bd=3)
        self.entry.pack(side=tk.LEFT)
        buttonConfirm = tk.Button(bottomInput, text="Confirm", command=self.drawCheckbox)
        buttonConfirm.pack(side=tk.LEFT)
        bottomInput.pack()

        buttonDone = tk.Button(self, text = "Close Input", command=master.master.hideInputStuff)
        buttonDone.pack()

    def drawCheckbox(self, event=None):
        self.master.master.add(self.entry.get())
        self.entry.delete(0, tk.END)

class AddButtonArea(tk.Frame):
    def __init__(self, master=None, **kwargs):
        tk.Frame.__init__(self, master, **kwargs)
    
        self.addButton = tk.Button(self, text="Add Item", command=master.showInputStuff)
        self.addButton.pack()
        
class SettingsButtonArea(tk.Frame):
    def __init__(self, master=None, **kwargs):
        tk.Frame.__init__(self, master, **kwargs)
        self.settingsButton = tk.Button(self, text="Settings", command=self.switchToSettings)
        self.settingsButton.pack()
        
    def switchToSettings(self):
        self.master.master.settingsWin.pack()
        self.master.pack_forget()
    
class MainWindow(tk.Frame):
    def __init__(self, master=None, **kwargs):
        tk.Frame.__init__(self, master, **kwargs)
        
        #define filepaths
        self.SAVEFILE_DIR_FILEPATH = os.path.expanduser(os.path.join("~", "Documents", "joseDzirehChongToDoList"))
        self.SAVEFILE_FILEPATH = os.path.join(self.SAVEFILE_DIR_FILEPATH, "toDoListSaveFile.json")
        
        self.checkboxList = {}
        self.checkboxNumber = 0

        self.checkboxArea = CheckboxArea(self)
        self.checkboxArea.pack(fill=tk.X)
        
        self.addButtonArea = AddButtonArea(self)
        self.addButtonArea.pack()
        
        self.inputStuff = InputStuff(self.addButtonArea)
        
        self.settingsButtonArea = SettingsButtonArea(self)
        self.settingsButtonArea.pack()

        self.hideInputStuff() # start with "add" button active

        self.load()
        
    def saveToJSON(self):
        with open (self.SAVEFILE_FILEPATH, 'w') as outfile:
            json.dump(self.checkboxList, outfile)
            
        print(self.checkboxList) #for debugging purposes

    def add(self, name, **kwargs):
        self.checkboxArea.add(name, **kwargs)
        self.saveToJSON()

    def showInputStuff(self): #hides "add item" button. shows input text, box, and "confirm" button (all in inputStuff). binds "confirm" button to return key for ease of use
        self.addButtonArea.addButton.pack_forget()
        self.inputStuff.pack()
        self.inputStuff.entry.focus()
        self.master.bind('<Return>', self.inputStuff.drawCheckbox)

    def hideInputStuff(self): #hides input text, box, and "confirm" button (all in inputStuff). shows "add item" button. unbinds "confirm" button from the return key since that button is no longer on the screen
        self.inputStuff.pack_forget()
        self.addButtonArea.addButton.pack()
        self.master.unbind('<Return>')

    def load(self):
        
        def createFile(): #check if savefile and its parent directory exist, if not, create them
            if not os.path.isdir(self.SAVEFILE_DIR_FILEPATH):
                os.makedirs(self.SAVEFILE_DIR_FILEPATH, 0o0777)

            if not os.path.isfile(self.SAVEFILE_FILEPATH):
                f = open(self.SAVEFILE_FILEPATH, 'w')
                f.close()
                os.chmod(self.SAVEFILE_FILEPATH, 0o0666)
                            
        def checkIfSaveFileIsEmpty():
            if os.path.getsize(self.SAVEFILE_FILEPATH) == 0:
                self.saveToJSON()
                
        def lastStand(): #badly named function, loads list items from JSON when the JSON file exists, if not possible, alerts the user that something's not right
            try:
                with open(self.SAVEFILE_FILEPATH) as infile:    
                    checkboxList = json.load(infile)
            
                for key in checkboxList:
                    self.checkboxArea.add(checkboxList[key][0], variable=checkboxList[key][1])
            except (ValueError, IOError, PermissionError):
                pymsgbox.alert("""You're not supposed to see this message. If you do, something's wrong with your save file and this program couldn't fix it. Please email me at "josedzirehchong@gmail.com" with a copy of your save file attached (if it doesn't exist just tell me). It can be found at """ + self.SAVEFILE_FILEPATH + """.""", 'Broken Save File')

        createFile()
        checkIfSaveFileIsEmpty()
        lastStand()
        
class SettingsWindow(tk.Frame):
    def __init__(self, master=None, **kwargs):
        tk.Frame.__init__(self, master, **kwargs)
        self.widthHeightSettings = WidthHeightSettings(self)
        self.widthHeightSettings.pack()
        
        self.exitSettings = tk.Button(self, text = "Exit Settings", command = self.exitSettings)
        self.exitSettings.pack()
        
    def exitSettings(self):
        self.master.mainWin.pack(fill=tk.X)
        self.pack_forget()
        
class WidthHeightSettings(tk.Frame):
    def __init__(self, master=None, **kwargs):
        tk.Frame.__init__(self, master, **kwargs)
        self.title = tk.Label(self, text = "Width & Height")
        self.widthInput = tk.Entry(self, text = "Input Width (default 400px)")
        self.heightInput = tk.Entry(self, text = "Input Height (default 400px)")
        self.exitWidthHeight = tk.Button(self, text = "Exit Width & Height", command = self.exitWidthHeight)
        
        self.showButton = tk.Button(self, text = "Width & Height", command = self.show)
        self.showButton.pack()
        
    def show(self):
        self.title.pack()
        self.widthInput.pack()
        self.heightInput.pack()
        self.exitWidthHeight.pack()
        
        self.showButton.pack_forget()
        
    def exitWidthHeight(self):
        self.title.pack_forget()
        self.widthInput.pack_forget()
        self.heightInput.pack_forget()
        self.showButton.pack()
        self.exitWidthHeight.pack_forget()
        
class SuperFrame(tk.Frame):
    def __init__(self, master=None, **kwargs):
        tk.Frame.__init__(self, master, **kwargs)
        self.mainWin = MainWindow(self)
        self.mainWin.pack(fill=tk.X)
        
        self.settingsWin = SettingsWindow(self)
        
def main():
    
    #define width and height to avoid magic numbers
    WIDTH = 400
    HEIGHT = 400
    
    #basically making the window for this program
    master = tk.Tk()
    master.title("To-Do List")
    master.geometry("{}x{}".format(WIDTH, HEIGHT))
    
    superFrame = SuperFrame(master)
    superFrame.pack(fill=tk.X)
    
    master.mainloop()
    
    #saving to JSON at the end of every run of this program for redundancy
    superFrame.mainWin.saveToJSON()

if __name__ == '__main__':
    main()
