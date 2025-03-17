# -*- coding: utf-8 -*-
"""
Created on Sun Nov 25 11:29:56 2018

@author: chris
"""
import getdbfields as dlg
from PyQt5 import QtWidgets
import json 

try :
    FP = open('FydStore.json', 'r')
    store = json.load(FP)
    FP.close()
except :
    store = {}
    
app = QtWidgets.QApplication([]) 
w = dlg.dlgFields(store)  
w.show()
app.exec_()


# if w.Ret == 0 :  #accepted : btn ok/cancelled
Fields = w.Fields
dir_path = w.dirPath
Sessnr = w.Sessnr
#   ID = w.ID

# The FYDStor is used to cache the contents of the json file
store = { "Fields" : Fields, "dirPath" : dir_path, "Sessnr" : Sessnr }
FP = open('FydStore.json', 'w')
json.dump(store, FP)
FP.close()
    #print(json.dumps(flds))
