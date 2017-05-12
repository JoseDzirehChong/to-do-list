#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on Sun Jan 22 14:47:36 2017
@author: Jose Dzireh Chong
"""
import os

SAVEFILE_FILEPATH = os.path.expanduser(os.path.join("~", "Documents", "joseDzirehChongToDoList", "toDoListSaveFile.json"))

def createFile():
    if not os.path.isdir(os.path.expanduser(os.path.join("~", "Documents", "joseDzirehChongToDoList"))):
        os.makedirs(os.path.expanduser(os.path.join("~", "Documents", "joseDzirehChongToDoList")), 777)
    if not os.path.isfile(SAVEFILE_FILEPATH):
        f = open(SAVEFILE_FILEPATH, 'w')
        f.close()
        os.chmod(SAVEFILE_FILEPATH, 666)
    
createFile()