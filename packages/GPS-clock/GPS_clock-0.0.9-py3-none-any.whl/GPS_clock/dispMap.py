# dispMap by Andrew BARRON
# this will display your position on a map preloaded onto the Nextion screen. You need to enter the top left and bottom right lat and lon 
# into the olat, olon, mlat and mlon variables

import serial                    # Py serial use pip3 to install
import serial.tools.list_ports   # Py serial tools use pip3 to install - used to find current USB port
import staticmaps                # use pip3 install py-staticmaps  to install - used to find a map of your location online RPI must have WiFi Internet access

Get_Map = "NO"                   # set to "YES" to download a map based on your coordinates. Note that this must be manually added to the Nextion screen using the Nextion editor.


mapx=310  # Enter the map size in pixels from the Nextion Editor
mapy=240

olat=83  # Enter the top left and bottom right coordinates
olon=164
mlat=-61
mlon=22
colour = "RED"
terminator = b'\xff\xff\xff'  # used to terminate every command
quote=b"\x22"                 # used to encase strings in quotes
device='/dev/ttyUSB0'         # this is the Nextion screen device - the program will track changes in the USB number
device2='/dev/ttyS0'          # this is the GPS device. Might be dev/ttyAMA0 or /dev/serial0


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
  global xmark, Get_Map
  n.coms("page 6")
  while True:
    data = g.getGPS()   # this is a bytearray type
    if data is not None:
        # convert bytearray to string
        data_string = "".join([chr(b) for b in data])
        vMessage=  data_string[0:6]
        if vMessage=="$GNRMC" or  vMessage=="$GPRMC":     # Find a "$GPRMC" NMEA string
           #print(data_string, end="")
           parts = data_string.split(",")
           vlatf = formatDegreesMinutes(parts[3], 2)
           if parts[4]=="S":
              vlatf=-vlatf
           vLat = str(round(vlatf,3))
           vlonf = formatDegreesMinutes(parts[5], 3)
           if parts[6]=="W":
              vlonf=-vlonf
           vLon = str(round(vlonf,3))
           if Get_Map == "YES":
              print("get a map")
              getMap(vlatf,vlonf)
              Get_Map = "NO"
           #print ("Your position: lon = " + vLon + ", lat = " + vLat)
           n.set("page6.t20.txt=",vLat) # print Lat
           n.set("page6.t21.txt=",vLon) # print Lon
           plot(vlatf,vlonf,colour)


           vlatf=51.50377  # London
           vlonf=-0.11740  # London
           plot(vlatf,vlonf,colour)
         
           vlatf=25.85850 # Miami
           vlonf=-80.19426  
           plot(vlatf,vlonf,colour)

           vlatf=34.03235 # LA
           vlonf=-118.25994  
           plot(vlatf,vlonf,colour)


#######################
def formatDegreesMinutes(coordinates, digits):
              # In the NMEA message, the position gets transmitted as: DDMM.MMMMM, where DD denotes the degrees and MM.MMMMM denotes
              # the minutes. However, I want to convert this format to the following: DD.MMMM. This method converts a transmitted string to the desired format
    #print(coordinates)
    #print(digits)

    parts = coordinates.split(".")
    if (len(parts) != 2):
        return coordinates

    if (digits > 3 or digits < 2):
        return coordinates
    
    degs = coordinates[:digits]
    y=int(degs)
    mins= (coordinates[digits:digits+7])
    x = round(float(mins)/60,6)
    degrees=(y+x)
    #print(degrees)
    return degrees
########################################## 
def plot(lat,lon,colour):
    global mapx,mapy,olat,olon,mlat,mlon
    #print(lat),print(lon)
    maplat=((lat-olat)/(mlat-olat))*mapy
    maplon=((lon-olon)/(mlon-olon))*mapx
    pixels=mapx/(360+mlon-olon)
    if lon>olon:
       maplon=(lon-olon)*pixels
    elif lon<0:
       maplon=(360-olon+lon)*pixels
    xs=int(maplon)
    ys=int(maplat)
    #print(maplat,maplon)
    #print(xs,ys)

    comm="cir "+str(xs)+","+str(ys)+",3,"+colour
    n.coms(comm)
    comm="cirs "+str(xs)+","+str(ys)+",2,"+"YELLOW"
    n.coms(comm)
    comm="cirs "+str(xs)+","+str(ys)+",1,"+colour
    n.coms(comm)


####################### this finds the acive USB port numer which will increment every time the USB dongle is plugged in. It resets to USB0 on reboot
def checkUSB():
   global device
   myports = [tuple(p) for p in list(serial.tools.list_ports.comports())]
   #print (myports)
   bob=str(myports[0:1])
   device=(bob[3:15])
   print(device)

########################
def getMap(vlatf,vlonf):
   context = staticmaps.Context()
   #context.set_tile_provider(staticmaps.tile_provider_StamenToner)        # Alternate map design (black)
   #context.set_tile_provider(staticmaps.tile_provider_ArcGISWorldImagery) # Alternate map design (photo)
   context.set_tile_provider(staticmaps.tile_provider_OSM)                 # Alternate map design (normal)

   center1 = staticmaps.create_latlng(vlatf,vlonf)
   zoom = 5000  # radius in km 1-5000km

   context.add_object(staticmaps.Circle(center1, zoom, fill_color=staticmaps.TRANSPARENT, color=staticmaps.WHITE, width=1))
   #context.add_object(staticmaps.Marker(center1, color=staticmaps.RED, size=6))
   print("This will take up to 60 seconds") 
   # render non-anti-aliased png
   image = context.render_pillow(320, 240)
   image.save("map.png")
   print("map.png saved") 
   print("Sadly you have to use the Nextion eitor to load it onto page 6")
   print("plotting")

checkUSB()
n=Nextion()
g=GPS()
main()


