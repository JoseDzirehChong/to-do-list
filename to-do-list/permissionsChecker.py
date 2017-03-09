import os

folderFilepath = os.path.expanduser(os.path.join("~", "Documents", "joseDzirehChongToDoList"))
savefileFilepath = os.path.expanduser(os.path.join("~", "Documents", "joseDzirehChongToDoList", "toDoListSaveFile.json"))
print("joseDzirehChongToDoList has %s permissions" % oct(os.stat(folderFilepath).st_mode)[-3:])
print("toDoListSaveFile.json has %s permissions" % oct(os.stat(savefileFilepath).st_mode)[-3:])