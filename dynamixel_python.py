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
DXL_MOVING_SPEED = 200                         # Dynamixel will rotate at this speed (value : 0~1023)

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
if dxl_comm_result != COMM_SUCCESS:
    print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
elif dxl_error != 0:
    print("%s" % packetHandler.getRxPacketError(dxl_error))
else:
    print("Torque enabled")




def transf(raw):
    temp = raw/65534 * 2 * 10
    return round(temp, 1)

class MyController(Controller):

    def __init__(self, **kwargs):
        Controller.__init__(self, **kwargs)
    
    def on_R3_down(self, value):
        value = transf(value)
        if(abs(value) <1):
            value = 0

        else:
            # Set Dynamixel goal velocity
            dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, DXL_ID, ADDR_MX_GOAL_VELOCITY, DXL_MOVING_SPEED)
            if dxl_comm_result != COMM_SUCCESS:
                print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
            elif dxl_error != 0:
                print("%s" % packetHandler.getRxPacketError(dxl_error))
            else:
                print("Goal velocity set")
            print(value)
            
    def on_R3_up(self, value):
        value = transf(value)
        if(abs(value) <1):
            value = 0

        else:
            # Set Dynamixel goal velocity
            dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, DXL_ID, ADDR_MX_GOAL_VELOCITY, DXL_MOVING_SPEED)
            if dxl_comm_result != COMM_SUCCESS:
                print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
            elif dxl_error != 0:
                print("%s" % packetHandler.getRxPacketError(dxl_error))
            else:
                print("Goal velocity set")
            print(value)
    
    def on_R3_y_at_rest(self):
        odrv0.axis0.controller.input_vel =0

    def on_circle_press(self):
        odrv0.axis0.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
    
    def on_x_press(self):
        odrv0.axis0.controller.input_vel = 0
        odrv0.axis0.requested_state = AXIS_STATE_IDLE
        exit()


controller = MyController(interface="/dev/input/js0", connecting_using_ds4drv=False)
controller.listen()
