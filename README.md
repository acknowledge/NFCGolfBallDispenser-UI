NFCGolfBallDispenser-UI
=======================

User Interface of the NFC Golf Ball Dispenser Project


## Context

This software is the main part of the *NFC Golf Ball Dispenser* project. It is made to run on a computer or embedded system (like a Raspberry Pi) with a Linux OS installed.

- Plug a display
- Plug a NFC reader in a USB port. For the project I use a ACR122U from Advanced Card Systems Ltd.
- Use a NFC smartcard to interact with the reader. For example a Mifare smartcard like the Mifare 1K.
- If you use a Raspberry Pi, you can plug a PiFace Digital module for the I/O (buttons + leds)

This software communicate with a MongoDB database. If the database is local it's ok, but if it's remote, you have to create a SSH tunnel between the Raspberry Pi and the server.


## Installation

You have to install *PySide* with the command :

    sudo apt-get install python-pyside

Then install *pip* :

    sudo apt-get install python-pip

And then install the Python libraries with :

    sudo pip install -r requirements.txt

To build the SSH tunnel, here's a hint :

    ssh -L 28082:localhost:27017 [remoteUser@remoteIP]

And finally you can launch the software :

    cd path/to/project
    python main.py
    

## Dependencies

This software can run alone, but if you want to accept the transactions with an Android smartphone, you have to watch the two related repositories that you can access with these links :

- The Python APIs for the server : [NFCGolfBallDispenser-API](https://github.com/acknowledge/NFCGolfBallDispenser-API)
- The Android application : [NFCGolfBallDispenser-AndroidApp](https://github.com/acknowledge/NFCGolfBallDispenser-AndroidApp)
