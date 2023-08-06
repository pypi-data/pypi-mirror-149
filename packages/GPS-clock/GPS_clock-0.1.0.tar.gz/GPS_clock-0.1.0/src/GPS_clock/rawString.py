# * This program displays the raw data packets from an Adafruit GPS breaout board connected to RPi serial port 0 
# No satellite fix the LED blinks evey 2 seconds.
# After sat fix the LED blinks every 10 seconds.
# Test serial stream. Should list NMEA strings until stopped with CTRL-C 

import os
os.system('stty -F /dev/serial0 raw 9600 cs8 clocal -cstopb')
# sets serial port 0 to 9600 bauds, with 8 bits, no modem control, and 1 stop bit
os.system('cat /dev/serial0')
# displays the NMEA strings as raw data


