import serial
import time
import socket
import json
import os.path

my_path = os.path.abspath(os.path.dirname(__file__))
path = os.path.join(my_path, "../node-todo/todo-list.json") 

# UDP_IP = "127.0.0.1"
# UDP_PORT = 5005   
# sock = socket.socket(socket.AF_INET, # Internet
#                   socket.SOCK_DGRAM) # UDP
# sock.bind((UDP_IP, UDP_PORT))

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
draw.rectangle((8,9,25,13), outline=0, fill=255)
draw.rectangle((8,14,25,14), outline=0, fill=255)
draw.rectangle((0,24,LCD.LCDWIDTH-1,46), outline=0, fill=255)
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

ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)

while True:
    #time.sleep(1.0)
    # draw.rectangle((8,9,13,27), outline=0, fill=0) 
    # sock.settimeout(1.0)
    # try:
        # data, addr = sock.recvfrom(1024)# buffer size is 1024 bytes
    # except sock.timeout:    
        # draw.ellipse((2,2,20,20), outline=0, fill=255)
        # draw.rectangle((8,9,27,13), outline=0, fill=255)
    if ser.readline() != "":
        d = json.load(open(path))

        draw.rectangle((0,24,LCD.LCDWIDTH-1,46), outline=0, fill=255)
        h=24
        i = 0
        for item in d["table"]:
            if i is 2:
                break;
            print(draw.textsize(item["description"]))
            draw.multiline_text((2,h), item["description"], font=font)
            h = h + 10
            i=i+1
        # draw.multiline_text((2,21), d["table"][1]["description"], font=font)
        disp.image(image)
        disp.display()
   
