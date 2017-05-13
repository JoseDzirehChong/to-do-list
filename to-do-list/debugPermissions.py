#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on Sun Jan 22 14:47:36 2017
@author: Jose Dzireh Chong
"""
import os

#build the directory and file paths
SAVEFILE_DIR_FILEPATH = os.path.expanduser(os.path.join("~", "Documents", "joseDzirehChongToDoList"))
SAVEFILE_FILEPATH = os.path.join(SAVEFILE_DIR_FILEPATH, "toDoListSaveFile.json")

def createFile():
    if not os.path.isdir(SAVEFILE_DIR_FILEPATH):
        os.makedirs(SAVEFILE_DIR_FILEPATH, 0o0777)

    if not os.path.isfile(SAVEFILE_FILEPATH):
        f = open(SAVEFILE_FILEPATH, 'w')
        f.close()
        os.chmod(SAVEFILE_FILEPATH, 0o0666)

createFile()