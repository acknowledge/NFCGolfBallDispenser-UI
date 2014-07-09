#!/usr/bin/env python
# -*- coding: utf-8 -*-

## @file ui.py
#  Contains the class Frame.

## @package ui
#  Graphical User Interface made with PySide.
#  @author CASAS Jacky
#  @date 22.06.2014
#  @version 1.0

import sys
import os
from PySide import QtGui
from PySide.QtGui import *
from PySide.QtCore import *
from constants import *

class Frame(QtGui.QWidget):
    """! @brief
    Main window of the software.
    @author CASAS Jacky
    @date 22.06.14
    @version 1.0
    """
    ## Signal used to activate PiFace buttons
    activateButton = Signal()
    ## Signal used to deactivate PiFace buttons
    deactivateButton = Signal()
    
    def __init__(self, parent=None):
        """! @brief Frame constructor. 
        @param self the Frame instance
        @param parent the parent QWidget, optional
        """
        QtGui.QWidget.__init__(self, parent)
        
        #self.resize(600,500)
        self.setFont(QtGui.QFont("Verdana")) 
        self.setWindowTitle("NFC Golf Ball Dispenser")

        self.setGeometry(0, 0, 650, 550)
        self.centerOnScreen()
        #self.setMinimumWidth(370)
        self.setMinimumHeight(470)

        ## Label to display a welcome message
        self.l1 = QtGui.QLabel("Welcome<br />on<br />NFC Golf Ball Dispenser", self)
        self.l1.setStyleSheet('font-size:30pt; qproperty-alignment:AlignCenter; qproperty-wordWrap:true;')
        ## Label to display the name of the developer
        self.l2 = QtGui.QLabel('created by Jacky Casas', self)
        self.l2.setStyleSheet('font-size:10pt; qproperty-alignment:AlignRight; qproperty-wordWrap:true;')
        self.l2.setFixedHeight(16)
        ## Label to display instructions
        self.l3 = QtGui.QLabel('Just approach your smartphone or smartcard in front of the reader', self)
        self.l3.setStyleSheet('font-size:20pt; qproperty-alignment:AlignCenter; qproperty-wordWrap:true;')
        ## Label to display the status (waiting for a card or card detected)
        self.l4 = QtGui.QLabel('waiting', self)  
        self.l4.setStyleSheet('font-size:12pt; qproperty-alignment:AlignCenter; background-color:#E0E0E0; padding:4px; margin:10px 30px;')
        ## Label to display a welcome message in the log view
        self.logl1 = QtGui.QLabel("Welcome on the login of the administration")
        self.logl1.setStyleSheet('font-size:30pt; qproperty-alignment:AlignCenter; qproperty-wordWrap:true;')
        self.logl1.setVisible(False)
        ## Label to display a welcome message in the admin view
        self.adminl1 = QtGui.QLabel("Welcome on the admin")
        self.adminl1.setStyleSheet('font-size:30pt; qproperty-alignment:AlignCenter; qproperty-wordWrap:true;')
        self.adminl1.setVisible(False)
        ## LineEdit to enter the username
        self.adminUsername = QtGui.QLineEdit()
        self.adminUsername.setPlaceholderText('username')
        self.adminUsername.setVisible(False)
        ## LineEdit to enter the password
        self.adminPassword = QtGui.QLineEdit()
        self.adminPassword.setPlaceholderText('password')
        self.adminPassword.setVisible(False)
        self.adminPassword.setEchoMode(QtGui.QLineEdit.Password)

        ## Button to enter in the admin
        self.log = QtGui.QPushButton('Login')
        self.log.setVisible(False)
        hLayoutLogin = QtGui.QHBoxLayout()
        hLayoutLogin.addWidget(self.adminUsername)
        hLayoutLogin.addWidget(self.adminPassword)
        hLayoutLogin.addWidget(self.log)

        ## Button to withdraw 2 CHF
        self.b1 = QtGui.QPushButton('2 CHF - 30 balls', self)
        self.b1.setEnabled(False)
        ## Button to withdraw 5 CHF
        self.b2 = QtGui.QPushButton('5 CHF - 80 balls', self)
        self.b2.setEnabled(False)
        ## Button to show the last 10 transactions
        self.transaction = QtGui.QPushButton('last transactions')
        self.transaction.setEnabled(False)
        ## Button to access the admin view
        self.admin = QtGui.QPushButton('admin')

        hLayoutButtons = QtGui.QHBoxLayout()
        hLayoutButtons.addWidget(self.b1)
        hLayoutButtons.addWidget(self.b2)
        hLayoutButtons.addWidget(self.transaction)
        hLayoutButtons.addWidget(self.admin)

        ## Label indicating the recharge of an account
        self.lRecharge = QtGui.QLabel('Recharge the account :')
        self.lRecharge.setVisible(False)
        ## SpinBox to enter the amount we want to recharge
        self.moneyBox = QtGui.QSpinBox()
        self.moneyBox.setRange(0, 1000)
        self.moneyBox.setSingleStep(10)
        self.moneyBox.setSuffix(' CHF')
        self.moneyBox.setValue(20)
        self.moneyBox.setVisible(False)
        ## Button to recharge an account
        self.bRecharge = QtGui.QPushButton('Recharge', self)
        self.bRecharge.setVisible(False)

        hLayoutRecharge = QtGui.QHBoxLayout()
        hLayoutRecharge.addWidget(self.lRecharge)
        hLayoutRecharge.addWidget(self.moneyBox)
        hLayoutRecharge.addWidget(self.bRecharge)

        ## LineEdit to write the username to create an account
        self.username = QtGui.QLineEdit()
        self.username.setPlaceholderText('username')
        self.username.setVisible(False)
        ## LineEdit to write the name to create an account
        self.name = QtGui.QLineEdit()
        self.name.setPlaceholderText('name')
        self.name.setVisible(False)
        ## LineEdit to write the surname to create an account
        self.surname = QtGui.QLineEdit()
        self.surname.setPlaceholderText('surname')
        self.surname.setVisible(False)
        ## Button to create an account
        self.bCreateAccount = QtGui.QPushButton('Create account')
        self.bCreateAccount.setVisible(False)

        hLayoutAccount = QtGui.QHBoxLayout()
        hLayoutAccount.addWidget(self.username)
        hLayoutAccount.addWidget(self.name)
        hLayoutAccount.addWidget(self.surname)
        hLayoutAccount.addWidget(self.bCreateAccount)

        ## Label indicating that we can add a card to an account
        self.lAddDevice = QtGui.QLabel('Add smartcard to account :')
        self.lAddDevice.setVisible(False)
        ## LineEdit to write the username of the account
        self.username2 = QtGui.QLineEdit()
        self.username2.setPlaceholderText('username')
        self.username2.setVisible(False)
        ## Button to add a smartcart to an account
        self.bAddDevice = QtGui.QPushButton('Add smartcard')
        self.bAddDevice.setVisible(False)

        hLayoutAddDevice = QtGui.QHBoxLayout()
        hLayoutAddDevice.addWidget(self.lAddDevice)
        hLayoutAddDevice.addWidget(self.username2)
        hLayoutAddDevice.addWidget(self.bAddDevice)

        ## Label indicating that it is the last 10 transactions
        self.lTransaction = QtGui.QLabel("The last 10<br />transactions")
        self.lTransaction.setStyleSheet('font-size:15pt; qproperty-alignment:AlignCenter; qproperty-wordWrap:true;')
        self.lTransaction.setVisible(False)
        ## TableWidget to display the 10 last transactions
        self.transactionTable = QtGui.QTableWidget()
        self.transactionTable.setVisible(False)
        self.transactionTable.setColumnCount(3)
        title = ['date', 'amount', 'currency']
        vheader = QtGui.QHeaderView(Qt.Orientation.Vertical)
        vheader.setResizeMode(QtGui.QHeaderView.Stretch) # Stretch, Interactive, Fixed, Custom, ResizeToContents
        self.transactionTable.setVerticalHeader(vheader)
        hheader = QtGui.QHeaderView(Qt.Orientation.Horizontal)
        hheader.setResizeMode(QtGui.QHeaderView.ResizeToContents)
        hheader.setStretchLastSection(True)
        self.transactionTable.setHorizontalHeader(hheader)
        self.transactionTable.setHorizontalHeaderLabels(title)
        self.transactionTable.setMaximumWidth(430)

        hLayoutTransaction = QtGui.QHBoxLayout()
        hLayoutTransaction.addWidget(self.lTransaction)
        hLayoutTransaction.addWidget(self.transactionTable)
        
        ## Label to indicate that it is the status
        self.lStatus = QtGui.QLabel()
        self.lStatus.setStyleSheet('background-color:#E0E0E0; padding:4px;')
        self.lStatus.setText('Status : ')
        self.lStatus.setFixedHeight(24)
        self.lStatus.setFixedWidth(60)
        ## Label to display the status of an action
        self.status = QtGui.QLabel()
        self.status.setStyleSheet('background-color:#E0E0E0; padding:4px;')
        self.status.setAlignment(Qt.AlignCenter);
        self.status.setFixedHeight(24)

        hLayoutStatus = QtGui.QHBoxLayout()
        hLayoutStatus.addWidget(self.lStatus)
        hLayoutStatus.addWidget(self.status)

        # link all the layouts to the main vertical layout
        verticalLayout = QtGui.QVBoxLayout()
        
        verticalLayout.addWidget(self.l1)
        verticalLayout.addWidget(self.logl1)
        verticalLayout.addWidget(self.adminl1)
        verticalLayout.addWidget(self.l2)
        verticalLayout.addLayout(hLayoutLogin)
        verticalLayout.addWidget(self.l3)
        verticalLayout.addWidget(self.l4)

        verticalLayout.addLayout(hLayoutTransaction)
        verticalLayout.addLayout(hLayoutRecharge)
        verticalLayout.addLayout(hLayoutAccount)
        verticalLayout.addLayout(hLayoutAddDevice)
        verticalLayout.addLayout(hLayoutButtons)
        verticalLayout.addLayout(hLayoutStatus)

        self.setLayout(verticalLayout)
 
        try:
            self.setWindowIcon(QtGui.QIcon('icon.png')) 
        except:pass

        ## Timer used to display a warning during a fixed time
        self.warningTimer = QTimer(self)
        self.warningTimer.setSingleShot(True)
        ## Timer used to release the card after x seconds if the user don't make any action
        self.releaseCardTimer = QTimer(self)
        self.releaseCardTimer.setSingleShot(True)
        ## Step of the *waiting* text
        self.step = 0
        ## Transaction visibility
        self.transactionIsVisible = False
        ## Admin visibility
        self.adminActivated = False

    @Slot()
    def update(self):
        """! @brief Slot used to update the *waiting* label.
        @param self the Frame instance
        """
        self.step += 1
        self.step %= 4
        self.l4.setText('waiting ' + self.step * '.')
        self.b1.setEnabled(False)
        self.b2.setEnabled(False)
        self.transaction.setEnabled(False)

        if self.transactionIsVisible:
            self.lTransaction.setVisible(False)
            self.transactionTable.setVisible(False)
            self.transactionIsVisible = False
            
        self.deactivateButton.emit()

    @Slot(int)
    def displayCard(self, balance):
        """! @brief Slot called when a card is detected. It displays the balance of the account.
        @param self the Frame instance
        @param balance the balance of the account linked to the card
        """
        self.l4.setText('Card detected.<br />There is ' + `balance` + ' CHF left on your account.')
        self.b1.setEnabled(True)
        self.b2.setEnabled(True)
        self.transaction.setEnabled(True)

        self.activateButton.emit()
        
        # 10 secondes timer before releasing the card if no action is make
        self.releaseCardTimer.start(10000)

    @Slot(int)
    def displayWarning(self, warning):
        """! @brief Slot which displays a warning.
        @param self the Frame instance
        @param warning identifier of the warning to be displayed
        """
        if (warning == WARN_NO_ACCOUNT):
            self.l4.setText('This card is not linked to any account.<br />Please create an account or link it to yours.')
        elif (warning == WARN_ACCOUNT_INACTIVE):
            self.l4.setText('Your account has been disable.<br />Please contact the administrator for further information.')
        elif (warning == WARN_ACCOUNT_DELETED):
            self.l4.setText('Your account has been deleted.<br />You can\'t use your card anymore.')
        elif (warning == WARN_DEVICE_LOST):
            self.l4.setText('This device has been lost.<br />Please send it to the administrator.')
        elif (warning == WARN_DEVICE_STOLEN):
            self.l4.setText('Stealing is bad !<br />Please send the device to the administrator.')
        elif (warning == WARN_DEVICE_DELETED):
            self.l4.setText('This device has been deleted from your account.<br />You can\'t use it anymore')
        else:
            self.l4.setText('An error has occurred')

        self.deactivateButton.emit()
        
        self.warningTimer.start(5000)

    @Slot(str)
    def displayStatus(self, message):
        """! @brief Slot which displays the status of an action.
        @param self the Frame instance
        @param message test to write on the status bar
        """
        self.status.setText(message)

    @Slot(str)
    def displayTransactions(self, trs):
        """! @brief Slot which displays the status of an action.
        @param self the Frame instance
        @param trs array with the last transactions
        """
        if self.transactionIsVisible == False:
            self.status.setText('click again to hide transactions')
            self.transactionTable.setRowCount(len(trs))

            for i in range(len(trs)):
                for j in range(len(trs[0])):
                    item = QtGui.QTableWidgetItem(trs[i][j])
                    if j == 1:
                        item.setTextAlignment(Qt.AlignVCenter | Qt.AlignRight)
                    self.transactionTable.setItem(i, j, item)

            self.lTransaction.setVisible(True)
            self.transactionTable.setVisible(True)
            self.transactionIsVisible = True
        else:
            self.status.setText('')
            self.lTransaction.setVisible(False)
            self.transactionTable.setVisible(False)
            self.transactionIsVisible = False

    @Slot()
    def toggleAdminView(self):
        """! @brief Slot which displays of hides the administration view
        @param self the Frame instance
        """
        if self.adminActivated:
            self.adminActivated = False
            self.admin.setText('admin')
            self.displayMainWindow()
        else:
            self.adminActivated = True
            self.admin.setText('return')
            self.displayLogin()

    def displayMainWindow(self):
        """! @brief Method which displays the elements for the user view.
        @param self the Frame instance
        """
        self.l1.setVisible(True)
        self.l2.setVisible(True)
        self.l3.setVisible(True)
        self.logl1.setVisible(False)
        self.adminl1.setVisible(False)

        self.adminUsername.setVisible(False)
        self.adminPassword.setVisible(False)
        self.log.setVisible(False)

        self.lRecharge.setVisible(False)
        self.moneyBox.setVisible(False)
        self.bRecharge.setVisible(False)

        self.username.setVisible(False)
        self.name.setVisible(False)
        self.surname.setVisible(False)
        self.bCreateAccount.setVisible(False)

        self.lAddDevice.setVisible(False)
        self.username2.setVisible(False)
        self.bAddDevice.setVisible(False)

    def displayLogin(self):
        """! @brief Method which displays the elements for the login view.
        @param self the Frame instance
        """
        self.l1.setVisible(False)
        self.l2.setVisible(False)
        self.l3.setVisible(False)
        self.logl1.setVisible(True)
        self.adminl1.setVisible(False)

        self.adminUsername.setVisible(True)
        self.adminPassword.setVisible(True)
        self.log.setVisible(True)

        self.lRecharge.setVisible(False)
        self.bRecharge.setVisible(False)
        self.moneyBox.setVisible(False)

        self.username.setVisible(False)
        self.name.setVisible(False)
        self.surname.setVisible(False)
        self.bCreateAccount.setVisible(False)

        self.lAddDevice.setVisible(False)
        self.username2.setVisible(False)
        self.bAddDevice.setVisible(False)

    @Slot()
    def displayAdmin(self, username, password):
        """! @brief Slot which displays the elements for the admin.
        @param self the Frame instance
        @param username username to access the admin
        @param password password to access the admin
        """
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            self.l1.setVisible(False)
            self.l2.setVisible(False)
            self.l3.setVisible(False)
            self.logl1.setVisible(False)
            self.adminl1.setVisible(True)

            self.adminUsername.setVisible(False)
            self.adminPassword.setVisible(False)
            self.log.setVisible(False)

            self.lRecharge.setVisible(True)
            self.bRecharge.setVisible(True)
            self.moneyBox.setVisible(True)

            self.username.setVisible(True)
            self.name.setVisible(True)
            self.surname.setVisible(True)
            self.bCreateAccount.setVisible(True)

            self.lAddDevice.setVisible(True)
            self.username2.setVisible(True)
            self.bAddDevice.setVisible(True)

            self.status.setVisible(True)
        
    def centerOnScreen(self):
        """! @brief Method to center the application on the screen.
        @param self the Frame instance
        """
        resolution = QtGui.QDesktopWidget().screenGeometry()
        self.move((resolution.width() / 2) - (self.frameSize().width() / 2),
                  (resolution.height() / 2) - (self.frameSize().height() / 2))

    def maximizeOnScreen(self):
        """! @brief Method to maximize the application on the screen.
        @param self the Frame instance
        """
        resolution = QtGui.QDesktopWidget().screenGeometry()
        self.setGeometry(0, 0, resolution.width(), resolution.height())

    def fullScreen(self):
        """! @brief Method to make the application full screen.
        @param self the Frame instance
        """
        self.showFullScreen()

    def keyPressEvent(self, e):
        """! @brief Called when a key is pressed. Exit the application when *ESC* is pressed.
        @param self the Frame instance
        @param e the event
        """
        if e.key() == Qt.Key_Escape:
            # close the button listener's threads
            self.deactivateButton.emit()
            # close the window
            self.close()
