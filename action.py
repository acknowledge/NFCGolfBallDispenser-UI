#!/usr/bin/env python
# -*- coding: utf-8 -*-

## @file action.py
#  Contains the class Action.

## @package action
#  Actions.
#  @author CASAS Jacky
#  @date 22.06.2014
#  @version 1.0

from uuid import uuid4
from datetime import datetime
from PySide.QtCore import *

from constants import *
from database import DataBase
from pifacecontrol import PiFaceControl

class Action(QObject):
    """! @brief
    Binding between the card reader and the database.
    @author CASAS Jacky
    @date 22.06.14
    @version 1.0
    """
    ## Signal used to display the action status on the UI
    status = Signal(str)
    ## Signal used to display the last transactions on the UI
    transactionsLoaded = Signal(list)

    def __init__(self, pifacecontrol):
        """! @brief Initialize the instance and get the two collections of the database.
        @param self the Action instance
        """
        QObject.__init__(self)
        ## contains a link to the database collection *user*
        self.users = DataBase().user
        ## contains a link to the database collection *transaction*
        self.transactions = DataBase().transaction

        self.piFace = pifacecontrol
        self.piFace.activateButtonListener()

    def transaction(self, deviceId, amount):
        """! @brief Method to make a transaction (withdraw an amount from an account).
        @param self the Action instance
        @param deviceId identifier of the device (smartcard or smartphone)
        @param amount amount to withdraw
        """
        canWithdraw = False
        user = self.users.find_one({"devices.uid": deviceId})
        for device in user['devices']:
            if device['uid'] == deviceId:
                if device['status'] == STA_DEVICE_ACTIVE:
                    if amount > 0:
                        if user['balance'] >= amount:    
                            canWithdraw = True
                        else:
                            self.status.emit('Please recharge your account, you don\'t have enough money in it.')
                    else:
                        self.status.emit('The amount must be greater than 0.')
                elif device['status'] == STA_DEVICE_LOST:
                    self.status.emit('Impossible transaction : Lost device.')
                elif device['status'] == STA_DEVICE_STOLEN:
                    self.status.emit('Impossible transaction : Stolen device.')
                elif device['status'] == STA_DEVICE_DELETED:
                    self.status.emit('Impossible transaction : Deleted device.')
                else:
                    self.status.emit('Impossible transaction : Device status unknown.')

                if canWithdraw:
                    # create transaction
                    userId = user['uid']
                    dispenserId = DISPENSER_ID
                    transactionDate = datetime.now()

                    transaction = {"userId":userId, "deviceId":deviceId, "dispenserId":dispenserId, "transactionType":WITHDRAWAL, "amount":amount, "transactionDate":transactionDate}
                    self.transactions.insert(transaction)

                    # debit credit in account
                    query = {"uid": user['uid'] }
                    update = {"$inc": { "balance": -amount}}
                    self.users.update(query, update)

                    self.status.emit('You withdraw ' + `amount` + ' CHF. You have now ' + `user['balance'] - amount` + ' CHF on your account.')
                    self.piFace.actionValidated()
                else:
                    self.piFace.actionDenied()
                break

    def recharge(self, deviceId, amount):
        """! @brief Method to make a recharge (put an amount in an account).
        @param self the Action instance
        @param deviceId identifier of the device (smartcard or smartphone)
        @param amount amount to recharge
        """
        canRecharge = False
        user = self.users.find_one({"devices.uid": deviceId})
        for device in user['devices']:
            if device['uid'] == deviceId:
                if device['status'] == STA_DEVICE_ACTIVE:
                    if amount > 0:  
                        canRecharge = True
                    else:
                        self.status.emit('The amount must be greater than 0.')
                elif device['status'] == STA_DEVICE_LOST:
                    self.status.emit('Impossible recharge : Lost device.')
                elif device['status'] == STA_DEVICE_STOLEN:
                    self.status.emit('Impossible recharge : Stolen device.')
                elif device['status'] == STA_DEVICE_DELETED:
                    self.status.emit('Impossible recharge : Deleted device.')
                else:
                    self.status.emit('Impossible recharge : Device status unknown.')

                if canRecharge:
                    # create transaction
                    userId = user['uid']
                    dispenserId = DISPENSER_ID
                    transactionDate = datetime.now()

                    transaction = {"userId":userId, "deviceId":deviceId, "dispenserId":dispenserId, "transactionType":RECHARGE, "amount":amount, "transactionDate":transactionDate}
                    self.transactions.insert(transaction)

                    # recharge account
                    query = {"uid": user['uid'] }
                    update = {"$inc": { "balance": amount}}
                    self.users.update(query, update)

                    self.status.emit('Recharge of ' + `amount` + ' CHF. You have now ' + `user['balance'] + amount` + ' CHF on your account.')
                    self.piFace.actionValidated()
                else:
                    self.piFace.actionDenied()
                break
            
    def getAccount(self, deviceId):
        """! @brief Method to get an account in a JSON format.
        @param self the Action instance
        @param deviceId identifier of the device (smartcard or smartphone)
        """
        user = self.users.find_one({"devices.uid": deviceId})
        if user is None:
            return None
        else:
            return user

    def getLastTransactions(self, deviceId):
        """! @brief Method to get the last 10 transactions.
        @param self the Action instance
        @param deviceId identifier of the device (smartcard or smartphone)
        """
        user = self.users.find_one({"devices.uid": deviceId})
        transactions = self.transactions.find(
                {'userId': user['uid']}, 
                {'_id': 0, 'amount': 1, 'transactionType': 1, 'transactionDate': 1, 'deviceId': 1, 'dispenserId': 1}
            ).limit(10).sort("transactionDate", -1)
        trs = []
        for transaction in transactions:
            tr = []
            tr.append(transaction['transactionDate'].strftime("%a %e %b %Y, %H:%M:%S"))
            if transaction['transactionType'] == RECHARGE:
                tr.append('+' + `transaction['amount']`)
            elif transaction['transactionType'] == WITHDRAWAL:
                tr.append('-' + `transaction['amount']`)
            tr.append('CHF')
            trs.append(tr)
        self.transactionsLoaded.emit(trs)

    def addUser(self, username, name=None, surname=None):
        """! @brief Method to create a new user account.
        @param self the Action instance
        @param username unique username
        @param name name of the user, optional
        @param surname surname of the user, optional
        """
        if not username:
            self.status.emit('Please enter at least a username.')
        else:
            userAlreadyRegistered = self.users.find_one({'username':username})
            if userAlreadyRegistered is None:
                uid = str(uuid4())
                balance = 0
                registrationDate = datetime.now()
                statement = STA_USER_ACTIVE
                devices = []

                if name is None:
                    if surname is None:
                        user = {"uid":uid, "username":username, "balance":balance, "registrationDate":registrationDate, "statement":statement, "devices":devices}
                    else:
                        user = {"uid":uid, "username":username, "surname":surname, "balance":balance, "registrationDate":registrationDate, "statement":statement, "devices":devices}
                else:
                    if surname is None:
                        user = {"uid":uid, "username":username, "name":name, "balance":balance, "registrationDate":registrationDate, "statement":statement, "devices":devices}
                    else:
                        user = {"uid":uid, "username":username, "name":name, "surname":surname, "balance":balance, "registrationDate":registrationDate, "statement":statement, "devices":devices}

                self.users.insert(user)
                self.status.emit('User successfully added to the database.')
                self.piFace.actionValidated()
            else:
                self.status.emit('User already registered.')

    def addDevice(self, username, deviceId, ATR):
        """! @brief Method to add a device to an account.
        @param self the Action instance
        @param username username of the account owner
        @param deviceId identifier of the device (smartcard or smartphone)
        @param ATR ATR of the card
        """
        if deviceId is None or ATR is None:
            self.status.emit('Please place a card in front of the reader.')
        else:
            if not username:
                self.status.emit('Please enter a username.')
            else:
                userWithDevice = self.users.find_one({"devices.uid": deviceId})
                if userWithDevice is None:
                    user = self.users.find_one({"username": username})

                    if user is None:
                        self.status.emit('This username doesn\'t exist.')
                    else:
                        status = STA_DEVICE_ACTIVE
                        activationDate = datetime.now()
                        category = 'smartcard'

                        # create the new device
                        newDevice = {"uid":deviceId, "status":status, "activationDate":activationDate, "ATR":ATR, "category":category}
                        # add the new device to the list
                        user['devices'].append(newDevice)
                        # remove the _id from user (required to make a $set)
                        del user['_id']
                        
                        # update user
                        query = {"uid": user['uid'] }
                        update = { "$set": user }
                        self.users.update(query, update)

                        self.status.emit('Device added to the user ' + user['name'] + ' ' + user['surname'] + '.')
                        self.piFace.actionValidated()
                else:
                    self.status.emit('This device already belongs to someone.')
