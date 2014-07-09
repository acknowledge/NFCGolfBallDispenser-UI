#!/usr/bin/env python
# -*- coding: utf-8 -*-

## @file constants.py
#  File for constants.
 
## @package constants
#  Constants.
#  @author CASAS Jacky
#  @date 22.06.2014
#  @version 1.0

## dispenser identifier, generate a new one for each dispenser
DISPENSER_ID = '84448f2c-f1e8-46db-a637-b813c1e2dd2a'

## username for the admin
ADMIN_USERNAME = 'admin'
## password for the admin
ADMIN_PASSWORD = 'asdf'

## transaction type for a recharge
RECHARGE = 0
## transaction type for a withdrawal
WITHDRAWAL = 1

## user statement active
STA_USER_ACTIVE = 1
## user statement inactive
STA_USER_INACTIVE = 2
## user statement deleted
STA_USER_DELETED = 3

## device status active
STA_DEVICE_ACTIVE = 1
## device status lost
STA_DEVICE_LOST = 2
## device status stolen
STA_DEVICE_STOLEN = 3
## device status deleted
STA_DEVICE_DELETED = 4

## default smartphone id
DEFAULT_SMARTPHONE_ID = 'AA AA AA AA'

## warning no account
WARN_NO_ACCOUNT = 0
## warning account inactive
WARN_ACCOUNT_INACTIVE = 1
## warning account deleted
WARN_ACCOUNT_DELETED = 2
## warning device lost
WARN_DEVICE_LOST = 3
## warning device stolen
WARN_DEVICE_STOLEN = 4
## warning device deleted
WARN_DEVICE_DELETED = 5

## APDU to read reader firmware version
READER_FIRMWARE_VERSION = [0xFF, 0x00, 0x48, 0x00, 0x00] 
## APDU to get device UID
GET_UID = [0xFF, 0xCA, 0x00, 0x00, 0x00]

## beginning of the APDU to get Android UID
CLA_INS_P1_P2 = [0x00, 0xA4, 0x04, 0x00]
## Android AID, part of the APDU to get Android UID
AID_ANDROID = [0xF0, 0x01, 0x02, 0x03, 0x03, 0x02, 0x01]
#AID_ANDROID = [0xF0, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06]
