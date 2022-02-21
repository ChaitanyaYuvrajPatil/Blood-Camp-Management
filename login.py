
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

ui1,_ = loadUiType('Login_1.ui')

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
        self.register_btn_2.clicked.connect(self.volunteer_Register)
        #self.pushButton_3.clicked.connect(self.Open_Volunteer)
        #self.pushButton_4.clicked.connect(self.Open_Approval)

        ########################### Send Mail ######################################

    def send_mail(self, rec_mail, decision):
            if decision == 'approve':
                mail_content = "Hello Sir/mam, Your your request for being volunteer in blood Donation Camp is accepted.Accept"
            else:
                mail_content = "Hello Sir/mam, Your your request for being volunteer in blood Donation Camp is rejected,Reject"

            # The mail addresses and password
            sender_address = 'cpatil27112001@gmail.com'
            sender_pass = 'Monu@123'
            receiver_address = rec_mail
            # Setup the MIME
            message = MIMEMultipart()
            message['From'] = sender_address
            message['To'] = receiver_address
            message['Subject'] = 'About volunteer selection in blood donation camp.'  # The subject line
            # The body and the attachments for the mail
            message.attach(MIMEText(mail_content, 'plain'))
            # Create SMTP session for sending the mail
            session = smtplib.SMTP('smtp.gmail.com', 587)  # use gmail with port
            session.starttls()  # enable security
            session.login(sender_address, sender_pass)  # login with mail_id and password
            text = message.as_string()
            session.sendmail(sender_address, receiver_address, text)
            session.quit()
            print('Mail Sent')

        ##########################################################################
###### UI CHanges Methods

    def Open_Login(self):
        self.buttun_style('login')
        self.tabWidget.setCurrentIndex(0)
        #self.buttun_style('Home')
    def Open_Register(self):
        self.buttun_style('register')
        self.tabWidget.setCurrentIndex(1)

    def Admin_Login(self):
        id = self.getName_admin.text()
        password = self.get_password.text()

        if id == 'Ram' and password == 'Sita':
            try:
                self.close()
                os.system('python index.py')
                #self.close()
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

    def volunteer_Register(self):
        name = self.getName_reg.text()
        sirname = self.getSirname_reg.text()
        mobile = self.getMobile_reg.text()
        gmail = self.getGmail_reg.text()
        id = self.getID_reg.text()
        gender = self.Gender_reg.currentText()
        address = self.getAdress_reg.toPlainText()
        #print(name, sirname, mobile)

        if str(name) == '' or str(sirname) == '' or str(mobile) == '' or str(gmail) == '' or str(id) == '' or str(address) == '':
            print(name + " " + sirname + " " + gender + " " + address)
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("You Fill Incomplete details")
            msg.setInformativeText("")
            msg.setWindowTitle("Error")
            msg.setDetailedText("Please fill all details")
            msg.exec_()

        else:

            try:
                mydb = mc.connect(
                    host="localhost",
                    user='root',
                    password='Lucifer@123',
                    database='blood_camp'
                )

                mycursor = mydb.cursor()
                query = """INSERT INTO blood_camp.approval_data (Name,Sirname,Mobile,Gmail,ID,Gender,Address) VALUES (%s, %s, %s, %s, %s, %s, %s)"""
                value = (name, sirname, mobile, gmail, id, gender, address)

                mycursor.execute(query, value)
                mydb.commit()
                mycursor.close()
                mydb.close()

                '''try:
                    mydb = mc.connect(
                        host="localhost",
                        user='root',
                        password='Lucifer@123',
                        database='blood_camp'
                    )

                    mycursor = mydb.cursor()
                    query = "DELETE FROM blood_camp.blood_camp.volunteer_data WHERE ID = %s"
                    mycursor.execute(query, (str(id),))  # ,ad
                    print("dfe")
                    mydb.commit()
                    mycursor.close()
                    mydb.close()


                except mc.Error as e:
                    print(e)'''

                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)

                msg.setText("Your data is sended to Admin wait up to approval")
                msg.setInformativeText("")
                msg.setWindowTitle("Message")
                msg.setDetailedText("Wait up to approval.Admin will send gmail to you")
                msg.exec_()

                from sendmail import send_mail_
                send_mail_(str(gmail))

            except mc.Error as e:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)

                msg.setText("Not Successfull")
                msg.setInformativeText("ID is repeated")
                msg.setWindowTitle("Error")
                msg.setDetailedText(str(e))
                retval = msg.exec_()
                print("value of pressed message box button:", retval)
                print(e)

    def buttun_style(self, num):
            if num == 'login':
                light_1 = '#60FF42'
                light_2 = '#1DB700'
            elif num == 'register':
                light_1 = '#1DB700'
                light_2 = '#60FF42'

            self.btn_login_1.setStyleSheet("background-color:" + light_1 + ";"
            "border: none;"
            "border-radius: 0px;"
            #"border-left: 2px solid black;"
            )
            self.register_btn_1.setStyleSheet("background-color:" + light_2 + ";"
                                                                              "border: none;"
                                                                              "border-radius: 0px;"
                                                                              "border-left: 2px solid black;"
                                              )



def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()