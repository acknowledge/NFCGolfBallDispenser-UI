#!/usr/bin/env python
# -*- coding: utf-8 -*-

## @file database.py
#  Contains the classes SingletonType and DataBase.
 
## @package database
#  Communication with databases.
#  @author CASAS Jacky
#  @date 22.06.2014
#  @version 1.0

import pymongo

class SingletonType(type):
    """! @brief
    Singleton type. 
    @author CASAS Jacky
    @date 22.06.14
    @version 1.0
    """
    def __call__(cls, *args, **kwargs):
        """! @brief Override of the `__call__` method."""
        try:
            return cls.__instance
        except AttributeError:
            cls.__instance = super(SingletonType, cls).__call__(*args, **kwargs)
            return cls.__instance

class DataBase(object):
    """! @brief
    Modelisation of the database. This class is a singleton.
    @author CASAS Jacky
    @date 22.06.14
    @version 1.0
    """
    __metaclass__ = SingletonType

    def __init__(self):
        """! @brief
        The connection to the MongoDB database is made here. 
        """
        try:
            # local database
            client = pymongo.MongoClient('mongodb://localhost:27017/')
            
            # remote database (through SSH tunnel)
            #client = pymongo.MongoClient('mongodb://localhost:28082/') 

            db = client['golfBallDispenserDatas']

            ## variable containing the collection *user*
            self.user = db['user']
            ## variable containing the collection *transaction*
            self.transaction = db['transaction']

        except pymongo.errors.ConnectionFailure, e:
           print "Could not connect to MongoDB: %s" % e 
