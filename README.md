# About

[LATEST EXE HERE](https://github.com/JoseDzirehChong/to-do-list/releases/tag/v0.0.0)

This is a to-do list. It saves between runs of the program through writing list items to a JSON file. It is coded using Python 3. It is the first "full" Python project I made for myself, that is, not following a tutorial.

Please note that renaming the save file or the folders it is in will cause a new savefile to be created. This to-do list will not be able to retrieve data from your original file (until you rename it and the directories it is in to their original name), instead it will retrieve data from the new savefile it has created. 

The modules it uses are:

- `tkinter` (makes the interface)
- `json` (deals with the data in the savefile)
- `os` (deals with the creation of the savefile if one does not yet exist)
- `pymsgbox` (deals with the creation of an error message which ideally will never be used)

# Installation

There's two ways to go about this.

If you want access to the code, download `toDoListToCompile.py` from the `to-do-list-to-compile` folder. `toDoListToCompile.py` can also be found as part of the source code download in the "Releases" section of this repository. Install [`pymsgbox`](http://pymsgbox.readthedocs.io/en/latest/basics.html). Finally, run `toDoListToCompile.py` using your IDE of choice. All modules other than `pymsgbox` already come with Python, so installation of those is not necessary.

If you just want a to-do list, download the exe from the link under "Info", then run it as you would a normal program.

# Contact

Email: `josedzirehchong@gmail.com`. Contact me on this email about bugs, feature requests, business inquiries etc..
