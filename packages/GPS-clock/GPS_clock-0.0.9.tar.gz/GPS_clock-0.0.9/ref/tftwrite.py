'''
 *   Copyright (C) 2016 Alex Koren
 *
 *   This program is free software; you can redistribute it and/or modify
 *   it under the terms of the GNU General Public License as published by
 *   the Free Software Foundation; either version 2 of the License, or
 *   (at your option) any later version.
 *
 *   This program is distributed in the hope that it will be useful,
 *   but WITHOUT ANY WARRANTY; without even the implied warranty of
 *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *   GNU General Public License for more details.
 *
 *   You should have received a copy of the GNU General Public License
 *   along with this program; if not, write to the Free Software
 *   Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
'''

import serial
import time
import sys
import os
import re

e = b"\xff\xff\xff"
#device='/dev/ttyS0'   #Serial UART0
#device='/dev/ttyAMA0' #Serial UART1
device='/dev/ttyUSB0'   # Serial USB
file=b"GPS_clock.tft"

def getBaudrate(ser, fSize=None, checkModel=None):
    for baudrate in (38400, 115200, 9600, 2400, 4800, 19200, 38400, 57600, 115200):
        ser.baudrate = baudrate
        ser.timeout = 3000 / baudrate + .2
        print(('Trying with baudrate: ' + str(baudrate) + '...'))
        ser.write(b"\xff\xff\xff")
        ser.write(b'connect')
        ser.write(b"\xff\xff\xff")
        r = ser.read(128)
        rstr = ser.read(128).decode('utf-16')
        if b'comok' in r:
            print(('Connected with baudrate: ' + str(baudrate) + '...'))
            noConnect = False
            print(r)
            #status, unknown1, model, fwversion, mcucode, serial, flashSize = r.strip('\xff\x00').split(',')
            status = r[6:7].decode()
            model= r[16:26].decode()
            fwversion = r[32:34].decode()
            mcucode = r[35:40].decode() 
            serial = r[41:57].decode()
            flashSize = r[58:65].decode()
            flashMem = int(flashSize)
            if status == "1":
                print('Touchscreen: yes')
            else:
                print('Touchscreen: no')
            print(('Model: ' + model))
            print(('Firmware version: ' + fwversion))
            print(('MCU code: ' + mcucode))
            print(('Serial: ' + serial))
            print(('Flash size: ' + flashSize))
            if fSize and fSize > flashMem:
                print('File too big!')
                return False
            if checkModel and not checkModel in model:
                print('Wrong Display!')
                return False
            print()
            print()
            return True
        else:
            print('Display not responding - reboot')
    return False

def setDownloadBaudrate(ser, fSize, baudrate):
    ser.write(b"")
    print('Writing *******')
    bob = ("whmi-wri " + str(fSize) + "," + str(baudrate) + ",0").encode()
    #print(bob)
    ser.write(bob)
    ser.write(b"\xff\xff\xff")
    time.sleep(.05)
    ser.baudrate = baudrate
    ser.timeout = .5
    #print("ready to read")
    print()
    r = ser.read(1)
    if b"\x05" in r:
        return True
    return False

def transferFile(ser, filename, fSize):
    with open(filename, 'rb') as hmif:
        dcount = 0
        while True:
            data = hmif.read(4096)
            if len(data) == 0:
                break
            dcount += len(data)
            ser.timeout = 5
            ser.write(data)
            sys.stdout.write('\rDownloading, %3.1f%%...'% (dcount / float(fSize) * 100.0))
            sys.stdout.flush()
            ser.timeout = .5
            time.sleep(0.5)
            r = ser.read(1)
            #print(dcount)
            if b"\x05" in r:
                continue
            else:
                #print("OUT")
                return False
                break
        print()
    return True

def upload(ser, filename, checkModel=None):
    if not getBaudrate(ser, os.path.getsize(filename), checkModel):
        print('Could not find baudrate')
        exit(1)

    if not setDownloadBaudrate(ser, os.path.getsize(filename), 115200):
        print('Could not set download baudrate')
        print()
        print('*****************************************************************')
        print('* Press nextion display to wake it up - then run tftwrite again *')
        print('*****************************************************************')
        exit(1)

    if not transferFile(ser, filename, os.path.getsize(filename)):
        print('Could not transfer file')
        exit(1)

    print('File transferred successfully')
    exit(0)

if __name__ == "__main__":
    if len(sys.argv) != 4 and len(sys.argv) != 3:
        print('usage:\npython nextion.py file_to_upload.tft /path/to/dev/ttyDevice [nextion_model_name]\
        \nexample: nextion.py newUI.tft /dev/ttyUSB0 NX3224T024\
        \nnote: model name is optional')
        ser = serial.Serial(device, 38400, timeout=5)
        upload(ser, file, None)
        exit(1)

    try:
        ser = serial.Serial(sys.argv[2], 38400, timeout=5)
    except serial.serialutil.SerialException:
        print(('could not open serial device ' + sys.argv[2]))
        exit(1)
    if serial.VERSION <= "3.0":
        if not ser.isOpen():
            ser.open()
    else:
        if not ser.is_open:
            ser.open()

    checkModel = None
    if len(sys.argv) == 4:
        checkModel = sys.argv[3]
        pattern = re.compile("^NX\d{4}[TFK]\d{3}$")
        if not pattern.match(checkModel):
            print('Invalid model name. Please give a correct one (e.g. NX3224T024)')
            exit(1)
    upload(ser, sys.argv[1], checkModel)
