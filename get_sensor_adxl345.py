#!/usr/bin/env python3.7

# from https://github.com/ControlEverythingCommunity/ADXL345/blob/master/Python/ADXL345.py

# Distributed with a free-will license.
# Use it any way you want, profit or free, provided it fits in the licenses of its associated works.
# ADXL345
# This code is designed to work with the ADXL345_I2CS I2C Mini Module available from ControlEverything.com.
# https://www.controleverything.com/content/Accelorometer?sku=ADXL345_I2CS#tabs-0-product_tabset-2

import signal
import sys
import time
import struct

import smbus

assert len(sys.argv) == 2, "missing output file"
ofile = sys.argv[1]

# handle ctr-c
def signal_handler(sig, frame):
    print('done')
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)


sr = 3200
ADXL345_ADDRESS          = 0x53
ADXL345_REG_DEVID        = 0x00 # Device ID
ADXL345_REG_DATAX0       = 0x32 # X-axis data 0 (6 bytes for X/Y/Z)
ADXL345_REG_POWER_CTL    = 0x2D # Power-saving features control
ADXL345_REG_DATA_FORMAT  = 0x31
ADXL345_REG_BW_RATE      = 0x2C
ADXL345_DATARATE_0_10_HZ = 0x00
ADXL345_DATARATE_0_20_HZ = 0x01
ADXL345_DATARATE_0_39_HZ = 0x02
ADXL345_DATARATE_0_78_HZ = 0x03
ADXL345_DATARATE_1_56_HZ = 0x04
ADXL345_DATARATE_3_13_HZ = 0x05
ADXL345_DATARATE_6_25HZ  = 0x06
ADXL345_DATARATE_12_5_HZ = 0x07
ADXL345_DATARATE_25_HZ   = 0x08
ADXL345_DATARATE_50_HZ   = 0x09
ADXL345_DATARATE_100_HZ  = 0x0A # (default)
ADXL345_DATARATE_200_HZ  = 0x0B
ADXL345_DATARATE_400_HZ  = 0x0C
ADXL345_DATARATE_800_HZ  = 0x0D
ADXL345_DATARATE_1600_HZ = 0x0E
ADXL345_DATARATE_3200_HZ = 0x0F
ADXL345_RANGE_2_G        = 0x00 # +/-  2g (default)
ADXL345_RANGE_4_G        = 0x01 # +/-  4g
ADXL345_RANGE_8_G        = 0x02 # +/-  8g
ADXL345_RANGE_16_G       = 0x03 # +/- 16g


# Get I2C bus
bus = smbus.SMBus(1)

# condiguring the adxl345
bus.write_byte_data(ADXL345_ADDRESS, ADXL345_REG_BW_RATE, ADXL345_DATARATE_3200_HZ)
bus.write_byte_data(ADXL345_ADDRESS, ADXL345_REG_POWER_CTL, 0x08)
bus.write_byte_data(ADXL345_ADDRESS, ADXL345_REG_DATA_FORMAT, ADXL345_RANGE_2_G)

with open(ofile, "w") as f:
    while 1:

        initial_time = time.perf_counter()
        data = bus.read_i2c_block_data(ADXL345_ADDRESS, ADXL345_REG_DATAX0, 6)
        # X, Y, Z = struct.unpack('<hhh', data)
        X = (data[0] << 8 | data[1]) >> 4
        Y = (data[2] << 8 | data[3]) >> 4
        Z = (data[4] << 8 | data[5]) >> 4

        if X > 511 :
        	X -= 1024

        if Y > 511 :
        	Y -= 1024

        if Z > 511 :
        	Z -= 1024

        f.write("{} {} {} {}\n".format(initial_time, X, Y, Z))
        ending_time = time.perf_counter()
        sleep_time = 1.0/sr - (ending_time - initial_time) if 1.0/sr > (ending_time - initial_time) else 0.0
        time.sleep(sleep_time)

