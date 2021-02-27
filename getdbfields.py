# -*- coding: utf-8 -*-
"""
Created on Fri Nov 23 15:21:49 2018

@author: chris
"""

import sys
import os
import json
import re
#import datetime
import mysql.connector 
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QMessageBox
from design import Ui_GetdbFields
from NWdlg import Ui_Dialog

from Conn import dbc

class DbConn(object): 
    def __init__(self): 
        self.db = mysql.connector.connect( 
                    host= dbc['host'], 
                    user= dbc['user'], 
                    passwd= dbc['passw'],
                    database= dbc['Database']
                    ) 
        self.cursor = self.db.cursor() 

    def connected(self):
        return self.db.is_connected()
    
    def close(self): 
        self.db.close() 
    
    def reopen(self):
        self.db.reconnect()
 
    def query(self,sql): 
        self.cursor.execute(sql) 
        return self.cursor.fetchall()
    
    def update(self, sql):
        self.cursor.execute(sql)
        self.db.commit()

    
class dlgNew(QtWidgets.QDialog):
    def __init__(self, Allist): 
        super(dlgNew, self).__init__()
        self.ui = Ui_Dialog() 
        self.ui.setupUi(self)
        self.Allist = Allist
        self.ui.cbAll.addItems(Allist)
        self.ui.cbAll.currentIndexChanged.connect(self.ChooseItem)
        self.ui.Ed_Id.textChanged.connect(self.CheckNw)
        self.ui.buttonBox.accepted.connect(lambda: self.Pushed(0))
        self.ui.buttonBox.rejected.connect(lambda: self.Pushed(1))
        self.ui.label_species.setVisible(False)
        self.ui.cbSpecies.setVisible(False)
        self.ui.label_sex.setVisible(False)
        self.ui.cbSex.setVisible(False)
        self.ui.label_genotype.setVisible(False)
        self.ui.Ed_Genotyp.setVisible(False)
        self.ui.cbSpecies.addItems(['human', 'monkey', 'rat', 'mouse'])
        self.ui.cbSex.addItems(['M', 'F', 'U'])
        
    def ChooseItem(self):
        self.ui.Ed_Id.setText(self.ui.cbAll.currentText())
    
    def Pushed(self, Btn_selected):
        self.Ret = Btn_selected;
        if not (self.Ret == 0 and len(self.ui.Ed_Id.text()) == 0) :
            self.close()

    def CheckNw(self):
        val = self.ui.Ed_Id.text()       
        pattern = r'^[a-zA-Z0-9][-.\w]*$'
        if(len(val) > 0 and not re.search(pattern, val)) :          
            res = QMessageBox.question(self,"ERROR:Invalid Input: ", "Please use valid characters:  a-zA-Z0-9_.- ", QMessageBox.Ok)

        elif len(self.Allist) > 0 :
            self.ui.cbAll.disconnect()
            self.ui.cbAll.clear()
            for strval in self.Allist :
                z = re.search(r'^'+val, strval)
                if z:
                    self.ui.cbAll.addItem(strval)

            self.ui.cbAll.currentIndexChanged.connect(self.ChooseItem)
        
 
class dlgFields(QtWidgets.QMainWindow): 
    def __init__(self, store ): 
        super(dlgFields, self).__init__() 
        self.ui = Ui_GetdbFields() 
        self.ui.setupUi(self)
        if len(store): 
            self.Fields = store["Fields"]
            self.dirPath = store["dirPath"]
            self.Sessnr = store["Sessnr"]
        else:
            self.Fields = {}
            self.dirPath = ''
            self.Sessnr = 0         
        self.Allist = []
        self.ID = ''
        self.Project = ''
        self.Dataset = ''
        self.Condition = ''
        self.Subject = ''
        self.Setup = ''
        self.Stimulus = ''
        self.Investigator = ''
        self.bOnce = True
        self.ui.label_Database.setText(self.ui.label_Database.text() + dbc['Database'])
        self.ui.spinSessnr.setValue(self.Sessnr)
        #self.DT = datetime.datetime.now()
        #self.ui.label_Date.setText(self.ui.label_Date.text() + self.DT.strftime("%Y /%m /%d"))
        self.show()
        self.mydb = DbConn() 
        self.fillProject() 
       # self.mydb.close()
        self.ui.cbProject.currentIndexChanged.connect(self.selchangeProj)
        
 #       self.ui.pbDone.clicked.connect(self.Done) 
        self.ui.pbProject.clicked.connect(self.NwProject)      
        self.ui.pbCondition.clicked.connect(self.NwCondition)
        self.ui.pbDataset.clicked.connect(self.NwDataset)
        self.ui.pbSubject.clicked.connect(self.NwSubject)
        self.ui.pbSetup.clicked.connect(self.NwSetup)
        self.ui.pbStimulus.clicked.connect(self.NwStimulus)
        self.ui.pbInvestigator.clicked.connect(self.NwInvestigator)
        self.ui.dateEdit.setDate(QtCore.QDate.currentDate())
        self.ui.dateEdit.dateChanged.connect(self.NwID)
        self.ui.spinSessnr.valueChanged.connect(self.NwSessnr)

        self.ui.btnSave.clicked.connect(self.Save)
        self.ui.buttonBox.accepted.connect(self.Done)
        self.ui.buttonBox.rejected.connect(self.Cancelled)
        self.NwID()
            
    def fillProject(self):
        sql = "SELECT projectid, idx FROM projects"
        strlst  = self.mydb.query(sql) 
        lst = [i[0] for i in strlst]
        self.ui.cbProject.addItem('.') 
        self.ui.cbProject.addItems(lst) 
        self.Projects = lst
        self.Project = self.ui.cbDataset.currentText()
        self.ProjId = lst[0][1] 
        if 'project' in self.Fields and self.Fields["project"] in lst :
            idx = lst.index(self.Fields["project"])+1
            self.ui.cbProject.setCurrentIndex(idx)
            self.Project = self.ui.cbProject.currentText()
            sql = 'SELECT idx FROM projects WHERE projectid = "' + self.Project + '"'
            strlst = self.mydb.query(sql)
            self.ProjId = strlst[0][0]
            
            sql = 'SELECT datasetid, idx FROM datasets WHERE project ="' + str(self.Project) + '"'
            strlst  = self.mydb.query(sql) 
            lst = [i[0] for i in strlst]
            if len(lst) > 0 :
                self.ui.cbDataset.addItems(lst)
                self.Datasets = lst
                if 'dataset' in self.Fields and self.Fields["dataset"] in lst :
                    idx = lst.index(self.Fields["dataset"])                  
                    self.ui.cbDataset.setCurrentIndex(idx)
                    
                self.Dataset = self.ui.cbDataset.currentText()
                self.DatasetId = strlst[idx][1]
                self.ui.cbDataset.setEnabled(True)
                self.ui.pbDataset.setEnabled(True)
                self.ui.cbDataset.currentIndexChanged.connect(self.selDataset)

                sql = 'SELECT conditionid FROM conditions WHERE dataset ="' + str(self.Dataset) +  \
                      '" AND project = "' + str(self.Project) + '"'                   
                strlst = self.mydb.query(sql)
                lst = [i[0] for i in strlst]             
                self.Conditionlist = lst;
                self.ui.cbCondition.addItems(lst)
                if 'condition' in self.Fields and self.Fields["condition"] in lst :
                    idx = lst.index(self.Fields["condition"])                  
                    self.ui.cbCondition.setCurrentIndex(idx)
                    
                self.Condition = self.ui.cbCondition.currentText()                
                self.ui.cbCondition.setEnabled(True) 
                self.ui.pbCondition.setEnabled(True)
                self.ui.cbCondition.currentIndexChanged.connect(self.selCondition) 
                

            sql = 'SELECT subject FROM projects_subjects WHERE project ="' + str(self.Project) + '"'
            strlst = self.mydb.query(sql) 
            lst = [i[0] for i in strlst]
            self.Subjectlist = lst;
            self.ui.cbSubject.addItems(lst)
            if 'subject' in self.Fields and self.Fields["subject"] in lst :
                idx = lst.index(self.Fields["subject"])                  
                self.ui.cbSubject.setCurrentIndex(idx)
            
            self.Subject = self.ui.cbSubject.currentText()
            self.ui.pbSubject.setEnabled(True)            
            self.ui.cbSubject.setEnabled(True)
            self.ui.cbSubject.currentIndexChanged.connect(self.selSubject)
            
            
            sql = 'SELECT stimulus FROM projects_stimulus WHERE project ="' + str(self.Project) + '"'
            strlst = self.mydb.query(sql) 
            lst = [i[0] for i in strlst]
            self.Stimuluslist = lst
            self.ui.cbStimulus.addItems(lst)
            if 'stimulus' in self.Fields and self.Fields["stimulus"] in lst :
                idx = lst.index(self.Fields["stimulus"])                  
                self.ui.cbStimulus.setCurrentIndex(idx)
                
            self.Stimulus = self.ui.cbStimulus.currentText()
            self.ui.cbStimulus.setEnabled(True) 
            self.ui.pbStimulus.setEnabled(True)
            self.ui.cbStimulus.currentIndexChanged.connect(self.selStimulus) 
            
            sql = 'SELECT setupid FROM setups'
            strlst = self.mydb.query(sql) 
            lst = [i[0] for i in strlst]
            self.Setuplist = lst
            self.ui.cbSetup.addItems(lst)
            if 'setup' in self.Fields and self.Fields["setup"] in lst :
                idx = lst.index(self.Fields["setup"])                  
                self.ui.cbSetup.setCurrentIndex(idx)
                
            self.ui.cbSetup.setEnabled(True)
            self.Setup = self.ui.cbSetup.currentText()           
            self.ui.cbSetup.setEnabled(True)
            self.ui.pbSetup.setEnabled(True)
            self.ui.cbSetup.currentIndexChanged.connect(self.selSetup) 

            sql = 'SELECT investigatorid FROM investigator'
            strlst = self.mydb.query(sql) 
            lst = [i[0] for i in strlst]
            self.Investlist = lst
            self.ui.cbInvestigator.addItems(lst)
            if 'investigator' in self.Fields and self.Fields["investigator"] in lst :
                idx = lst.index(self.Fields["investigator"])                  
                self.ui.cbInvestigator.setCurrentIndex(idx)
                
            self.Investigator = self.ui.cbInvestigator.currentText()
            self.ui.cbInvestigator.setEnabled(True)
            self.ui.pbInvestigator.setEnabled(True)
            self.ui.cbInvestigator.currentIndexChanged.connect(self.selInvestigator)
       

    def fillDataset(self): 
        sql = 'SELECT datasetid, idx FROM datasets WHERE project ="' + str(self.Project) + '"'
        strlst  = self.mydb.query(sql) 
        lst = [i[0] for i in strlst]
        self.ui.cbDataset.disconnect()
        self.ui.cbDataset.clear()
        self.Datasets = []
        if len(lst) > 0 :
            self.ui.cbDataset.addItems(lst)
            self.Datasets = lst
            self.Dataset = self.ui.cbDataset.currentText()
            self.DatasetId = strlst[0][1]           
            self.ui.pbCondition.setEnabled(True)
             
        self.fillCondition()
        self.ui.cbDataset.currentIndexChanged.connect(self.selDataset)
               
    def fillSubject(self): 
        sql = 'SELECT subject FROM projects_subjects WHERE project ="' + str(self.Project) + '"'
        strlst = self.mydb.query(sql) 
        lst = [i[0] for i in strlst]
        self.Subjectlist = lst;
        self.ui.cbSubject.disconnect()
        self.ui.cbSubject.clear() 
        self.ui.cbSubject.addItems(lst) 
        self.Subject = self.ui.cbSubject.currentText() 
        
        self.ui.cbSubject.currentIndexChanged.connect(self.selSubject)   
        
    def fillCondition(self):
        self.Conditionlist = []
        self.ui.cbCondition.disconnect()
        self.ui.cbCondition.clear() 
        if hasattr(self, 'Dataset'):
            sql = 'SELECT conditionid FROM conditions WHERE dataset ="' + str(self.Dataset) +  \
                  '" AND project = "' + str(self.Project) + '"'
                
            strlst = self.mydb.query(sql)
            lst = [i[0] for i in strlst]
            
            self.Conditionlist = lst;

            self.ui.cbCondition.addItems(lst)
            self.Condition = self.ui.cbCondition.currentText()
        
        self.ui.cbCondition.currentIndexChanged.connect(self.selCondition) 
               
    def fillStimulus(self): 
        sql = 'SELECT stimulus FROM projects_stimulus WHERE project ="' + str(self.Project) + '"'
        strlst = self.mydb.query(sql) 
        lst = [i[0] for i in strlst]
        self.Stimuluslist = lst
        self.ui.cbStimulus.disconnect() 
        self.ui.cbStimulus.clear() 
        self.ui.cbStimulus.addItems(lst)
        self.ui.cbStimulus.setEnabled(True) 
        self.Stimulus = self.ui.cbStimulus.currentText()
        self.ui.cbStimulus.currentIndexChanged.connect(self.selStimulus) 
 
    def fillSetup(self): 
        sql = 'SELECT setupid FROM setups'
        strlst = self.mydb.query(sql) 
        lst = [i[0] for i in strlst]
        self.Setuplist = lst
        
        self.ui.cbSetup.disconnect()
        self.ui.cbSetup.clear() 
        self.ui.cbSetup.addItems(lst)

        self.ui.cbSetup.setEnabled(True)
        self.Setup = self.ui.cbSetup.currentText()
        self.ui.cbSetup.currentIndexChanged.connect(self.selSetup) 
        
    def fillInvestigator(self):
        sql = 'SELECT investigatorid FROM investigator'
        strlst = self.mydb.query(sql) 
        lst = [i[0] for i in strlst]
        self.Investlist = lst
        
        self.ui.cbInvestigator.disconnect()
        self.ui.cbInvestigator.clear() 
        self.ui.cbInvestigator.addItems(lst)

        self.ui.cbInvestigator.setEnabled(True)
        self.Investigator = self.ui.cbInvestigator.currentText()
        self.ui.cbInvestigator.currentIndexChanged.connect(self.selInvestigator)        
        
    def selchangeProj(self, i):    
        indx = self.ui.cbProject.currentIndex()
        if( indx > 0 ):
            self.Project =  self.ui.cbProject.currentText()
            sql = 'SELECT idx FROM projects WHERE projectid = "' + self.Project + '"'
            strlst = self.mydb.query(sql)
            self.ProjId = strlst[0][0]
            self.FillFields()
        else:
            self.ui.cbDataset.disconnect()
            self.ui.cbDataset.clear()
            self.ui.cbDataset.currentIndexChanged.connect(self.selDataset)
            self.ui.cbSubject.disconnect()
            self.ui.cbSubject.clear()
            self.ui.cbSubject.currentIndexChanged.connect(self.selSubject)
            self.ui.cbCondition.disconnect()
            self.ui.cbCondition.clear()
            self.ui.cbCondition.currentIndexChanged.connect(self.selCondition)
            self.ui.cbStimulus.disconnect() 
            self.ui.cbStimulus.clear() 
            self.ui.cbStimulus.currentIndexChanged.connect(self.selStimulus)
            self.ui.pbDataset.setEnabled(False)
            self.ui.pbCondition.setEnabled(False)
            self.ui.pbSubject.setEnabled(False)  
            self.ui.pbStimulus.setEnabled(False)
            
 
    def FillFields(self):
        self.ui.pbCondition.setEnabled(False)
        
        self.fillDataset()
        self.fillSubject()
       # self.fillCondition()
        self.fillSetup()
        self.fillStimulus()
        self.fillInvestigator()
        self.NwID()            

        self.ui.pbDataset.setEnabled(True)
        self.ui.pbSubject.setEnabled(True)  
        self.ui.pbStimulus.setEnabled(True)
        
        if self.bOnce : #enable the first time
            self.ui.cbDataset.setEnabled(True)
            self.ui.cbCondition.setEnabled(True)         
            self.ui.cbSubject.setEnabled(True) 
            self.ui.cbSetup.setEnabled(True)
            self.ui.pbSetup.setEnabled(True)
            self.ui.cbStimulus.setEnabled(True) 
            self.ui.pbInvestigator.setEnabled(True)
            self.bOnce = False
       # print(self.ui.cbProject.currentText()) 
         
    def selDataset(self, i): 
        self.Dataset = self.ui.cbDataset.currentText() 
        sql = 'SELECT idx FROM datasets WHERE datasetid = "' + self.Dataset + '"'
        strlst = self.mydb.query(sql)
        self.DatasetId = strlst[0][0]         
        self.fillCondition()
        self.ui.pbCondition.setEnabled(True)
               
    def selSubject(self, i): 
        self.Subject = self.ui.cbSubject.currentText()
        self.NwID()
   
    def selCondition(self, i): 
        self.Condition = self.ui.cbCondition.currentText()       

    def selStimulus(self, i): 
        self.Stimulus = self.ui.cbStimulus.currentText()
 #       print(self.Stimulus)
#        wait = input("Press Enter to continue.")
 
    def selSetup(self, i): 
        self.Setup = self.ui.cbSetup.currentText()
        
    def selInvestigator(self,i):
        self.Investigator = self.ui.cbInvestigator.currentText()

    def Checkinput(self, field, val ):
        if ( len(val) > 0 ):   
            self.Fields[field] = val;
            return True
        else:          
            res = QMessageBox.question(self,"ERROR:Empty field: "+field , "Please enter a value for this field!!", QMessageBox.Ok)
            return False
        
   
    
    def Save(self):

        if ( not self.Checkinput("project", self.Project) ):
            return;
        if ( not self.Checkinput("dataset", self.Dataset) ):
            return;
        if ( not self.Checkinput("condition", self.Condition) ):
            return;
        if ( not self.Checkinput("subject", self.Subject) ):
            return;
        if ( not self.Checkinput("stimulus",  self.Stimulus) ):
            return;
        if ( not self.Checkinput("setup", self.Setup) ):
            return;
        if ( not self.Checkinput("investigator", self.Investigator) ):
            return;

        self.Fields["date"] = self.ui.dateEdit.date().toString("yyyy-MM-dd")
        self.Fields["logfile"] = self.ui.ed_Log.text()
        self.Fields["version"] = '1.0'
        self.ID = self.ui.ed_ID.text()

        self.dirPath = QtWidgets.QFileDialog.getExistingDirectory(self,"Choose Directory", self.dirPath )
        strpath = self.dirPath+'\\'+self.ID+'_session.json'
        FP = open(strpath, 'w')
        json.dump(self.Fields, FP)
        FP.close()
        
    def Done(self):  
        self.Fields["project"] = self.Project
        self.Fields["dataset"] = self.Dataset
        self.Fields["condition"]   = self.Condition
        self.Fields["subject"] = self.Subject
        self.Fields["stimulus"] = self.Stimulus
        self.Fields["setup"]    = self.Setup
        self.Fields["investigator"] = self.Investigator

        self.Fields["date"] = self.ui.dateEdit.date().toString("yyyy-MM-dd");        
        self.Fields["logfile"] = self.ui.ed_Log.text()
        self.Fields["version"] = '1.0'
        self.ID = self.ui.ed_ID.text()
        self.Sessnr = self.ui.spinSessnr.value()
        self.Ret = 0
        self.mydb.close()
        self.close()
         
    def Cancelled(self):
        self.Ret = 1
        self.mydb.close()
        self.close()
        
#w.mydb.reopen()
#w.mydb.update(sql)
    def Reconnect(self):
        if self.mydb.connected() == False :
           self.mydb.reopen() 
                
    def NwProject(self):
        dlg = dlgNew([]) 
        dlg.ui.label.setText("NEW : project")
        dlg.ui.cbAll.setVisible(False)
        dlg.show()
        dlg.exec()
        
        strRes = dlg.ui.Ed_Id.text()
        strDescr = dlg.ui.Ed_Descr.text()
        
        if dlg.Ret == 0 : #accepted , 1 = canceled
            if strRes in self.Projects:
                print("Project already exists!!")
                
            elif len(strRes) > 0 :
                print('Adding to table projects')
                try:
                    sql = "INSERT INTO projects ( projectid, shortdescr ) VALUES ( '" + strRes + "', '"  + strDescr + "' )"
#                    self.mydb.reopen()
                    self.mydb.update(sql)
                                       
                    self.ui.cbProject.addItem(strRes)
                    self.ui.cbProject.setCurrentText(strRes)
#                    self.mydb.close()
                    
                except mysql.connector.Error as e:
                    print('failed to add new project : '+ e.msg)  
                    

    def NwDataset(self):
        dlg = dlgNew([]) 
        dlg.ui.label.setText("NEW : dataset")
        dlg.ui.cbAll.setVisible(False)
        dlg.show()
        dlg.exec()
        strRes = dlg.ui.Ed_Id.text()
        strDescr = dlg.ui.Ed_Descr.text()
        
        if dlg.Ret == 0 : #accepted , 1 = canceled
            if strRes in self.Datasets:
                print("Dataset already exists!!")
                
            elif len(strRes) > 0 :
                print('Adding to table datasets')
                try:
                    sql = "INSERT INTO datasets ( datasetid, project, projectidx, shortdescr ) VALUES ( '" \
                           + strRes + "' , '" + self.Project + "', '" + str(self.ProjId) + "', '" + strDescr + "' )"
                    self.mydb.update(sql)

                    #add default condition when creating new dataset
                    sql = "INSERT INTO conditions( conditionid, dataset, project, shortdescr ) VALUES ( 'none', " \
                           + "'" + strRes + "', '" + self.Project + "', '" + strDescr + "' )"

                    self.mydb.update(sql)                  
                    self.Datasets.append( strRes )                  
                    self.ui.cbDataset.addItem(strRes)
                    self.ui.cbDataset.setCurrentText(strRes)
                    
                except mysql.connector.Error as e:
                    print('failed to add new dataset : '+ e.msg)  

    def NwCondition(self):
        dlg = dlgNew([])        
        dlg.ui.label.setText("NEW : condition")
        dlg.ui.cbAll.setVisible(False)      
        dlg.show()
        dlg.exec()
        
        if dlg.Ret == 0 : #accepted , 1 = canceled
            strRes = dlg.ui.Ed_Id.text()
            strDescr = dlg.ui.Ed_Descr.text()
            
            if strRes in self.Conditionlist :
                print("Condition already exists!!")
                
            elif len(strRes) > 0 :
                print('Adding to table conditions')
                try:
                    sql = "INSERT INTO conditions( conditionid, dataset, project, shortdescr ) VALUES ( '" + strRes \
                           + "', '" + self.Dataset + "', '" + self.Project + "', '" + strDescr + "' )"

                    self.mydb.update(sql)
                    self.Conditionlist.append(strRes)                  
                    self.ui.cbCondition.addItem(strRes)
                    self.ui.cbCondition.setCurrentText(strRes)
                    
                except  mysql.connector.Error as e:
                    print('failed to add new condition : '+ e.msg )  


    def NwSubject(self):

        sql = 'SELECT subjectid FROM subjects' 
        strlst = self.mydb.query(sql)
        Allist = [i[0] for i in strlst]

        dlg = dlgNew(Allist) 
        dlg.ui.label.setText("NEW : subject")       
        dlg.ui.cbAll.setEnabled(True)
        dlg.ui.cbSpecies.setVisible(True)
        dlg.ui.label_sex.setVisible(True)
        dlg.ui.cbSex.setVisible(True)
        dlg.ui.label_genotype.setVisible(True)
        dlg.ui.Ed_Genotyp.setVisible(True)
        dlg.show()
        dlg.exec()
        
        if dlg.Ret == 0 : #accepted , 1 = canceled
            strRes = dlg.ui.Ed_Id.text()
            strDescr = dlg.ui.Ed_Descr.text()
            strSpecies = dlg.ui.cbSpecies.currentText()
            strSex = dlg.ui.cbSex.currentText()
            strGenotype = dlg.ui.Ed_Genotyp.text()
            
            if strRes in self.Subjectlist:
                print('Subject already exists, choose different name!')
                
            elif len(strRes) > 0 :
                if strRes not in Allist:
                    print('Adding to table subjects')
                    try:
                        sql = 'INSERT INTO subjects( subjectid, shortdescr, species, sex, genotype ) VALUES ( "' + strRes \
                              + '", "' + strDescr + '", "' + strSpecies + '", "' + strSex + '", "' + strGenotype + '")'
                        self.mydb.update(sql)
                        
                    except mysql.connector.Error as e:
                        print('failed to add new subject : '+ e.msg)                       
                        
                        
                sql = 'INSERT INTO projects_subjects(project, projectidx, subject, subjectidx ) VALUES ' \
                     '( "' + self.Project + '", "' + str(self.ProjId) + '", "' + strRes  \
                     + '", (SELECT idx FROM subjects WHERE subjectid = "' + strRes + '" )  )'                
                self.mydb.update(sql)
                
                self.Subjectlist.append(strRes)                                           
                self.ui.cbSubject.addItem(strRes)
                self.ui.cbSubject.setCurrentText(strRes)
                                    
                
    def NwSetup(self):
        dlg = dlgNew([]) 
        dlg.ui.label.setText("NEW : setup")
        dlg.ui.cbAll.setVisible(False)
        dlg.show()
        dlg.exec()
          
        if dlg.Ret == 0 : #accepted , 1 = canceled
            strRes = dlg.ui.Ed_Id.text()
            strDescr = dlg.ui.Ed_Descr.text()
            
            if strRes in self.Setuplist:
                print("setup already exists!!")
                
            elif len(strRes) > 0 :
                print('Adding to table setups')
                try:
                    sql = 'INSERT INTO setups( setupid, shortdescr ) VALUES ( "' + strRes + '", ' + strDescr + '")'
                    self.mydb.update(sql)

                    self.Setuplist.append(strRes)                       
                    self.ui.cbSetup.addItem(strRes)
                    self.ui.cbSetup.setCurrentText(strRes)
                 
                except mysql.connector.Error as e:
                    print('failed to add new setup : '+ e.msg) 
                    
                    
        
    def NwStimulus(self):

        sql = 'SELECT stimulusid FROM stimulus' 
        strlst = self.mydb.query(sql)
        Allist = [i[0] for i in strlst]
        
        dlg = dlgNew(Allist) 
        dlg.ui.label.setText("NEW : stimulus")                        
        dlg.ui.cbAll.setEnabled(True)              
        dlg.show()
        dlg.exec()
        
        if dlg.Ret == 0 : #accepted , 1 = canceled
            strRes = dlg.ui.Ed_Id.text()
            strDescr = dlg.ui.Ed_Descr.text()
            
            if strRes in self.Stimuluslist :
                print("Stimulus already exists!!")
                
            elif len(strRes) > 0 :
                if strRes not in Allist:
                    print('Adding to table stimulus')
                    try:
                        sql = 'INSERT INTO stimulus( stimulusid, shortdescr ) VALUES ( "' + strRes + '", ' + strDescr + '" )'
                        self.mydb.update(sql)
                        
                    except  mysql.connector.Error as e:
                        print('failed to add new Stimulus : '+ e.msg )  
                
    
                sql = 'INSERT INTO projects_stimulus(project, projectidx, stimulus, stimulusidx ) VALUES ' \
                     '( "' + self.Project + '", "' + str(self.ProjId) + '", "' + strRes  \
                     + '", (SELECT idx FROM stimulus WHERE stimulusid = "' + strRes + '" )  )'
                  
                self.mydb.update(sql)      
                self.Stimuluslist.append(strRes)               
                self.ui.cbStimulus.addItem(strRes)
                self.ui.cbStimulus.setCurrentText(strRes)


    def NwInvestigator(self):
        dlg = dlgNew([]) 
        dlg.ui.label.setText("NEW : investigator")
        dlg.ui.cbAll.setVisible(False)
        dlg.ui.label_shortdescr.setVisible(False)
        dlg.ui.Ed_Descr.setVisible(False)
        dlg.show()
        dlg.exec()
                
        if dlg.Ret == 0 : #accepted , 1 = canceled
            strRes = dlg.ui.Ed_Id.text()    
            if strRes in self.Investlist:
                print("Investigator already exists!!")
                
            elif len(strRes) > 0 :
                print('Adding to table investigator')
                try:
                    sql = 'INSERT INTO investigator( investigatorid) VALUES ( "' + strRes + '")'
                    self.mydb.update(sql)
                    self.Investlist.append(strRes)    
                     
                    self.ui.cbInvestigator.addItem(strRes)
                    self.ui.cbInvestigator.setCurrentText(strRes)
               
                except mysql.connector.Error as e:
                    print('failed to add new investigator : '+ e.msg)      

    def NwSessnr(self):
        self.NwID()

    def NwID(self):
        strdate = self.ui.dateEdit.date().toString("yyyy-MM-dd");
        sessnr =  str(self.ui.spinSessnr.value()).zfill(3);
        self.ui.ed_ID.setText( self.Subject + "_" + strdate + "_" + sessnr )
        self.ui.ed_Log.setText( self.Subject + "_" + strdate + "_" + sessnr + '_log')
        # print(strdate)
        
#def main():
#    app = QtWidgets.QApplication([]) 
#    w = dlgFields()  
#    w.show() 
#    #sys.exit(app.exec_())    
#    app.exec()
#    
#if __name__ == '__main__':
#    main()

# self.connect(button3, SIGNAL("clicked()"), lambda who="Three": self.anyButton(who))
