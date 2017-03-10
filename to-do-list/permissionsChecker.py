import os
import pathlib

FOLDER_FILEPATH = os.path.expanduser(os.path.join("~", "Documents", "joseDzirehChongToDoList"))
SAVEFILE_FILEPATH = os.path.expanduser(os.path.join("~", "Documents", "joseDzirehChongToDoList", "toDoListSaveFile.json"))

pathlibFolderPath = pathlib.Path(FOLDER_FILEPATH)
pathlibSavefilePath = pathlib.Path(SAVEFILE_FILEPATH)

folderPermissions = oct(os.stat(FOLDER_FILEPATH).st_mode)[-3:]
savefilePermissions = oct(os.stat(SAVEFILE_FILEPATH).st_mode)[-3:]

folderOwner = pathlibFolderPath.owner
savefileOwner = pathlibSavefilePath.owner

def printPermissionsAndOwnership():
    print("joseDzirehChongToDoList has {} permissions and is owned by {}".format(folderPermissions, folderOwner))
    print()
    print("toDoListSaveFile.json has {} permissions and is owned by {}".format(savefilePermissions, savefileOwner))

printPermissionsAndOwnership()