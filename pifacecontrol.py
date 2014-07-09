#!/usr/bin/env python
# -*- coding: utf-8 -*-

## @file pifacecontrol.py
#  Contains the classe PiFaceControl.

## @package pifacecontrol
#  Control of the PiFace Digital module.
#  @author CASAS Jacky
#  @date 22.06.2014
#  @version 1.0

from time import sleep
import imp # to check if a module exists
from PySide.QtCore import *

DELAY = 0.2 #seconds
LONG_DELAY = 0.7

class PiFaceControl(QObject):
    """! @brief
    Control of the PiFace Digital module.
    @author CASAS Jacky
    @date 22.06.14
    @version 1.0
    """
    ## Signal from the button 1
    b1 = Signal()
    ## Signal from the button 2
    b2 = Signal()
    ## Signal from the button 3
    b3 = Signal()
    ## Signal from the button 4
    b4 = Signal()

    def __init__(self):
        """! @brief Initialize the instance if the module is connected.
        @param self the PiFaceControl instance
        """
        QObject.__init__(self)
        try:
            imp.find_module('pifacedigitalio')
            ## tell if the module PiFaceDigital is connected or not
            self.moduleFound = True
            import pifacedigitalio
            ## exportation of the library in the class
            self.pifacedigitalio = pifacedigitalio
            ## instance of PiFaceDigital, access to the leds
            self.pfd = pifacedigitalio.PiFaceDigital()
            for i in range(2, 8):
                self.pfd.leds[i].turn_off()
            ## constant of the library for the falling edge detection
            self.fallingEdge = pifacedigitalio.IODIR_FALLING_EDGE
            ## tell if the button listener is activated or not
            self.listenerActivated = False
        except ImportError:
            print 'The module pifacedigitalio is not installed'
            self.moduleFound = False
            
    def button1Pressed(self, event):
        """! @brief Method called when button 1 is pressed.
        @param self the PiFaceControl instance
        @param event the event that trigger that method call
        """
        self.b1.emit()
    
    def button2Pressed(self, event):
        """! @brief Method called when button 2 is pressed.
        @param self the PiFaceControl instance
        @param event the event that trigger that method call
        """
        self.b2.emit()
    
    def button3Pressed(self, event):
        """! @brief Method called when button 3 is pressed.
        @param self the PiFaceControl instance
        @param event the event that trigger that method call
        """
        self.b3.emit()
		
    def button4Pressed(self, event):
        """! @brief Method called when button 4 is pressed.
        @param self the PiFaceControl instance
        @param event the event that trigger that method call
        """
        self.b4.emit()

    def actionValidated(self):
        """! @brief Method called when an action is validated. It makes a moving line of LEDs.
        @param self the PiFaceControl instance
        """
        if self.moduleFound:
            self.pfd.leds[7].turn_on()
            sleep(DELAY)
            self.pfd.leds[6].turn_on()
            sleep(DELAY)
            self.pfd.leds[5].turn_on()
            self.pfd.leds[7].turn_off()
            sleep(DELAY)
            self.pfd.leds[4].turn_on()
            self.pfd.leds[6].turn_off()
            sleep(DELAY)
            self.pfd.leds[3].turn_on()
            self.pfd.leds[5].turn_off()
            sleep(DELAY)
            self.pfd.leds[2].turn_on()
            self.pfd.leds[4].turn_off()
            sleep(DELAY)
            self.pfd.leds[3].turn_off()
            sleep(DELAY)
            self.pfd.leds[2].turn_off()
            sleep(DELAY)
            self.pfd.leds[2].turn_off()

    def actionDenied(self):
        """! @brief Method called when an action is denied. It makes LED blinks.
        @param self the PiFaceControl instance
        """
        if self.moduleFound:
            for i in range(2, 8):
                self.pfd.leds[i].turn_on()
            sleep(DELAY)
            for i in range(2, 8):
                self.pfd.leds[i].turn_off()
            sleep(DELAY)
            for i in range(2, 8):
                self.pfd.leds[i].turn_on()
            sleep(DELAY)
            for i in range(2, 8):
                self.pfd.leds[i].turn_off()

            sleep(LONG_DELAY)

            for i in range(2, 8):
                self.pfd.leds[i].turn_on()
            sleep(DELAY)
            for i in range(2, 8):
                self.pfd.leds[i].turn_off()
            sleep(DELAY)
            for i in range(2, 8):
                self.pfd.leds[i].turn_on()
            sleep(DELAY)
            for i in range(2, 8):
                self.pfd.leds[i].turn_off()
                
    @Slot()
    def activateButtonListener(self):
        """! @brief Slot called to activate the buttons listener.
        @param self the PiFaceControl instance
        """
        if self.moduleFound:
            if self.listenerActivated == False:
                # create new instances of the listener
                ## listener fot the button 1
                self.listener1 = self.pifacedigitalio.InputEventListener(chip=self.pfd)
                ## listener fot the button 2
                self.listener2 = self.pifacedigitalio.InputEventListener(chip=self.pfd)
                ## listener fot the button 3
                self.listener3 = self.pifacedigitalio.InputEventListener(chip=self.pfd)
                ## listener fot the button 4
                self.listener4 = self.pifacedigitalio.InputEventListener(chip=self.pfd) 
                # registration of the button to the listener
                self.listener1.register(0, self.fallingEdge, self.button1Pressed)
                self.listener2.register(1, self.fallingEdge, self.button2Pressed)
                self.listener3.register(2, self.fallingEdge, self.button3Pressed)
                self.listener4.register(3, self.fallingEdge, self.button4Pressed)
                # activation of the listening
                self.listener1.activate()
                self.listener2.activate()
                self.listener3.activate()
                self.listener4.activate()
                self.listenerActivated = True
	
    @Slot()	
    def deactivateButtonListener(self):
        """! @brief Slot called to activate the buttons listener.
        @param self the PiFaceControl instance
        """
        if self.moduleFound:
            if self.listenerActivated == True:
                # deactivation of the listening, kill the threads
                self.listener1.deactivate()
                self.listener2.deactivate()
                self.listener3.deactivate()
                self.listener4.deactivate()
                self.listenerActivated = False
