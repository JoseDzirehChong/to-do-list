import os
try:
    import pwd
except ImportError:
    import win32security

FOLDER_FILEPATH = os.path.expanduser(os.path.join("~", "Documents", "joseDzirehChongToDoList"))
SAVEFILE_FILEPATH = os.path.expanduser(os.path.join("~", "Documents", "joseDzirehChongToDoList", "toDoListSaveFile.json"))

folderPermissions = oct(os.stat(FOLDER_FILEPATH).st_mode)[-3:]
savefilePermissions = oct(os.stat(SAVEFILE_FILEPATH).st_mode)[-3:]

try:
    folderOwnerFinal = pwd.getpwuid(os.stat(FOLDER_FILEPATH).st_uid).pw_name
    savefileOwnerFinal = pwd.getpwuid(os.stat(SAVEFILE_FILEPATH).st_uid).pw_name

except NameError:
    folderOwnerTemp = win32security.GetFileSecurity(FOLDER_FILEPATH, win32security.OWNER_SECURITY_INFORMATION)
    folderOwnerSID = folderOwnerTemp.GetSecurityDescriptorOwner()
    folderOwner, folderOwnerDomain, type = win32security.LookupAccountSid(None, folderOwnerSID)
    folderFinal = os.path.join(folderOwnerDomain, folderOwner)
    
    savefileOwnerTemp = win32security.GetFileSecurity(SAVEFILE_FILEPATH, win32security.OWNER_SECURITY_INFORMATION)
    savefileOwnerSID = savefileOwnerTemp.GetSecurityDescriptorOwner()
    savefileOwner, savefileOwnerAndDomain, type = win32security.LookupAccountSid(None, savefileOwnerSID)
    savefileFinal = os.path.join(savefileOwnerAndDomain, savefileOwner)
    
def printPermissionsAndOwnership():
    print("joseDzirehChongToDoList has {} permissions and is owned by {}".format(folderPermissions, folderFinal))
    print()
    print("toDoListSaveFile.json has {} permissions and is owned by {}".format(savefilePermissions, savefileFinal))

printPermissionsAndOwnership()