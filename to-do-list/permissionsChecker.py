import os
import pwd

FOLDER_FILEPATH = os.path.expanduser(os.path.join("~", "Documents", "joseDzirehChongToDoList"))
SAVEFILE_FILEPATH = os.path.expanduser(os.path.join("~", "Documents", "joseDzirehChongToDoList", "toDoListSaveFile.json"))

folderPermissions = oct(os.stat(FOLDER_FILEPATH).st_mode)[-3:]
savefilePermissions = oct(os.stat(SAVEFILE_FILEPATH).st_mode)[-3:]

folderOwner = pwd.getpwuid(os.stat(FOLDER_FILEPATH).st_uid).pw_name
savefileOwner = pwd.getpwuid(os.stat(SAVEFILE_FILEPATH).st_uid).pw_name

def printPermissionsAndOwnership():
    print("joseDzirehChongToDoList has {} permissions and is owned by {}".format(folderPermissions, folderOwner)
    print()
    print("toDoListSaveFile.json has {} permissions and is owned by {}".format(savefilePermissions, savefileOwner)

printPermissionsAndOwnership()
