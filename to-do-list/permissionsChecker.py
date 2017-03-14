import os
try:
    import pwd
    import grp
except ImportError:
    import win32security

FOLDER_FILEPATH = os.path.expanduser(os.path.join("~", "Documents", "joseDzirehChongToDoList"))
SAVEFILE_FILEPATH = os.path.expanduser(os.path.join("~", "Documents", "joseDzirehChongToDoList", "toDoListSaveFile.json"))

folderPermissions = oct(os.stat(FOLDER_FILEPATH).st_mode)[-3:]
savefilePermissions = oct(os.stat(SAVEFILE_FILEPATH).st_mode)[-3:]

try:
    folderOwner = pwd.getpwuid(os.stat(FOLDER_FILEPATH).st_uid).pw_name
    folderGroup = grp.getgruid(os.stat(FOLDER_FILEPATH).st_gid).gr_name
    folderFinal = os.path.join(folderGroup, folderOwner)

    savefileOwner = pwd.getpwuid(os.stat(SAVEFILE_FILEPATH).st_uid).pw_name
    savefileGroup = grp.getgruid(os.stat(SAVEFILE_FILEPATH).st_gid).gr_name
    savefileFinal = os.path.join(savefileGroup, savefileOwner)

except NameError:
    folderOwnerTemp = win32security.GetFileSecurity(FOLDER_FILEPATH, win32security.OWNER_SECURITY_INFORMATION)
    folderOwnerSID = folderOwnerTemp.GetSecurityDescriptorOwner()
    folderOwner, folderOwnerDomain, type = win32security.LookupAccountSid(None, folderOwnerSID)
    folderFinal = os.path.join(folderOwnerDomain, folderOwner)
    
    savefileOwnerTemp = win32security.GetFileSecurity(SAVEFILE_FILEPATH, win32security.OWNER_SECURITY_INFORMATION)
    savefileOwnerSID = savefileOwnerTemp.GetSecurityDescriptorOwner()
    savefileOwner, savefileOwnerDomain, type = win32security.LookupAccountSid(None, savefileOwnerSID)
    savefileFinal = os.path.join(savefileOwnerDomain, savefileOwner)
    
def printPermissionsAndOwnership():
    print("joseDzirehChongToDoList has {} permissions and is owned by {}".format(folderPermissions, folderFinal))
    print()
    print("toDoListSaveFile.json has {} permissions and is owned by {}".format(savefilePermissions, savefileFinal))

printPermissionsAndOwnership()