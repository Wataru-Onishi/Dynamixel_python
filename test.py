import time
from dynamixel_sdk import *                    

# Dynamixel settings
DXL_ID_1 = 2                                    # Dynamixel ID 2
DXL_ID_2 = 3                                    # Dynamixel ID 3
BAUDRATE = 57600                                # Dynamixel default baudrate
DEVICENAME = '/dev/ttyUSB0'                     # Check your device port

# Protocol version
PROTOCOL_VERSION = 2.0

# Control table addresses
ADDR_MX_TORQUE_ENABLE = 64                     
ADDR_MX_GOAL_VELOCITY = 104                    

# Default settings
TORQUE_ENABLE = 1                              
TORQUE_DISABLE = 0                             
DXL_MOVING_SPEED = 100                         

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

# Enable Dynamixel Torque for both servos
for DXL_ID in [DXL_ID_1, DXL_ID_2]:
    dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL_ID, ADDR_MX_TORQUE_ENABLE, TORQUE_ENABLE)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))
    else:
        print(f"Torque enabled for Dynamixel ID: {DXL_ID}")

time.sleep(10)

# Set Dynamixel goal velocity for both servos
for DXL_ID in [DXL_ID_1, DXL_ID_2]:
    dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, DXL_ID, ADDR_MX_GOAL_VELOCITY, DXL_MOVING_SPEED)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))
    else:
        print(f"Goal velocity set for Dynamixel ID: {DXL_ID}")

# Wait for a bit
time.sleep(10)

# Disable Dynamixel Torque for both servos
for DXL_ID in [DXL_ID_1, DXL_ID_2]:
    dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL_ID, ADDR_MX_TORQUE_ENABLE, TORQUE_DISABLE)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))
    else:
        print(f"Torque disabled for Dynamixel ID: {DXL_ID}")

# Close port
portHandler.closePort()
