import serial
import time
import socket
import json
from pprint import pprint
 
UDP_IP = "127.0.0.1"
UDP_PORT = 5005   
sock = socket.socket(socket.AF_INET, # Internet
                    socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))

import Adafruit_Nokia_LCD as LCD
import Adafruit_GPIO.SPI as SPI

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont


# Raspberry Pi hardware SPI config:
DC = 23
RST = 24
SPI_PORT = 0
SPI_DEVICE = 0

# Raspberry Pi software SPI config:
# SCLK = 4
# DIN = 17
# DC = 23
# RST = 24
# CS = 8

# Beaglebone Black hardware SPI config:
# DC = 'P9_15'
# RST = 'P9_12'
# SPI_PORT = 1
# SPI_DEVICE = 0

# Beaglebone Black software SPI config:
# DC = 'P9_15'
# RST = 'P9_12'
# SCLK = 'P8_7'
# DIN = 'P8_9'
# CS = 'P8_11'


# Hardware SPI usage:
disp = LCD.PCD8544(DC, RST, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=4000000))

# Software SPI usage (defaults to bit-bang SPI interface):
#disp = LCD.PCD8544(DC, RST, SCLK, DIN, CS)

# Initialize library.
disp.begin(contrast=60)

# Clear display.
disp.clear()
disp.display()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
image = Image.new('1', (LCD.LCDWIDTH, LCD.LCDHEIGHT))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a white filled box to clear the image.
draw.rectangle((0,0,LCD.LCDWIDTH,LCD.LCDHEIGHT), outline=255, fill=255)

# Draw some shapes.
draw.ellipse((2,2,20,20), outline=0, fill=255)
#draw.ellipse((8,2,15,1), outline=0, fill=0)
draw.rectangle((8,9,27,13), outline=0, fill=0)
# draw.polygon([(46,22), (56,2), (66,22)], outline=0, fill=255)
# draw.line((68,22,81,2), fill=0)
# draw.line((68,2,81,22), fill=0)

# Load default font.
font = ImageFont.load_default()

# Alternatively load a TTF font.
# Some nice fonts to try: http://www.dafont.com/bitmap.php
# font = ImageFont.truetype('Minecraftia.ttf', 12)
 # font = ImageFont.truetype('Minecraftia.ttf', 12)
draw.text((30,0), 'Smart', font=font)
draw.text((30,10), 'Handlers', font=font)
# Display image.
disp.image(image)
disp.display()

print('Press Ctrl-C to quit.')

#ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)

while True:
    # if draw is not None:
    #      del draw

    #time.sleep(1.0)

    # Create blank image for drawing.
    # Make sure to create image with mode '1' for 1-bit color.
    # Initialize library.

    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    #draw = ImageDraw.Draw(image)
    #font = ImageFont.load_default()
    #todos = json.load(open('../node-todo/todo-list.json'))

    print(data, "something has received")
    #print "Received Message:", data
    #draw.text((8,30), ser.readline(), font=font)
    #draw.text((8,30), data['table'][0]["description"], font=font)
    # draw.rectangle((LCD.LCDWIDTH,20,20,30), outline=0, fill=255)
    draw.rectangle((0,21,LCD.LCDWIDTH-1,43), outline=0, fill=255)
    draw.multiline_text((2,21), data, font=font)
    disp.image(image)
    disp.display()
    
