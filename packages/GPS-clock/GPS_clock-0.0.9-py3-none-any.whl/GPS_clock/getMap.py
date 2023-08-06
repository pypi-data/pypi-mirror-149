import staticmaps
import numpy as np

# Latitude: 1 deg = 110.574 km
# Longitude: 1 deg = 111.320*cos(latitude) km

yourLat = 10  # Enter centre Latitude in degrees 
yourLon = -85  # Enter centre Longitude in degrees

screenx = 320.0
screeny = 240.0
zoomx = 9200       # x dimension in km (approx)
zoomy=zoomx*(screeny/screenx)
lonx = 111.32*np.cos(np.radians(yourLat))
lonxd = (zoomx/lonx)/2
laty = 110.574
latyd =(zoomy/laty)/2
xleft = round(yourLon-lonxd,4)
xright = round(yourLon+lonxd,4)
ytop = round(yourLat+latyd,4)
ybottom = round(yourLat-latyd,4)

if xleft<-180:
   xleft=-180
if xright>180:
   xright=180
if ytop>90:
   ytop=90
if ytop<-90:
   ytop=-90
if ybottom<-90:
   ybottom=-90
if ybottom>90:
   ybottom=90

print("calculating ...")
context = staticmaps.Context()
#context.set_tile_provider(staticmaps.tile_provider_StamenToner)
#context.set_tile_provider(staticmaps.tile_provider_ArcGISWorldImagery)
context.set_tile_provider(staticmaps.tile_provider_OSM)

polygon = [
    (ytop,xright),
    (ytop,xleft),
    (ybottom,xleft),  
    (ybottom,xright),
    (ytop,xright),
]
print(yourLat,yourLon)
print(ytop,xleft)
print(ybottom,xright)

zoom = 2  # radius in km 
context.add_object(staticmaps.Area([staticmaps.create_latlng(lat, lng) for lat, lng in polygon],
        fill_color=staticmaps.TRANSPARENT,width=2,color=staticmaps.parse_color("#00FF003F")))

#context.add_object(staticmaps.Circle(center1, zoom, fill_color=staticmaps.TRANSPARENT, color=staticmaps.RED, width=2))
#context.add_object(staticmaps.Marker(center1, color=staticmaps.RED, size=6))

# render non-anti-aliased png
image = context.render_pillow(640, 480)
image.save("map.png")
print("saved the map as map.png")
