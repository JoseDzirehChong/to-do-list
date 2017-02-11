#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
try:
    import tkinter as tk
except ImportError:
    import Tkinter as tk

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
        master.protocol("WM_DELETE_WINDOW", self.on_closing)

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
        try:
            with open('toDoListSaveFile.json') as infile:
                checkboxList = json.load(infile)
            for savedCheckbox in checkboxList:
                self.add(savedCheckbox)
        except (IOError, ValueError):
            #an error occured while loading ... so no saved settings loaded
            pass

    def on_closing(self):
        with open("toDoListSaveFile.json", 'w') as outfile:
            json.dump(self.checkboxList, outfile)
        self.quit()

def main():
    master = tk.Tk()
    master.title("To-Do List (with saving!)")
    master.geometry("300x300")
    win = MainWindow(master)
    win.pack(fill=tk.X)
    master.mainloop()

if __name__ == '__main__':
    main()
