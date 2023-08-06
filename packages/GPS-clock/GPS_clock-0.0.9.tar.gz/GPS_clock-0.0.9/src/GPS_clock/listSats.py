# listSats by Andrew BARRON
import serial                    # Py serial use pip3 to install
import serial.tools.list_ports   # Py serial tools use pip3 to install - used to find current USB port
import numpy as np               # Used for radar plot polar to cartesian calcs  
from time import sleep           # used to catch up on rest after a hard day

vGNS = "GSV"
vGNS1 = "$GLGSV"
vGNS2 = "$GPGSV"
z=0
tlist=["","","","","","","","","","","","","",""]

vmark = 0
xmark = 0
origonx = 129
origony = 122
colour = "RED"
terminator = b'\xff\xff\xff'  # used to terminate every command
quote=b"\x22"                 # used to encase strings in quotes
device='/dev/ttyUSB0'         # this is the Nextion screen device - the program will track changes in the USB number
device2='/dev/ttyS0'          # this is the GPS device. If it says dev/ttyAMA0 the serial USB device is probably not working
Terminal ="YES"               # Set this to "YES" to turn on the terminal output. Anything else is Nextion output only.  

class Nextion:
   def __init__(self):
        self.ser = serial.Serial(device, 38400, timeout=1)

   def connect(self):
       self.ser.write(b"connect" + terminator)
       r = self.ser.read(128)
       return r

   def coms(self,command):
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
       

##########################################
def main():
  global xmark
  n.coms("pic 0,0,4")
  n.coms("page 5")
  while True:
    data = g.getGPS()
    # print(data)  # this is a bytearray type
    if data is not None:
        # convert bytearray to string
        data_string = "".join([chr(b) for b in data])
        #print(data_string, end="")
        vMessage=  data_string[3:6]
        if vMessage==vGNS:     
           #print(data_string, end="")
           part = data_string.split(",")
           vLen=len(part)
           vSats=part[3]
           vID=part[4]
           vCon=int(vID)
           dispID(vCon,vID)
           if vCon<33:
              vType=" GPS sat ID "
              vmark=1 
              n.set("page5.t1.txt=",vSats)
           elif vCon>32 and vCon<65:
              vType=" SBAS sat ID "
              print("SBAS")
              vmark=1 
           elif vCon>64 and vCon<97:
              vType=" Glonass sat ID "
              vmark=2 
              n.set("page5.t0.txt=",vSats)
           else:
              vType=" satellite ID "
              vmark=3 
           if not xmark==vmark:
              if Terminal =="YES":
                 print("*************************************")
           xmark=vmark
           vEL=part[5]
           vAZ=part[6]
           vRSSI=part[7]
           if vRSSI=="":
              vRSSI="*"   
           if '*' in vRSSI: 
              vOut=vSats +vType + vID +" Elevation "+ vEL +" Azimuth "+ vAZ  
           else: 
              vOut=vSats +vType + vID +" Elevation "+ vEL +" Azimuth "+ vAZ +" Signal "+ vRSSI   
           if Terminal =="YES":
              print(vOut)
           if vmark==1:
              display(vAZ,vEL,"RED") 
           elif vmark==2:
              display(vAZ,vEL,"GREEN") 
           else:
              display(vAZ,vEL,"YELLOW") 
           if vLen>8:  
              vID=part[8]
              vCon=int(vID)
              dispID(vCon,vID)
              if vCon>32 and vCon<65:
                 vType=" SBAS sat ID "
              vEL=part[9]
              vAZ=part[10]
              vRSSI=part[11]
              if vRSSI=="":
                 vRSSI="*"   
              if '*' in vRSSI: 
                 vOut=vSats +vType + vID +" Elevation "+ vEL +" Azimuth "+ vAZ  
              else: 
                 vOut=vSats +vType + vID +" Elevation "+ vEL +" Azimuth "+ vAZ +" Signal "+ vRSSI   
              if Terminal =="YES":
                 print(vOut)
              if vmark==1:
                 display(vAZ,vEL,"RED") 
              elif vmark==2:
                 display(vAZ,vEL,"GREEN") 
              else:
                 display(vAZ,vEL,"YELLOW") 
           if vLen>12:  
              vID=part[12]
              vCon=int(vID)
              dispID(vCon,vID)
              if vCon>32 and vCon<65:
                 vType=" SBAS sat ID "
              vEL=part[13]
              vAZ=part[14]
              vRSSI=part[15]
              if vRSSI=="":
                 vRSSI="*"   
              if '*' in vRSSI: 
                vOut=vSats +vType + vID +" Elevation "+ vEL +" Azimuth "+ vAZ  
              else: 
                 vOut=vSats +vType + vID +" Elevation "+ vEL +" Azimuth "+ vAZ +" Signal "+ vRSSI   
              if Terminal =="YES":
                 print(vOut)
              if vmark==1:
                 display(vAZ,vEL,"RED") 
              elif vmark==2:
                 display(vAZ,vEL,"GREEN") 
              else:
                 display(vAZ,vEL,"YELLOW") 
           if vLen>16:  
              vID=part[12]
              vCon=int(vID)
              dispID(vCon,vID)
              if vCon>32 and vCon<65:
                 vType=" SBAS sat ID "
              vEL=part[13]
              vAZ=part[14]
              vRSSI=part[15]
              if vRSSI=="":
                 vRSSI="*"   
              if '*' in vRSSI: 
                vOut=vSats +vType + vID +" Elevation "+ vEL +" Azimuth "+ vAZ  
              else: 
                 vOut=vSats +vType + vID +" Elevation "+ vEL +" Azimuth "+ vAZ +" Signal "+ vRSSI   
              if Terminal =="YES":
                 print(vOut)
              if vmark==1:
                 display(vAZ,vEL,"RED") 
              elif vmark==2:
                 display(vAZ,vEL,"GREEN") 
              else:
                 display(vAZ,vEL,"YELLOW") 

########################################## 
def display(AZ,EL,colour):
    global z
    az=float(AZ)-90
    el=(90-float(EL))*1.05
    #print("AZ "+str(az)+" EL "+str(el))
    rad= np.deg2rad(az)
    x = float(el) * np.cos(rad)
    y = float(el) * np.sin(rad)
    x+= origonx 
    y += origony
    xs=int(x)
    ys=int(y)
    comm="cirs "+str(xs)+","+str(ys)+",3,"+colour
    n.coms(comm)
    #print(comm)
    z+=1
    #if z==50:
    #   z=0
    #   n.coms("pic 0,0,4")
##########################################
def dispID(vCon,vID):
    global tlist
    if vCon<65:
       tlist[13]=tlist[11]
       tlist[11]=tlist[9]
       tlist[9]=tlist[7]
       tlist[7]=tlist[5]
       tlist[5]=tlist[3]
       tlist[3]=vID
       n.set("page5.t3.txt=",tlist[3])  
       n.set("page5.t5.txt=",tlist[5])  
       n.set("page5.t7.txt=",tlist[7])  
       n.set("page5.t9.txt=",tlist[9])  
       n.set("page5.t11.txt=",tlist[11])  
       n.set("page5.t13.txt=",tlist[13])  
    if vCon>64:
       tlist[12]=tlist[10]
       tlist[10]=tlist[8]
       tlist[8]=tlist[6]
       tlist[6]=tlist[4]
       tlist[4]=tlist[2]
       tlist[2]=vID
       n.set("page5.t2.txt=",tlist[2])  
       n.set("page5.t4.txt=",tlist[4])  
       n.set("page5.t6.txt=",tlist[6])  
       n.set("page5.t8.txt=",tlist[8])  
       n.set("page5.t10.txt=",tlist[10])  
       n.set("page5.t12.txt=",tlist[12]) 


####################### this finds the acive USB port numer which will increment every time the USB dongle is plugged in. It resets to USB0 on reboot
def checkUSB():
   global device
   myports = [tuple(p) for p in list(serial.tools.list_ports.comports())]
   #print (myports)
   bob=str(myports[0:1])
   device=(bob[3:15])
   print(device)

checkUSB()
n=Nextion()
g=GPS()
main()


