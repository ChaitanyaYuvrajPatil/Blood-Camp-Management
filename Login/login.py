from index import main_1
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys
import smtplib
import mysql.connector as mc
from PyQt5.uic import loadUiType
import urllib.request
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5 import QtCore, QtGui, QtWidgets
import os
from os import path
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from pyqt5_plugins.examplebutton import QtWidgets

ui1,_ = loadUiType('Login.ui')

class MainApp(QWidget , ui1):
    def __init__(self , parent=None):
        super(MainApp , self).__init__(parent)
        QWidget.__init__(self)
        self.setupUi(self)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.InitUI()
        self.Handel_Buttons()

    def InitUI(self):
        pass
        ## contain all ui changes in loading
        self.tabWidget.tabBar().setVisible(False)

    def Handel_Buttons(self):
        pass
        ########### Close minimize ###############
        #pushButton_close
        self.pushButton_close.clicked.connect(self.close) #showMinimized  pushButton_minimize
        self.pushButton_minimize.clicked.connect(self.showMinimized)
        ## handel all buttons in the app

        self.btn_login_1.clicked.connect(self.Open_Login)
        self.register_btn_1.clicked.connect(self.Open_Register)
        self.btn_login_2.clicked.connect(self.Admin_Login)
        self.register_btn_2.clicked.connect(self.Open_Register)
        #self.pushButton_3.clicked.connect(self.Open_Volunteer)
        #self.pushButton_4.clicked.connect(self.Open_Approval)
###### UI CHanges Methods

    def Open_Login(self):
        self.tabWidget.setCurrentIndex(0)
        #self.buttun_style('Home')
    def Open_Register(self):
        self.tabWidget.setCurrentIndex(1)

    def Admin_Login(self):
        id = self.getName_admin.text()
        password = self.get_password.text()

        if id == 'Ram' and password == 'Sita':
            try:
                pass
                #main_1()
                #exec(open(r'C:\Users\mypc\PycharmProjects\Blood Camp Management\index.py').read())
            except Exception as e:
                print(e)
            #main_1()
            #os.system('python index.py')
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)

            msg.setText("Not Successfull")
            msg.setInformativeText("Please Check your ID or Password")
            msg.setWindowTitle("Error")
            msg.setDetailedText("")
            msg.exec_()


def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()