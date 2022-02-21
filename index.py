
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


############################################################







################################################################

ui,_ = loadUiType('main.ui') #

class MainApp(QWidget ,ui):
    def __init__(self , parent=None):
        super(MainApp , self).__init__(parent)
        QWidget.__init__(self)
        self.setupUi(self)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.InitUI()
        self.Handel_Buttons()
        self.db_to_table_doner()
        self.db_to_table_volunteer()
        self.db_to_table_approval()
        self.total_blood_count()
        self.db_to_table_volunteer_certificate()


    def InitUI(self):
        ## contain all ui changes in loading
        self.tabWidget.tabBar().setVisible(False)
        ## ################# Doner ##################
        self.tableWidget.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.tableWidget.selectionModel().selectionChanged.connect(self.on_selection_changed_doner)

        ## ################# Volunteer ##################
        self.tableWidget_v.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.tableWidget_v.selectionModel().selectionChanged.connect(self.on_selection_changed_volunteer)

        ## ################# Aproval ##################
        self.tableWidget_a.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.tableWidget_a.selectionModel().selectionChanged.connect(self.on_selection_changed_approval)

        ## ################# Vol_Certificate ##################
        self.tableWidget_vol_c.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.tableWidget_vol_c.selectionModel().selectionChanged.connect(self.on_selection_changed_vol_certificate)

    def on_selection_changed_doner(self,selected,deselected):
            for ix in selected.indexes():
                    print('Selected row : {0}'.format(ix.row()))
            self.selected_row = int(ix.row())
            self.get_row_data(int(ix.row()))

    def on_selection_changed_volunteer(self,selected,deselected):
            for ix in selected.indexes():
                    print('Selected row : {0}'.format(ix.row()))
            self.selected_row = int(ix.row())
            self.get_row_data_volunteer(int(ix.row()))

    def on_selection_changed_approval(self,selected,deselected):
            for ix in selected.indexes():
                    print('Selected row : {0}'.format(ix.row()))
            self.selected_row = int(ix.row())
            self.get_row_data_approval(int(ix.row()))

    def on_selection_changed_vol_certificate(self,selected,deselected):
            for ix in selected.indexes():
                    print('Selected row : {0}'.format(ix.row()))
            self.selected_row = int(ix.row())
            self.get_row_data_vol_certificate(int(ix.row()))


    def Handel_Buttons(self):
        ########### Close minimize ###############
        #pushButton_close
        self.pushButton_close.clicked.connect(self.close) #showMinimized  pushButton_minimize
        self.pushButton_minimize.clicked.connect(self.showMinimized)
        ## handel all buttons in the app

        self.pushButton.clicked.connect(self.Open_Home)
        self.pushButton_2.clicked.connect(self.Open_Doner)
        self.pushButton_3.clicked.connect(self.Open_Volunteer)
        self.pushButton_4.clicked.connect(self.Open_Approval)
        self.pushButton_5.clicked.connect(self.Open_Certificate)

        ############# Doner################
        self.add_btn.clicked.connect(self.insert_data_doner)
        self.update_btn.clicked.connect(self.update_row_doner)
        self.delete_btn.clicked.connect(self.delete_row_doner)
        self.reset_btn.clicked.connect(self.reset_fun_doner)
        self.search_btn.clicked.connect(self.searchby_doner)

        ############# Volunteer ################
        self.add_btn_2.clicked.connect(self.insert_data_Volunteer)
        self.update_btn_2.clicked.connect(self.update_row_volunteer)
        self.delete_btn_2.clicked.connect(self.delete_row_volunteer)
        self.reset_btn_2.clicked.connect(self.reset_volunteer)
        self.search_btn_2.clicked.connect(self.searchby_volunteer)

        ############# Approval ################
        self.aprove_btn.clicked.connect(self.volunteer_approval)
        self.decline_btn.clicked.connect(self.volunteer_decline)
        self.search_btn_3.clicked.connect(self.searchby_approval)

        ############# volunteer Certificates ################
        self.send_btn.clicked.connect(self.send_certificate)
        self.print_btn.clicked.connect(self.print_certificate)
        #self.search_btn_3.clicked.connect(self.searchby_approval)

    ################################################
    ###### UI CHanges Methods

    def Open_Home(self):
        self.tabWidget.setCurrentIndex(0)
        self.buttun_style('Home')
    def Open_Doner(self):
        self.tabWidget.setCurrentIndex(1)
        self.buttun_style('Doner')
        #self.pushButton_2.setStyleSheet('background-color:#60FF42;')

    def Open_Volunteer(self):
        self.tabWidget.setCurrentIndex(2)
        self.buttun_style('Volunteer')

    def Open_Approval(self):
        self.tabWidget.setCurrentIndex(3)
        self.buttun_style('Approval')

    def Open_Certificate(self):
        self.tabWidget.setCurrentIndex(4)
        self.buttun_style('Certificate')

    ########################### Send Mail ######################################

    def send_mail(self,rec_mail,decision):
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
    ######################### Blood Count ####################################

    def total_blood_count(self):
        try:
            mydb = mc.connect(
                host="localhost",
                user='root',
                password='Lucifer@123',
                database='blood_camp'
            )

            total_A1 = 0
            total_A2 = 0
            total_B1 = 0
            total_B2 = 0
            total_AB1 = 0
            total_AB2 = 0
            total_O1 = 0
            total_O2 = 0
            mycursor = mydb.cursor()
            table_name = 'doner_data'
            mycursor.execute("SELECT Blood_Group,Blood_Donated FROM {}".format(table_name))
            result = mycursor.fetchall()

            for item in result:
                if item[0] == 'A+':
                    total_A1 = total_A1 + int(item[1])
                if item[0] == 'A-':
                    total_A1 = total_A2 + int(item[1])
                if item[0] == 'B+':
                    total_B1 = total_B1 + int(item[1])
                if item[0] == 'B-':
                    total_B2 = total_B2 + int(item[1])
                if item[0] == 'AB+':
                    total_AB1 = total_AB1 + int(item[1])
                if item[0] == 'AB-':
                    total_AB2 = total_AB2 + int(item[1])
                if item[0] == 'O+':
                    total_O1 = total_O1 + int(item[1])
                if item[0] == 'O-':
                    total_O2 = total_O2 + int(item[1])

            print(total_A1)
            self.label_A1.setText('               A+ : '+str(total_A1/1000)+'L')
            self.label_A2.setText('               A- : ' + str(total_A2 / 1000) + 'L')
            self.label_B1.setText('               B+ : ' + str(total_B1 / 1000) + 'L')
            self.label_B2.setText('               B- : ' + str(total_B2 / 1000) + 'L')
            self.label_AB1.setText('               AB+ : ' + str(total_AB1 / 1000) + 'L')
            self.label_AB2.setText('               AB- : ' + str(total_AB2 / 1000) + 'L')
            self.label_O1.setText('               O+ : ' + str(total_O1 / 1000) + 'L')
            self.label_O2.setText('               O- : ' + str(total_O2 / 1000) + 'L')

            mydb.commit()
            mycursor.close()
            mydb.close()
        except mc.Error as e:
            print(e)
            pass

    ############################################################################

    ########################### Donar Data Management ####################################

    def load(self):
        self.window = MainApp()
        self.close()
        self.window.show()

    def insert_data_doner(self):
        name = self.getName.text()
        sirname = self.getSirname.text()
        dob = self.getDOB.text()
        age = self.getAge.text()
        gender = self.Gender.currentText()
        id = self.getID.text()
        address = self.getAdress.toPlainText()
        blood_group = self.blood_group.currentText()
        blood_donated = self.blood_donated.text()

        print(name + " " + sirname + " " + gender + " " + address)
        if str(name) == '' or str(sirname) == '' or str(dob) == '' or str(age) == ''  or str(id) == ''or str(address) == ''or str(blood_group) == ''or str(blood_donated) == '':
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
                query = """INSERT INTO blood_camp.doner_data (Name,Sirname,DOB,Age,Gender,ID,Address,Blood_Group,Blood_Donated) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
                value = (name, sirname, dob,age,gender,id,address,blood_group,blood_donated)

                mycursor.execute(query, value)
                mydb.commit()
                mycursor.close()
                mydb.close()


                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)

                msg.setText("Your data is Successfully added")
                msg.setInformativeText("")
                msg.setWindowTitle("Message")
                msg.setDetailedText("Your data is successfully store in database")
                msg.exec_()
                self.load()
            except mc.Error as e:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)

                msg.setText("Not Successfull")
                msg.setInformativeText("Reg No is repeated")
                msg.setWindowTitle("Error")
                msg.setDetailedText(str(e))
                retval = msg.exec_()
                print("value of pressed message box button:", retval)
                print(e)

    def db_to_table_doner(self):
        try:
            mydb = mc.connect(
                host="localhost",
                user='root',
                password='Lucifer@123',
                database='blood_camp'
            )

            mycursor = mydb.cursor()
            table_name = 'doner_data'
            print("display 1")
            mycursor.execute("SELECT * FROM {}".format(table_name))
            print("display 2")
            result = mycursor.fetchall()
            print("display 3")
            #self.tableWidget.clear()
            self.tableWidget.setRowCount(0)
            #self.tableWidget.setRowCount(11)
            #self.tableWidget.setColumnCount(9)

            for row_number, row_data in enumerate(result):
                self.tableWidget.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.tableWidget.setItem(row_number, column_number, QTableWidgetItem(str(data)))

            print("display 4")

            mydb.commit()
            mycursor.close()
            mydb.close()
            #self.db_to_table_doner()
        except mc.Error as e:
            print(e)
            pass

    def get_row_data(self,ind):
            print('ahah')
            mydb = mc.connect(
                host="localhost",
                user='root',
                password='Lucifer@123',
                database='blood_camp'
            )

            mycursor = mydb.cursor()
            table_name = 'doner_data'
            mycursor.execute("SELECT * FROM {}".format(table_name))

            result = mycursor.fetchall()
            self.getName.setText(result[ind][0])
            self.getSirname.setText(result[ind][1])
            self.getDOB.setText(result[ind][2])
            self.getAge.setText(result[ind][3])
            self.Gender.setCurrentText(result[ind][4])
            self.getID.setText(result[ind][5])
            self.getAdress.setText(result[ind][6])
            self.blood_group.setCurrentText(result[ind][7])
            self.blood_donated.setText(result[ind][8])

            mydb.commit()
            mycursor.close()
            mydb.close()

    def update_row_doner(self):
        name = self.getName.text()
        sirname = self.getSirname.text()
        dob = self.getDOB.text()
        age = self.getAge.text()
        gender = self.Gender.currentText()
        id = self.getID.text()
        address = self.getAdress.toPlainText()
        blood_group = self.blood_group.currentText()
        blood_donated = self.blood_donated.text()

        try:
                    mydb = mc.connect(
                        host="localhost",
                        user='root',
                        password='Lucifer@123',
                        database='blood_camp'
                    )

                    mycursor = mydb.cursor()
                    query =  """UPDATE blood_camp.doner_data SET Name=%s, Sirname=%s,DOB=%s,Age=%s,Gender=%s,ID=%s,Address=%s,Blood_Group=%s,Blood_Donated=%s WHERE ID=%s"""
                    #Name,Sirname,DOB,Age,Gender,ID,Address,Blood_Group,Blood_Donated
                    mycursor.execute(query,(str(name),str(sirname),str(dob),str(age),str(gender),str(id),str(address),str(blood_group),str(blood_donated),str(id)))
                    mydb.commit()
                    mycursor.close()
                    mydb.close()

                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Information)

                    msg.setText("Your data is Successfully Updated")
                    msg.setInformativeText("")
                    msg.setWindowTitle("Message")
                    msg.setDetailedText("Your data is successfully updated in database")
                    msg.exec_()
                    self.load()

                    print("Updated")

        except mc.Error as e:
                    print(e)


    def delete_row_doner(self):
        id = self.getID.text()
        try:
                    print("delete")
                    mydb = mc.connect(
                        host="localhost",
                        user='root',
                        password='Lucifer@123',
                        database='blood_camp'
                    )

                    mycursor = mydb.cursor()
                    query = "DELETE FROM blood_camp.doner_data WHERE ID = %s"
                    mycursor.execute(query,(str(id),))  # ,ad
                    print("dfe")
                    mydb.commit()
                    mycursor.close()
                    mydb.close()

                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Information)

                    msg.setText("Your data is Successfully Deleted")
                    msg.setInformativeText("")
                    msg.setWindowTitle("Message")
                    msg.setDetailedText("Your data is successfully Deleted in database")
                    msg.exec_()
                    self.load()

        except mc.Error as e:
                    print(e)

    def reset_fun_doner(self):
        self.getName.setText("")
        self.getSirname.setText("")
        self.getDOB.setText("")
        self.getAge.setText("")
        self.Gender.setItemText(0,'Male')
        self.getID.setText("")
        self.getAdress.setText("")
        self.blood_group.setItemText(0,'A+')
        self.blood_donated.setText("")

    def searchby_doner(self):
        if str(self.searchby.currentText()) == 'Name':
            searchby = 'Name'
        elif str(self.searchby.currentText()) =='Sirname':
            searchby = 'Sirname'
        elif str(self.searchby.currentText()) =='ID':
            searchby = 'ID'
        elif str(self.searchby.currentText()) =='Blood':
            searchby = 'Blood_Group'

        search = self.Search.text()
        if search == '':
            self.load()
        try:
            mydb = mc.connect(
                host="localhost",
                user='root',
                password='Lucifer@123',
                database='blood_camp'
            )

            mycursor = mydb.cursor()
            table_name = 'doner_data'
            mycursor.execute("SELECT * FROM {} WHERE {} = '{}'".format(table_name,str(searchby),str(search))) #,str(searchby),str(search)
            result = mycursor.fetchall()
            print(result)
            self.tableWidget.setRowCount(0)
            #self.tableWidget.setRowCount(11)
            #self.tableWidget.setColumnCount(9)

            for row_number, row_data in enumerate(result):
                self.tableWidget.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.tableWidget.setItem(row_number, column_number, QTableWidgetItem(str(data)))

            print("display 4")

            mydb.commit()
            mycursor.close()
            mydb.close()
            #self.db_to_table_doner()
        except mc.Error as e:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)

            msg.setText("Data not found")
            msg.setInformativeText("Your Search is wrong")
            msg.setWindowTitle("Error")
            msg.setDetailedText(str(e))
            msg.exec_()
            print(e)


    ############################################

    ######################### Volunteer Data #########################
    def insert_data_Volunteer(self):
        name = self.getName_v.text()
        sirname = self.getSirname_v.text()
        mobile = self.getMobile_v.text()
        gmail = self.getGmail_v.text()
        id = self.getID_v.text()
        gender = self.Gender_v.currentText()
        address = self.getAdress_v.toPlainText()

        print(name + " " + sirname + " " + gender + " " + address)
        if str(name) == '' or str(sirname) == '' or str(mobile) == '' or str(gmail) == '' or str(id) == '' or str(address)=='':
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
                query = """INSERT INTO blood_camp.volunteer_data (Name,Sirname,Mobile,Gmail,ID,Gender,Address) VALUES (%s, %s, %s, %s, %s, %s, %s)"""
                value = (name, sirname, mobile,gmail,id,gender,address)

                mycursor.execute(query, value)
                mydb.commit()
                mycursor.close()
                mydb.close()


                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)

                msg.setText("Your data is Successfully added")
                msg.setInformativeText("")
                msg.setWindowTitle("Message")
                msg.setDetailedText("Your data is successfully store in database")
                msg.exec_()
                self.load()
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

    def db_to_table_volunteer(self):
        try:
            mydb = mc.connect(
                host="localhost",
                user='root',
                password='Lucifer@123',
                database='blood_camp'
            )

            mycursor = mydb.cursor()
            table_name = 'volunteer_data'
            mycursor.execute("SELECT * FROM {}".format(table_name))
            result = mycursor.fetchall()
            self.tableWidget_v.setRowCount(0)

            for row_number, row_data in enumerate(result):
                self.tableWidget_v.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.tableWidget_v.setItem(row_number, column_number, QTableWidgetItem(str(data)))

            print("display 4")

            mydb.commit()
            mycursor.close()
            mydb.close()
            #self.db_to_table_doner()
        except mc.Error as e:
            print(e)
            pass

    def update_row_volunteer(self):
        name = self.getName_v.text()
        sirname = self.getSirname_v.text()
        mobile = self.getMobile_v.text()
        gmail = self.getGmail_v.text()
        id = self.getID_v.text()
        gender = self.Gender_v.currentText()
        address = self.getAdress_v.toPlainText()

        try:
                    mydb = mc.connect(
                        host="localhost",
                        user='root',
                        password='Lucifer@123',
                        database='blood_camp'
                    )

                    mycursor = mydb.cursor()
                    query =  """UPDATE blood_camp.volunteer_data SET Name=%s, Sirname=%s,Mobile=%s,Gmail=%s,ID=%s,Gender=%s,Address=%s WHERE ID=%s"""
                    #Name,Sirname,DOB,Age,Gender,ID,Address,Blood_Group,Blood_Donated
                    mycursor.execute(query,(name, sirname, mobile,gmail,id,gender,address,id))
                    mydb.commit()
                    mycursor.close()
                    mydb.close()

                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Information)

                    msg.setText("Your data is Successfully Updated")
                    msg.setInformativeText("")
                    msg.setWindowTitle("Message")
                    msg.setDetailedText("Your data is successfully updated in database")
                    msg.exec_()
                    self.load()

                    print("Updated")

        except mc.Error as e:
                    print(e)

    def get_row_data_volunteer(self,ind):
            print('ahah')
            mydb = mc.connect(
                host="localhost",
                user='root',
                password='Lucifer@123',
                database='blood_camp'
            )

            mycursor = mydb.cursor()
            table_name = 'volunteer_data'
            mycursor.execute("SELECT * FROM {}".format(table_name))

            result = mycursor.fetchall()
            self.getName_v.setText(result[ind][0])
            self.getSirname_v.setText(result[ind][1])
            self.getMobile_v.setText(result[ind][2])
            self.getGmail_v.setText(result[ind][3])
            self.getID_v.setText(result[ind][4])
            self.Gender_v.setCurrentText(result[ind][5])
            self.getAdress_v.setText(result[ind][6])

            mydb.commit()
            mycursor.close()
            mydb.close()

    def reset_volunteer(self):
        self.getName_v.setText('')
        self.getSirname_v.setText('')
        self.getMobile_v.setText('')
        self.getGmail_v.setText('')
        self.getID_v.setText('')
        self.Gender_v.setItemText(0, 'Male')
        self.getAdress_v.setText('')

    def delete_row_volunteer(self):
        id = self.getID_v.text()
        try:
                    print("delete")
                    mydb = mc.connect(
                        host="localhost",
                        user='root',
                        password='Lucifer@123',
                        database='blood_camp'
                    )

                    mycursor = mydb.cursor()
                    query = "DELETE FROM blood_camp.volunteer_data WHERE ID = %s"
                    mycursor.execute(query,(str(id),))  # ,ad
                    print("dfe")
                    mydb.commit()
                    mycursor.close()
                    mydb.close()

                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Information)

                    msg.setText("Your data is Successfully Deleted")
                    msg.setInformativeText("")
                    msg.setWindowTitle("Message")
                    msg.setDetailedText("Your data is successfully Deleted in database")
                    msg.exec_()
                    self.load()

        except mc.Error as e:
                    print(e)

    def searchby_volunteer(self):

        searchby = self.searchby_v.currentText()
        if str(searchby) == 'Name':
            searchby = 'Name'
        elif str(searchby) =='Sirname':
            searchby = 'Sirname'
        elif str(searchby) =='ID':
            searchby = 'ID'

        search = self.search_v.text()
        if search == '':
            self.load()
        try:
            mydb = mc.connect(
                host="localhost",
                user='root',
                password='Lucifer@123',
                database='blood_camp'
            )

            mycursor = mydb.cursor()
            table_name = 'volunteer_data'
            mycursor.execute("SELECT * FROM {} WHERE {} = '{}'".format(table_name,str(searchby),str(search))) #,str(searchby),str(search)
            result = mycursor.fetchall()
            print(result)
            self.tableWidget_v.setRowCount(0)

            for row_number, row_data in enumerate(result):
                self.tableWidget_v.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.tableWidget_v.setItem(row_number, column_number, QTableWidgetItem(str(data)))

            print("display 4")

            mydb.commit()
            mycursor.close()
            mydb.close()
            #self.db_to_table_doner()
        except mc.Error as e:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)

            msg.setText("Data not found")
            msg.setInformativeText("Your Search is wrong")
            msg.setWindowTitle("Error")
            msg.setDetailedText(str(e))
            msg.exec_()
            print(e)
    ####################################################################

    ############################ Approval #################################
    def get_row_data_approval(self,ind):
            print('ahah')
            mydb = mc.connect(
                host="localhost",
                user='root',
                password='Lucifer@123',
                database='blood_camp'
            )

            mycursor = mydb.cursor()
            table_name = 'approval_data' #approval_data
            mycursor.execute("SELECT * FROM {}".format(table_name))

            result = mycursor.fetchall()
            self.getName_a.setText(result[ind][0])
            self.getSirname_a.setText(result[ind][1])
            self.getMobile_a.setText(result[ind][2])
            self.getGmail_a.setText(result[ind][3])
            self.getID_a.setText(result[ind][4])
            self.Gender_a.setCurrentText(result[ind][5])
            self.getAdress_a.setText(result[ind][6])

            mydb.commit()
            mycursor.close()
            mydb.close()

    def db_to_table_approval(self):
        try:
            mydb = mc.connect(
                host="localhost",
                user='root',
                password='Lucifer@123',
                database='blood_camp'
            )

            mycursor = mydb.cursor()
            table_name = 'approval_data'
            mycursor.execute("SELECT * FROM {}".format(table_name))
            result = mycursor.fetchall()
            self.tableWidget_a.setRowCount(0)

            for row_number, row_data in enumerate(result):
                self.tableWidget_a.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.tableWidget_a.setItem(row_number, column_number, QTableWidgetItem(str(data)))

            print("display 4")

            mydb.commit()
            mycursor.close()
            mydb.close()
            #self.db_to_table_doner()
        except mc.Error as e:
            print(e)
            pass

    def volunteer_approval(self):
        name = self.getName_a.text()
        sirname = self.getSirname_a.text()
        mobile = self.getMobile_a.text()
        gmail = self.getGmail_a.text()
        id = self.getID_a.text()
        gender = self.Gender_a.currentText()
        address = self.getAdress_a.toPlainText()

        print(name + " " + sirname + " " + gender + " " + address)
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
                query = """INSERT INTO blood_camp.volunteer_data (Name,Sirname,Mobile,Gmail,ID,Gender,Address) VALUES (%s, %s, %s, %s, %s, %s, %s)"""
                value = (name, sirname, mobile, gmail, id, gender, address)

                mycursor.execute(query, value)
                mydb.commit()
                mycursor.close()
                mydb.close()

                try:
                    mydb = mc.connect(
                        host="localhost",
                        user='root',
                        password='Lucifer@123',
                        database='blood_camp'
                    )

                    mycursor = mydb.cursor()
                    query = "DELETE FROM blood_camp.approval_data WHERE ID = %s"
                    mycursor.execute(query, (str(id),))  # ,ad
                    print("dfe")
                    mydb.commit()
                    mycursor.close()
                    mydb.close()

                    '''msg = QMessageBox()
                    msg.setIcon(QMessageBox.Information)

                    msg.setText("Your data is Successfully Deleted")
                    msg.setInformativeText("")
                    msg.setWindowTitle("Message")
                    msg.setDetailedText("Your data is successfully Deleted in database")
                    msg.exec_()
                    self.load()'''

                except mc.Error as e:
                    print(e)

                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)

                msg.setText("Your data is Successfully added")
                msg.setInformativeText("")
                msg.setWindowTitle("Message")
                msg.setDetailedText("Your data is successfully store in database")
                msg.exec_()
                self.send_mail(str(gmail), 'approve')
                self.load()


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

    def volunteer_decline(self):
        gmail = self.getGmail_a.text()
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)

        msg.setText("Mail of declinationis sended to applicant")
        msg.setInformativeText("")
        msg.setWindowTitle("Message")
        msg.setDetailedText("Mail of declinationis sended to applicant")
        msg.exec_()
        self.send_mail(str(gmail),'decline')
        self.load()

    def searchby_approval(self):
        print("nndndn")
        searchby = self.searchby_a.currentText()
        if str(searchby) == 'Name':
            searchby = 'Name'
        elif str(searchby) =='Sirname':
            searchby = 'Sirname'
        elif str(searchby) =='ID':
            searchby = 'ID'

        search = self.search_a.text()
        if search == '':
            self.load()
        try:
            mydb = mc.connect(
                host="localhost",
                user='root',
                password='Lucifer@123',
                database='blood_camp'
            )

            mycursor = mydb.cursor()
            table_name = 'approval_data'
            mycursor.execute("SELECT * FROM {} WHERE {} = '{}'".format(table_name,str(searchby),str(search))) #,str(searchby),str(search)
            result = mycursor.fetchall()
            print(result)
            self.tableWidget_a.setRowCount(0)
            for row_number, row_data in enumerate(result):
                self.tableWidget_a.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.tableWidget_a.setItem(row_number, column_number, QTableWidgetItem(str(data)))


            print("display 4")

            mydb.commit()
            mycursor.close()
            mydb.close()
            #self.db_to_table_doner()
        except mc.Error as e:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)

            msg.setText("Data not found")
            msg.setInformativeText("Your Search is wrong")
            msg.setWindowTitle("Error")
            msg.setDetailedText(str(e))
            msg.exec_()
            print(e)

    ####################################################################

    ####################### Certificate #############################
    def db_to_table_volunteer_certificate(self):
        try:
            mydb = mc.connect(
                host="localhost",
                user='root',
                password='Lucifer@123',
                database='blood_camp'
            )

            mycursor = mydb.cursor()
            table_name = 'volunteer_data'
            mycursor.execute("SELECT * FROM {}".format(table_name))
            result = mycursor.fetchall()
            self.tableWidget_vol_c.setRowCount(0)

            for row_number, row_data in enumerate(result):
                self.tableWidget_vol_c.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.tableWidget_vol_c.setItem(row_number, column_number, QTableWidgetItem(str(data)))

            print("display 4")

            mydb.commit()
            mycursor.close()
            mydb.close()
            #self.db_to_table_doner()
        except mc.Error as e:
            print(e)
            pass

    def get_row_data_vol_certificate(self,ind):
            print('vol_certificate')
            mydb = mc.connect(
                host="localhost",
                user='root',
                password='Lucifer@123',
                database='blood_camp'
            )

            mycursor = mydb.cursor()
            table_name = 'volunteer_data'
            mycursor.execute("SELECT * FROM {}".format(table_name))

            result = mycursor.fetchall()
            self.getName_vol_c.setText(result[ind][0])
            self.getSirname_vol_c.setText(result[ind][1])
            self.getMobile_vol_c.setText(result[ind][2])
            self.getGmail_vol_c.setText(result[ind][3])
            self.getID_vol_c.setText(result[ind][4])
            self.Gender_v.setCurrentText(result[ind][5])
            self.getAdress_vol_c.setText(result[ind][6])

            mydb.commit()
            mycursor.close()
            mydb.close()
    def send_certificate(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)

        msg.setText("Certificate is Sended to your mail")
        msg.setInformativeText("")
        msg.setWindowTitle("Message")
        msg.setDetailedText("Please check mail.If any Query please contact us")
        msg.exec_()
        from sendmail import generate_certificate,send_mail_w_attach
        name = self.getName_vol_c.text()
        sirname = self.getSirname_vol_c.text()
        gmail = self.getGmail_vol_c.text()
        vol_name = name+" "+sirname
        generate_certificate(vol_name)
        send_mail_w_attach(gmail,vol_name)

    def print_certificate(self):
        from sendmail import print_c
        name = self.getName_vol_c.text()
        sirname = self.getSirname_vol_c.text()
        #gmail = self.getGmail_vol_c.text()

        vol_name = name + " " + sirname
        print_c(vol_name)

    ###### Set Button Style####
    def buttun_style(self,num):
        if num == 'Home':
            light_1 = '#60FF42'
            light_2 = '#1DB700'
            light_3 = '#1DB700'
            light_4 = '#1DB700'
            light_5 = '#1DB700'
            #dark = '#1DB700'
        elif num == 'Doner':
            light_1 = '#1DB700'
            light_2 = '#60FF42'
            light_3 = '#1DB700'
            light_4 = '#1DB700'
            light_5 = '#1DB700'
        elif num == 'Volunteer':
            light_1 = '#1DB700'
            light_2 = '#1DB700'
            light_3 = '#60FF42'
            light_4 = '#1DB700'
            light_5 = '#1DB700'
        elif num == 'Approval':
            light_1 = '#1DB700'
            light_2 = '#1DB700'
            light_3 = '#1DB700'
            light_4 = '#60FF42'
            light_5 = '#1DB700'
        elif num == 'Certificate':
            light_1 = '#1DB700'
            light_2 = '#1DB700'
            light_3 = '#1DB700'
            light_4 = '#1DB700'
            light_5 = '#60FF42'

        self.pushButton.setStyleSheet("background-color:"+light_1+";"
                                        "border-top-left-radius :20px;"
                                        "border-top-right-radius : 0px; "
                                        "border-bottom-left-radius : 20px;"
                                        "border-bottom-right-radius : 0px")
        self.pushButton_2.setStyleSheet("background-color:" + light_2 + ";"
                                                                      "border-top-left-radius :20px;"
                                                                      "border-top-right-radius : 0px; "
                                                                      "border-bottom-left-radius : 20px;"
                                                                      "border-bottom-right-radius : 0px")
        self.pushButton_3.setStyleSheet("background-color:" + light_3 + ";"
                                                                      "border-top-left-radius :20px;"
                                                                      "border-top-right-radius : 0px; "
                                                                      "border-bottom-left-radius : 20px;"
                                                                      "border-bottom-right-radius : 0px")
        self.pushButton_4.setStyleSheet("background-color:" + light_4 + ";"
                                                                      "border-top-left-radius :20px;"
                                                                      "border-top-right-radius : 0px; "
                                                                      "border-bottom-left-radius : 20px;"
                                                                      "border-bottom-right-radius : 0px")
        self.pushButton_5.setStyleSheet("background-color:" + light_5 + ";"
                                                                      "border-top-left-radius :20px;"
                                                                      "border-top-right-radius : 0px; "
                                                                      "border-bottom-left-radius : 20px;"
                                                                      "border-bottom-right-radius : 0px")


######################################################################################

###########################  Certificate ############################

######################################################################################
def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)

def main_1():
    app_1 = QApplication(sys.argv)
    window_1 = MainApp()
    window_1.show()
    app_1.exec_()

if __name__ == '__main__':
    main_1()
    #sys.excepthook = except_hook