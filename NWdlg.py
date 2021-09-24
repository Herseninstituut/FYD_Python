# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'NWdlg.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(365, 317)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        Dialog.setFont(font)
        Dialog.setWindowOpacity(1.0)
        self.Ed_Id = QtWidgets.QLineEdit(Dialog)
        self.Ed_Id.setGeometry(QtCore.QRect(99, 50, 111, 25))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.Ed_Id.setFont(font)
        self.Ed_Id.setObjectName("Ed_Id")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(20, 20, 230, 20))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.cbAll = QtWidgets.QComboBox(Dialog)
        self.cbAll.setEnabled(False)
        self.cbAll.setGeometry(QtCore.QRect(230, 50, 121, 25))
        self.cbAll.setFrame(True)
        self.cbAll.setObjectName("cbAll")
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(250, 280, 101, 23))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.buttonBox.setFont(font)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.label_title = QtWidgets.QLabel(Dialog)
        self.label_title.setGeometry(QtCore.QRect(20, 50, 81, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_title.setFont(font)
        self.label_title.setObjectName("label_title")
        self.label_shortdescr = QtWidgets.QLabel(Dialog)
        self.label_shortdescr.setGeometry(QtCore.QRect(20, 90, 81, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_shortdescr.setFont(font)
        self.label_shortdescr.setObjectName("label_shortdescr")
        self.label_species = QtWidgets.QLabel(Dialog)
        self.label_species.setGeometry(QtCore.QRect(20, 191, 61, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_species.setFont(font)
        self.label_species.setObjectName("label_species")
        self.cbSpecies = QtWidgets.QComboBox(Dialog)
        self.cbSpecies.setEnabled(True)
        self.cbSpecies.setGeometry(QtCore.QRect(80, 191, 91, 22))
        self.cbSpecies.setCurrentText("")
        self.cbSpecies.setObjectName("cbSpecies")
        self.label_sex = QtWidgets.QLabel(Dialog)
        self.label_sex.setGeometry(QtCore.QRect(210, 191, 41, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_sex.setFont(font)
        self.label_sex.setObjectName("label_sex")
        self.cbSex = QtWidgets.QComboBox(Dialog)
        self.cbSex.setGeometry(QtCore.QRect(240, 191, 51, 22))
        self.cbSex.setObjectName("cbSex")
        self.label_genotype = QtWidgets.QLabel(Dialog)
        self.label_genotype.setGeometry(QtCore.QRect(20, 241, 71, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_genotype.setFont(font)
        self.label_genotype.setObjectName("label_genotype")
        self.Ed_Genotyp = QtWidgets.QLineEdit(Dialog)
        self.Ed_Genotyp.setGeometry(QtCore.QRect(90, 240, 81, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.Ed_Genotyp.setFont(font)
        self.Ed_Genotyp.setObjectName("Ed_Genotyp")
        self.label_Age = QtWidgets.QLabel(Dialog)
        self.label_Age.setGeometry(QtCore.QRect(210, 240, 41, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_Age.setFont(font)
        self.label_Age.setObjectName("label_Age")
        self.Ed_Age = QtWidgets.QLineEdit(Dialog)
        self.Ed_Age.setGeometry(QtCore.QRect(240, 240, 61, 25))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.Ed_Age.setFont(font)
        self.Ed_Age.setObjectName("Ed_Age")
        self.Ed_Descr = QtWidgets.QTextEdit(Dialog)
        self.Ed_Descr.setGeometry(QtCore.QRect(100, 100, 251, 71))
        self.Ed_Descr.setObjectName("Ed_Descr")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog Enter new value"))
        self.label.setText(_translate("Dialog", "NEW         : "))
        self.label_title.setText(_translate("Dialog", "Id(name)"))
        self.label_shortdescr.setText(_translate("Dialog", "Shortdescr"))
        self.label_species.setText(_translate("Dialog", "Species"))
        self.label_sex.setText(_translate("Dialog", "Sex"))
        self.label_genotype.setText(_translate("Dialog", "Genotype"))
        self.Ed_Genotyp.setText(_translate("Dialog", "none"))
        self.label_Age.setText(_translate("Dialog", "Age"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
