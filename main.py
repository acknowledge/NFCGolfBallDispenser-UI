#!/usr/bin/env python
# -*- coding: utf-8 -*-

## @file main.py
#  File containing the main fonction. Entry of the code.
 
## @package main
#  Main.
#  @author CASAS Jacky
#  @date 22.06.14
#  @version 1.0
 
## @mainpage Dispenser UI documentation
#  @section intro_sec Introduction
#  This the documentation of the **NFC Golf Ball Dispenser**. 
#
#  A NFC Card Reader is plugged in a Raspberry Pi. 
#  The Raspberry Pi communicate with a remote MongoDB database and display information to the customer via a screen.
#
#  @section overview_sec Overview
#  This image shows an overview of the interface of this project.
#  ![Overview](../img/overview.png)
#
#  @section classdiagram_sec Class Diagram
#  And here it is the complete class diagram.
#  ![Class Diagram](../img/classDiagram.png)
#
#  @section license_sec License
#  This software is developped by Jacky CASAS and was commissioned by Digiclever. 
#  For further information about the license, please contact Digiclever (http://digiclever.com).
#
#  This project was developped at HES-SO//Valais during the bachelor thesis of Jacky Casas in 2014.

from cardreader import CardReader
from ui import Frame
from action import Action
from pifacecontrol import PiFaceControl
import sys
from PySide import QtGui
from PySide.QtCore import *
from functools import partial

def main():
    """! @brief Main of the software"""

    ## Qt Application
    app = QtGui.QApplication(sys.argv)
    app.setOrganizationName('Digiclever')
    app.setApplicationName('NFC Golf Ball Dispenser')
    ## Frame instance
    frame = Frame()
    frame.show()
	
    ## PiFaceControl instance
    piface = PiFaceControl()
    ## Action instance
    action = Action(piface)
    ## CardReader instance
    cardReader = CardReader(action)

    # connect signals to slots
    frame.b1.clicked.connect(cardReader.someBalls)
    frame.b2.clicked.connect(cardReader.manyBalls)
    frame.transaction.clicked.connect(lambda: action.getLastTransactions(cardReader.cardUid))
    frame.admin.clicked.connect(frame.toggleAdminView)
    frame.log.clicked.connect(lambda: frame.displayAdmin(frame.adminUsername.text(), frame.adminPassword.text()))
    frame.bRecharge.clicked.connect(lambda: cardReader.recharge(frame.moneyBox.value()))
    frame.bCreateAccount.clicked.connect(lambda: action.addUser(frame.username.text(), frame.name.text(), frame.surname.text()))
    frame.bAddDevice.clicked.connect(lambda: action.addDevice(frame.username2.text(), cardReader.cardUid, cardReader.ATR))

    action.status.connect(frame.displayStatus)
    action.transactionsLoaded.connect(frame.displayTransactions)

    frame.connect(frame.warningTimer, SIGNAL("timeout()"), cardReader.start)
    frame.connect(frame.releaseCardTimer, SIGNAL("timeout()"), cardReader.start)

    cardReader.connect(cardReader.timer, SIGNAL("timeout()"), cardReader.waitForCard)
    cardReader.updateWaiting.connect(frame.update)

    cardReader.cardDetected.connect(frame.displayCard)
    cardReader.warning.connect(frame.displayWarning)
    
    frame.activateButton.connect(piface.activateButtonListener)
    frame.deactivateButton.connect(piface.deactivateButtonListener)
    
    piface.b1.connect(cardReader.someBalls)
    piface.b2.connect(cardReader.manyBalls)
    piface.b3.connect(lambda: action.getLastTransactions(cardReader.cardUid))
    piface.b4.connect(frame.toggleAdminView)

    cardReader.start()
    sys.exit(app.exec_())

if __name__ == '__main__':	
    main()
