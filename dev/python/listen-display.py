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

draw.text((30,0), 'Smart', font=font)
draw.text((30,10), 'Handlers', font=font)
# Display image.
disp.image(image)
disp.display()

print('Press Ctrl-C to quit.')

ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)

prevVal = 0
prevIndex = 0
startTime = 0
endTime = 0
deletable = False
while True:
    while True:
        incoming = ser.readline() 
        if len(incoming) != 0:
            if incoming[0] == "b":
                if not deletable:
                    prevVal = 0
                    prevIndex = 0
                    d = json.load(open(path))
                    
                    draw.rectangle((0,24,LCD.LCDWIDTH-1,46), outline=0, fill=255)
                    h=24
                    i = 0
                    for item in d["table"]:
                        if i is 1:
                            break;
                        # print(draw.textsize(item["description"]))
                        draw.text((2,h), item["description"], font=font)
                        h = h + 10
                        i=i+1
                        draw.text((2,h), str(len(d["table"])) + " todo(s)", font=font)
                    # draw.multiline_text((2,21), d["table"][1]["description"], font=font)
                    disp.image(image)
                    disp.display()
                    startTime = time.time()
                    
                    deletable = True
                
                else:
                    with open(path, 'w') as outfile:
                        data = {}
                        data['table'] = [] 
                        json.dump(data , outfile)

                    prevVal = 0
                    prevIndex = 0
                    draw.rectangle((0,24,LCD.LCDWIDTH-1,46), outline=0, fill=255)
                    disp.image(image)
                    disp.display()
                break
            
            elif incoming[0] == 'c':   
                startTime = time.time()  
                prevVal = 0
                prevIndex = 0
                d = json.load(open(path))
                
                draw.rectangle((0,24,LCD.LCDWIDTH-1,46), outline=0, fill=255)
                h=24
                i = 0
                for item in d["table"]:
                    if i is 1:
                        break;
                    # print(draw.textsize(item["description"]))
                    draw.text((2,h), item["description"], font=font)
                    h = h + 10
                    i=i+1
                    draw.text((2,h), str(len(d["table"])) + " todo(s)", font=font)
                # draw.multiline_text((2,21), d["table"][1]["description"], font=font)
                deletable = True

                disp.image(image)
                disp.display()
                break
            else:
                startTime = time.time()
                d = json.load(open(path))
                if len(d["table"]) == 0:
                    break
                
                h=24
                encoderVal = int(incoming[:-2])
                if encoderVal == 16383 and prevVal == 0:
                    prevVal = 16384
                 
                # print("current: " + str(encoderVal))
                # print("prev: " + str(prevVal))

                if encoderVal > prevVal:
                    prevIndex = prevIndex + 1
                    prevVal = encoderVal
                    # print("prevIndex: " + str(prevIndex))
                    if prevIndex > len(d["table"]):
                        prevIndex = len(d["table"]) - 1
                    
                    # print("prevIndex: " + str(prevIndex))
                    if len(d["table"]) > prevIndex:
                        draw.rectangle((0,24,LCD.LCDWIDTH-1,46), outline=0, fill=255)
                        draw.text((2,h), d["table"][prevIndex]["description"], font=font)
                        h = h + 10
                        # draw.text((2,h), str(len(d["table"]) - 1 - prevIndex) + " items left", font=font)
                        draw.text((2,h), str(len(d["table"])) + " todo(s)", font=font)

                        deletable = True

                        disp.image(image)
                        disp.display()                   

                elif encoderVal < prevVal:
                    prevIndex = prevIndex - 1
                    prevVal = encoderVal
                    if prevIndex < 0:
                        prevIndex = 0
                    # print("prevIndex: " + str(prevIndex))
                    if len(d["table"]) >= prevIndex:
                        draw.rectangle((0,24,LCD.LCDWIDTH-1,46), outline=0, fill=255)
                        draw.text((2,h), d["table"][prevIndex]["description"], font=font)
                        h = h + 10
                        # draw.text((2,h), str(len(d["table"]) - 1 - prevIndex) + " items left", font=font)
                        draw.text((2,h), str(len(d["table"])) + " todo(s)", font=font)

                        deletable = True

                        disp.image(image)
                        disp.display()

                break

        endTime = time.time()

        if endTime - startTime > 5.0:
            deletable = False
            draw.rectangle((0,24,LCD.LCDWIDTH-1,46), outline=0, fill=255)
            disp.image(image)
            disp.display()      

