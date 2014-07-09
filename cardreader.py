#!/usr/bin/env python
# -*- coding: utf-8 -*-

## @file cardreader.py
#  Contains the classes DCCardType and CardReader.

## @package cardreader
#  Communication with a NFC Card Reader.
#  @author CASAS Jacky
#  @date 22.06.2014
#  @version 1.0

from smartcard.CardType import ATRCardType, CardType
from smartcard.CardRequest import CardRequest
from smartcard.util import toHexString, toBytes
from smartcard.CardConnection import CardConnection
from smartcard.CardConnectionObserver import ConsoleCardConnectionObserver, CardConnectionObserver
from smartcard.Exceptions import CardRequestTimeoutException
from smartcard.sw.ISO7816_4ErrorChecker import ISO7816_4ErrorChecker
from smartcard.sw.ISO7816_8ErrorChecker import ISO7816_8ErrorChecker
from smartcard.sw.ISO7816_9ErrorChecker import ISO7816_9ErrorChecker
from smartcard.sw.ErrorCheckingChain import ErrorCheckingChain
from smartcard.sw.SWExceptions import SWException
from smartcard.Card import Card

import sys
from string import replace
from PySide.QtCore import *
from constants import *
from action import Action
from ui import Frame

class DCCardType(CardType):
    """! @brief
    Direct Convention Card class. 
    @author CASAS Jacky
    @date 22.06.14
    @version 1.0
    """
    
    def matches(self, atr, reader=None):
        """! @brief Method that verify if the ATR begins with 0x38.
        @param self the DCCardType instance
        @param atr ATR of the card
        @param reader identifier of the reader, optional
        """
        return atr[0] == 0x3B

class CardReader(QObject):
    """! @brief
    All actions from and to the NFC card reader are handled here.
    @author CASAS Jacky
    @date 22.06.14
    @version 1.0
    """
    ## Signal used to update the waiting of a new card 
    updateWaiting = Signal()
    ## Signal used to display different warnings on the UI
    warning = Signal(int)
    ## Signal used to update UI when a card is detected
    cardDetected = Signal(int)

    def __init__(self, action):
        """! @brief Link an Action instance, create a cardrequest and a timer.
        @param self the CardReader instance
        @param action an instance of Action
        """
        QObject.__init__(self)
        ## DCCardType instance
        self.cardtype = DCCardType()
        ## card request to make a connection with a smartcard
        self.cardrequest = CardRequest(timeout=0.5, cardType=self.cardtype)
        
        ## link to an Action instance
        self.action = action
        ## timer used to update the waiting state
        self.timer = QTimer(self)
        ## identifier of the card when detected
        self.cardUid = None
        ## ATR of the card when dtected
        self.ATR = None
        
    @Slot()
    def start(self):
        """! @brief Slot used to start the update timer with 0.5 seconds.
        @param self the CardReader instance
        """
        self.timer.start(500)

    @Slot()
    def waitForCard(self):
        """! @brief Slot called every 0.5 seconds. If a card is detected, the card is read.
        @param self the CardReader instance
        """
        try:
            cardService = self.cardrequest.waitforcard()
            self.timer.stop()

            cardService.connection.connect()

            self.cardUid = self.getUID(cardService)
            self.ATR = self.getATR(cardService)

            account = self.action.getAccount(self.cardUid)
            
            if account is None:
                self.warning.emit(WARN_NO_ACCOUNT)
            else:
                if account['statement'] == STA_USER_ACTIVE:
                    for device in account['devices']:
                        if device['uid'] == self.cardUid:
                            if device['status'] == STA_DEVICE_ACTIVE:
                                # all is ok
                                self.cardDetected.emit(account['balance'])
                            elif device['status'] == STA_DEVICE_LOST:
                                self.warning.emit(WARN_DEVICE_LOST)
                            elif device['status'] == STA_DEVICE_STOLEN:
                                self.warning.emit(WARN_DEVICE_STOLEN)
                            elif device['status'] == STA_DEVICE_DELETED:
                                self.warning.emit(WARN_DEVICE_DELETED)
                            else:
                                self.warning.emit(WARN_DEVICE_DELETED)
                            break
                elif account['statement'] == STA_USER_INACTIVE:
                    self.warning.emit(WARN_ACCOUNT_INACTIVE)
                elif account['statement'] == STA_USER_DELETED:
                    self.warning.emit(WARN_ACCOUNT_DELETED)
                else:
                    self.warning.emit(WARN_ACCOUNT_DELETED)

        except CardRequestTimeoutException:
            self.updateWaiting.emit()
            # init variables
            self.cardUid = None
            self.ATR = None

    @Slot()
    def someBalls(self):
        """! @brief Slot called when we click on the button to get some balls. Make a transaction.
        @param self the CardReader instance
        """
        self.action.transaction(self.cardUid, 2)
        self.start()

    @Slot()
    def manyBalls(self):
        """! @brief Slot called when we click on the button go get many balls. Make a transaction.
        @param self the CardReader instance
        """
        self.action.transaction(self.cardUid, 5)
        self.start()

    @Slot(int)
    def recharge(self, amount):
        """! @brief Slot called when we want to recharge the account.
        @param self the CardReader instance
        @param amount the amount paid to the account
        """
        self.action.recharge(self.cardUid, amount)
        self.start()

    def myTransmit(self, connection, apdu):
        """! @brief Method that overrides the standard transmit method. It let us trace the command and response.
        @param self the CardReader instance
        @param connection the current connection with the card
        @param apdu the APDU we want to transmit
        """
        # trace request :
        #print 'sending : \t', toHexString(apdu)
        response, sw1, sw2 = connection.transmit( apdu )
        # trace response :
        #if None == response: response=[]
        #print 'response : \t', toHexString(response), '\nstatus words : \t', "%x %x" % (sw1, sw2)
        if sw1 in range(0x61, 0x6f):
            print "Error: sw1: %x sw2: %x" % (sw1, sw2)
        return response, sw1, sw2

    def getUID(self, cardService):
        """! @brief Method to get the UID of the smartcard or smartphone.
        @param self the CardReader instance
        @param cardService the current connection with the smartcard
        """
        try:
            # try to get ID from smartphone
            aidSize = [0x07]
            ending = [0x00]
            apdu = CLA_INS_P1_P2 + aidSize + AID_ANDROID + ending
            response, sw1, sw2 = self.myTransmit(cardService.connection, apdu)
            UID = toHexString(response)
            #apdu = [0x00]
            #response, sw1, sw2 = self.myTransmit(cardService.connection, apdu)
            #print 'esasdf : ', toHexString(response)
        except IndexError:
            # otherwise get ID from smartcard
            apdu = GET_UID
            response, sw1, sw2 = self.myTransmit(cardService.connection, apdu)
            UID = toHexString(response)
        return UID

    def getATR(self, cardService):
        """! @brief Method to get the ATR of the smartcard or smartphone.
        @param self the CardReader instance
        @param cardService the current connection with the smartcard
        """
        ATR = toHexString(cardService.connection.getATR())
        return ATR
