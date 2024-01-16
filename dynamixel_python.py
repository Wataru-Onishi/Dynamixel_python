# -*- coding: utf-8 -*-
from __future__ import division
import time
from pyPS4Controller.controller import Controller

import os
import time
from dynamixel_sdk import *

DXL_ID = 3                                     # Dynamixel ID
BAUDRATE = 57600                               # Dynamixel default baudrate
DEVICENAME = '/dev/ttyUSB0'                    # Check your device port


# Protocol version
PROTOCOL_VERSION = 2.0

# Control table addresses
ADDR_MX_TORQUE_ENABLE = 64                     # Control table address for torque enable
ADDR_MX_GOAL_VELOCITY = 104                    # Control table address for goal velocity

# Default settings
TORQUE_ENABLE = 1                              # Value to enable the torque
TORQUE_DISABLE = 0                             # Value to disable the torque
#DXL_MOVING_SPEED = 0                         # Dynamixel will rotate at this speed (value : 0~1023)

# Initialize PortHandler and PacketHandler instances
portHandler = PortHandler(DEVICENAME)
packetHandler = PacketHandler(PROTOCOL_VERSION)

# Open port
if portHandler.openPort():
    print("Port opened")
else:
    print("Failed to open the port")
    quit()

# Set port baudrate
if portHandler.setBaudRate(BAUDRATE):
    print("Baudrate set")
else:
    print("Failed to set the baudrate")
    quit()

# Enable Dynamixel Torque
dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL_ID, ADDR_MX_TORQUE_ENABLE, TORQUE_ENABLE)


def transf(raw):
    temp = raw/65534 * 2 * 10
    return round(temp, 1)

class MyController(Controller):

    def __init__(self, **kwargs):
        Controller.__init__(self, **kwargs)
    
    def on_R3_down(self, value):
        value = transf(value)
        if(abs(value) <1):
            DXL_MOVING_SPEED = 0
            dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL_ID, ADDR_MX_TORQUE_ENABLE, TORQUE_ENABLE)
            dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, DXL_ID, ADDR_MX_GOAL_VELOCITY, DXL_MOVING_SPEED)


        else:
            DXL_MOVING_SPEED = 100
            dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL_ID, ADDR_MX_TORQUE_ENABLE, TORQUE_ENABLE)
            dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, DXL_ID, ADDR_MX_GOAL_VELOCITY, DXL_MOVING_SPEED)
         





controller = MyController(interface="/dev/input/js0", connecting_using_ds4drv=False)
controller.listen()
