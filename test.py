import os
import time
from dynamixel_sdk import *                    # Uses Dynamixel SDK library

# Dynamixel settings
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

# Set Dynamixel goal velocity
dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, DXL_ID, ADDR_MX_GOAL_VELOCITY, DXL_MOVING_SPEED)
if dxl_comm_result != COMM_SUCCESS:
    print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
elif dxl_error != 0:
    print("%s" % packetHandler.getRxPacketError(dxl_error))
else:
    print("Goal velocity set")

# Wait for a bit
time.sleep(2)

# Disable Dynamixel Torque
dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL_ID, ADDR_MX_TORQUE_ENABLE, TORQUE_DISABLE)
if dxl_comm_result != COMM_SUCCESS:
    print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
elif dxl_error != 0:
    print("%s" % packetHandler.getRxPacketError(dxl_error))
else:
    print("Torque disabled")

# Close port
portHandler.closePort()
