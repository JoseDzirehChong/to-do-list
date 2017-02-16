#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

try:
    import tkinter as tk
except ImportError:
    import Tkinter as tk
import os
import pymsgbox

class CheckboxRow(tk.Frame):
    def __init__(self, master, name, **kwargs):
        tk.Frame.__init__(self, master, **kwargs)
        self.name = name

        checkbox = tk.Checkbutton(self, text=name)
        checkbox.pack(side=tk.LEFT)

        deleteItem = tk.Button(self, text="x", bg="red", fg="white",
                                activebackground="white", activeforeground="red",
                                command=self.destroyCheckbox)
        deleteItem.pack(side=tk.RIGHT)

    def destroyCheckbox(self):
        self.master.master.checkboxList.remove(self.name)
        self.destroy()

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

        buttonDone = tk.Button(self, text = "Close Input", command=master.hide_input_stuff)
        buttonDone.pack()

    def drawCheckbox(self, event=None):
        self.master.add(self.entry.get())
        self.entry.delete(0, tk.END)

class MainWindow(tk.Frame):
    def __init__(self, master=None, **kwargs):
        tk.Frame.__init__(self, master, **kwargs)
        
        self.filepath = os.path.expanduser(r'~\Documents\joseDzirehChongToDoList\toDoListSaveFile.json')

        self.checkboxList = []

        self.checkbox_area = CheckboxArea(self)
        self.checkbox_area.pack(fill=tk.X)

        self.input_stuff = InputStuff(self)
        self.add_button = tk.Button(self, text="Add Item", command=self.show_input_stuff)

        self.hide_input_stuff() # start with "add" button active

        self.load()

    def add(self, name):
        self.checkbox_area.add(name)
        self.checkboxList.append(name)

    def show_input_stuff(self):
        self.add_button.pack_forget()
        self.input_stuff.pack()
        self.input_stuff.entry.focus()
        self.master.bind('<Return>', self.input_stuff.drawCheckbox)

    def hide_input_stuff(self):
        self.input_stuff.pack_forget()
        self.add_button.pack()
        self.master.unbind('<Return>')

    def load(self):
        def checkExistenceOfSaveFile():
            if not os.path.isdir(os.path.expanduser(r'~\Documents\joseDzirehChongToDoList')):
                os.makedirs(os.path.expanduser(r'~\Documents\joseDzirehChongToDoList'), 777)
                
                if not os.path.isfile(self.filepath):
                    open(self.filepath, 'w')
                    open(self.filepath).close()
                    
        def checkIfSaveFileIsEmpty():
            if os.path.getsize(self.filepath) == 0:
                with open (self.filepath, 'w') as outfile:
                    json.dump(self.checkboxList, outfile)
                        

            with open(self.filepath) as infile:    
                 self.checkboxList = json.load(infile)

    
        def lastStand(filepath):
            try:
                open(self.filepath, 'w')
                open(self.filepath).close()
            except (IOError, ValueError):
                pymsgbox.alert("""You're not supposed to see this message ever. If you do, that means your save file is either missing or corrupted, and my methods of stopping that have failed. Please email me at 'josedzirehchong@gmail.com' with a copy of your save file so I can tell what went wrong.

Click the button below to exit, the red button in the corner doesn't work.""", 'Broken Save File')
       
        checkExistenceOfSaveFile()
        checkIfSaveFileIsEmpty()
        lastStand()

def main():
    master = tk.Tk()
    master.title("To-Do List (with saving!)")
    master.geometry("300x300")
    win = MainWindow(master)
    win.pack(fill=tk.X)
    master.mainloop()

if __name__ == '__main__':
    main()
