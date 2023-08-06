'''
 *   Copyright (C) 2022 Andrew Barron
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
import serial                    # Py serial use pip3 to install
import serial.tools.list_ports   # Py serial tools use pip3 to install
import time			 # time used for delays
from threading import Thread     # used to create program threads

# sets the initial values for global variables. Stops errors caused by variables being called before they are set in another thread.
terminator = b'\xff\xff\xff'  # used to terminate every command
quote=b"\x22"                 # used to encase strings in quotes
vDatef ="0"                   # initial value dd/mm/yy or mm/dd/yy format
vTimef="0"                    # initial value 24 or 12 hour time format
vGridf="0"                    # initial value 6 or 8 digit grid
vDate=""	              # initial value for the date	
Uoff=13	                      # initial value for UTC offset
vLat="42.497 S"               # initial value for Latitude
vLon="72.605 E"               # initial value for Longitude
vGrid=""                      # initial value for Maidenhead grid
vSpeed="0"                    # initial value for speed
vBearing="0"                  # initial value for bearing
vAlt="0"                      # initial value for altitude
vData=""                      # initial value for data recieved from the GPS module 
aData=""                      # initial value for $GPGGA data string from getGPS() to dispGPS()
pData=""                      # initial value for $GPRMC data string from getGPS() to dispGPS()
vNMEA="no data received"      # initial value for Information string
vDadd=0                       # used to add or subtract a day to the date if local date is different to UTC date from GPS
page=0                        # initial value for Nextion page
LCLtime="00:00:00"            # initial value for local time
UTCtime="00:00:00"            # initial value for UTC time
device='/dev/ttyUSB0'         # this is the Nextion screen device - the program will track changes in the USB number
device2='/dev/ttyS0'          # this is the GPS device. Might be dev/ttyAMA0 or /dev/serial0

##################################
class Nextion:
   def __init__(self):
        checkUSB()
        self.ser = serial.Serial(device, 38400, timeout=1)

   def connect(self):
       self.ser.write(b"connect" + terminator)
       r = self.ser.read(128)
       return r

   def get(self,command):
       self.ser.write(command.encode() + terminator)
       r = self.ser.readline()
       #print(r)
       if b'p' in r:  # text
          vtxt= str(r[1:12])
          return vtxt
       #if b'q' in r:  # a number
       #  vnum=int.from_bytes(r[1:2],"little")
       #   return vnum
       return 0

   def set(self,command, var):
       self.ser.write(command.encode() + quote + var.encode() +quote + terminator)

##################################
class GPS:
   def __init__(self):
        self.gps = serial.Serial(device2, 9600, timeout=1)

   def getGPS(self):
       raw = self.gps.readline()
       return raw
       

####################### this finds the acive USB port numer which will increment every time the USB dongle is plugged in. It resets to USB0 on reboot
def checkUSB():
   global device
   myports = [tuple(p) for p in list(serial.tools.list_ports.comports())]
   #print (myports)
   bob=str(myports[0:1])
   device=(bob[3:15])
   print(device)
####################### reads the Nextion buttons and UTC offset from the display. Takes about 1 second.
def getData():
   global Uoff, page, vDatef, vTimef, vGridf
   vt=page
   while True:
      data=n.get("get page4.vstring.txt")
      if not '\xff' in data: 
         #print(data)   
         part = data.split(",")
         vdatef=part[0]
         vDatef=vdatef[2]
         vTimef=part[1]
         vGridf=part[2]
         Uoff=int(part[3])
         page=int(part[4])
         Uoff-=13
         #print("UTC offset " + str(Uoff))
         #print(vDatef+" "+vTimef+" "+vGridf) 
#######################
def setData():
   while True:
      if page==0 or page==1:
        n.set("page0.lTime.txt=",LCLtime)
        n.set("page0.uTime.txt=",UTCtime)
        n.set("page1.lTime.txt=",LCLtime)
        n.set("page1.uTime.txt=",UTCtime)
        n.set("page1.lDate.txt=",vDate)
        time.sleep(.5)
      if page==2:
        #print("setData page " +str(page))
        #print("setData grid " +vGrid)
        n.set("page2.Maiden.txt=",vGrid)
        n.set("page2.t20.txt=",vLat)
        n.set("page2.t21.txt=",vLon)
        time.sleep(1)
      if page==3:
        #print("setData page " +str(page))
        n.set("page3.NMEA.txt=",vNMEA)
        n.set("page3.tsat.txt=",vSats)
        n.set("page3.tspeed.txt=",vSpeed)
        n.set("page3.tnth.txt=",vBearing)
        n.set("page3.talt.txt=",vAlt)
        time.sleep(1)
      if page==4:
        #print("setData page " +str(page))
        time.sleep(1)
        pass

#######################
def initialise():
    global page
    r=n.connect()
    #print(r)
    if b'comok' in r:
            print('Connected')
            noConnect = False
            ## string format = status, unknown1, model, fwversion, mcucode, serial, flashSize = r.strip('\xff\x00').split(',')
            status = r[6:7].decode()
            model= r[16:31].decode()
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
            n.set("page0.t2.txt=","UTC") # set text on page 0
            n.get("sleep=0")  # wake up display
            page=n.get("sendme")
    else:
            print('Display not responding - reboot')
    print("Initialised")
    print()

#######################
def getGPS():
    print("get GPS")
    global UTCtime, LCLtime, aData, pData, page, vDadd
    while True:
      mbytes = g.getGPS()
      if len(mbytes)>0: 
          vData = mbytes.decode()  
          vMessage = vData[0:6]
          #print(vMessage)
          if (vMessage == "$GPRMC" or vMessage == "$GNRMC"):   # Get the position data that was transmitted with the GPRMC message
             pData=vData 
             #print(vMessage)
          if (vMessage == "$GPGGA" or vMessage == "$GNGGA"):   # Get the position data that was transmitted with the GPGGA message
             aData=vData
             if page==0 or page==1:    # format UTC and find Local Time
                parts = aData.split(",")
                utime=parts[1]
                UTCtime= utime[0:2]+":"+utime[2:4]+":"+utime[4:6] # format UTC time
                hrs=int(utime[0:2])+Uoff  # apply the UTC offset to find the Local time
                vDadd =0               
                if hrs < 0:               # reset if the UTC offset create a time less than 0
                   hrs = hrs + 24
                   vDadd =-1              # local date different to UTC date
                if hrs > 24:              # reset if the UTC offset create a time over 24 hours
                   hrs = hrs - 24
                   vDadd =1               # local date different to UTC date
                if vTimef =="1":          # If 12 hour clock set AM or PM
                   if hrs > 12:
                      hrs=hrs-12
                      shrs = str(hrs)
                      LCLtime = shrs +":"+utime[2:4]+" PM" 
                   else:
                      shrs = str(hrs)
                      LCLtime = shrs +":"+utime[2:4]+" AM" 
                else:
                   shrs = str(hrs)
                   LCLtime = shrs +":"+utime[2:4]+":"+utime[4:6] # format 24 hour Local time
             time.sleep(0.5)
      else:
          vSats="00"
####################### dispGPS() displays the date, grid, lat, lon, NMEA text, vDadd
def dispGPS(): 
      print("disp GPS")
      global vDate, vLat, vLon, vNMEA, vSats, vSpeed, vBearing, vAlt
      #print(aData)
      #print(pData)
      vDate="0"
      vspeed="0.00"
      vSats="00"
      vAlt="0"
      vbearing="0.00"
      speed=1.234
      bearing=1.234 #???
      lst = [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00]
      lstb = [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00]
      while True: 
         vRec1=0
         vRec2=0
         # do GPS magic
         vMessage = aData[0:6]
         #print(vMessage)
         if (vMessage == "$GPGGA" or vMessage == "$GNGGA"):   # Get the position data that was transmitted with the GPGGA message
            parts = aData.split(",")
            vSats= parts[7]
            if(vSats!="00"):
              vRec1=1  
            vlonf = formatDegreesMinutes(parts[4], 3)
            vlonr = round(vlonf,3)
            vLon=str(vlonr)+" "+parts[5]
            vlatf = formatDegreesMinutes(parts[2], 2)
            vlatr = round(vlatf,3)
            vLat=str(vlatr)+" "+parts[3]
            #print ("Your position: lon = " + str(vLon) + ", lat = " + str(vLat))
            vAlt=parts[9]
            if page==2:
               calcGrid(vlonf,vlatf, parts[5],parts[3])  ## calculate the grid

         vMessage = pData[0:6]
         if (vMessage == "$GPRMC" or vMessage == "$GNRMC"):   # Get the position data that was transmitted with the GPRMC message
             parts = pData.split(",")
             #print(pData)
             valid=parts[2]
             if(valid=="A"):
                vRec2=1  
             vspeed=parts[7]
             vbearing=parts[8]
             if vbearing=="":
                vbearing=0 
             vdate=parts[9]
             dd=vdate[0:2]
             mm=vdate[2:4]
             yy=vdate[4:6]
             d=int(dd)+vDadd
             m=int(mm)
             if d>31:
                d=1
                m=m+1
             if d<1:
                d=31
                m=m-1
             dd=str(d)
             mm=str(m)  
             if d<10:
                dd="0"+str(d)
             if m<10:
                mm="0"+str(m)

             if vDatef =="1":
                vDate=mm+"/"+dd+"/"+yy
             else:  
               vDate=dd+"/"+mm+"/"+yy
             #print("date "+vDate) 
             # convert speed to kph and mph
             lst[9]=lst[8]
             lst[8]=lst[7]
             lst[7]=lst[6]
             lst[6]=lst[5]
             lst[5]=lst[4]
             lst[4]=lst[3]
             lst[3]=lst[2]
             lst[2]=lst[1]
             lst[1]=lst[0]
             lst[0]=float(vspeed)
             speed = Average(lst)
             kph=round(speed*1.852,1)
             mph=round(speed*1.15078,1)
             vSpeed=(str(kph)+" kph  "+str(mph)+" mph")

             # average bearing
             lstb[9]=lstb[8]
             lstb[8]=lstb[7]
             lstb[7]=lstb[6]
             lstb[6]=lstb[5]
             lstb[5]=lstb[4]
             lstb[4]=lstb[3]
             lstb[3]=lstb[2]
             lstb[2]=lstb[1]
             lstb[1]=lstb[0]
             lstb[0]=float(vbearing)
             vBearing = str(round(Average(lstb),1))
             #print("Bearing "+str(vbearing)+" averaged "+str(vBearing))
             time.sleep(0.5)
         if(vRec1==1 and vRec2==1):
            vNMEA="GGA and RMC received"
         elif(vRec1==1):
            vNMEA="GGA received"
         elif(vRec2==1):
            vNMEA="RMC received"
         else: 
            vNMEA="Waiting for GPS lock"  
#######################
def formatDegreesMinutes(coordinates, digits):
              # In the NMEA message, the position gets transmitted as: DDMM.MMMMM, where DD denotes the degrees and MM.MMMMM denotes
              # the minutes. However, I want to convert this format to the following: DD.MMMM. This method converts a transmitted string to the desired format
    #print(coordinates)
    #print(digits)

    parts = coordinates.split(".")
    if (len(parts) != 2):
        #print("no coordinates")
        return 0

    if (digits > 3 or digits < 2):
        #print("coordinates length error")
        return 0
    
    degs = coordinates[:digits]
    y=int(degs)
    mins= (coordinates[digits:digits+7])
    x = round(float(mins)/60,6)
    degrees=(y+x)
    #print(degrees)
    return degrees
####################### Python program to get average of a list
def Average(lst):
    return sum(lst) / len(lst)
  
#######################
def calcGrid(vlon,vlat,ew, ns):
    global vGrid, vGridf
    if(ew=="W"):
      vlon=-vlon
    if(ns=="S"):
      vlat=-vlat
    #vlat=42.664048 # test FN42ep09
    #vlon=-71.661962 # test
    vlon1=vlon+180
    vlon2=vlon1/20
    out1=int(vlon2)
    rem1=vlon1-(out1*20)
    vlon3=rem1/2
    out3=int(vlon3)
    rem2=rem1-(out3*2)
    vlon4=rem2/0.083333
    out5=int(vlon4)
    rem3=rem2-(out5*0.083333)
    vlon5=(rem3/0.0083333)
    out7=int(vlon5)

    vlat1=vlat+90
    vlat2=vlat1/10
    out2=int(vlat2)
    vlat3=vlat1-(out2*10)
    out4=int(vlat3)
    rem2=vlat3-out4
    vlat4=rem2/0.0416665
    out6=int(vlat4)
    rem3=rem2-(out6*0.0416665)
    vlat5=(rem3/0.00416665)
    out8=int(vlat5)
    if(vGridf=="1"):    # sort out 6 digit or 8 digit Maidenhead grid 
        vGrid=chr(out1+65)+chr(out2+65)+str(out3)+str(out4)+chr(out5+97)+chr(out6+97)+str(out7)+str(out8)
    else:
        vGrid=chr(out1+65)+chr(out2+65)+str(out3)+str(out4)+chr(out5+97)+chr(out6+97)
 
#######################
def main():
   initialise()
   time.sleep(1)
   ### Threads ###
   print("Starting Threads")
   t1=Thread(target=getData)
   t2=Thread(target=setData)
   t3=Thread(target=getGPS)
   t4=Thread(target=dispGPS)


   t1.start()
   t2.start()
   t3.start()
   t4.start()



#######################
if __name__ == '__main__':
   n=Nextion()
   g=GPS()
   main()