import sys
import time

from mpd import (MPDClient, CommandError)
from socket import error as SocketError

import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import subprocess

# Raspberry Pi pin configuration:
RST = None
# Note the following are only used with SPI:
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0

# 128x32 display with hardware I2C:
disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST)

# Initialize library.
disp.begin()

# Clear display.
disp.clear()
disp.display()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new('1', (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0,0,width,height), outline=0, fill=0)

# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height-padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0
indent = 0
# Load default font.
#font = ImageFont.load_default()
font = ImageFont.truetype("DejaVuSans", 11)
#definitions
client = MPDClient()
client.connect('localhost', 6600)

PREFIX_SONG=' - '

while True:

    # Draw a black filled box to clear the image.
    draw.rectangle((0,0,width,height), outline=0, fill=0)

    #Read song title
    song_info = client.currentsong()
    #example songtitle
    #{'file': 'https://rockfm-cope-rrcast.flumotion.com/cope/rockfm.mp3', 'title': 'LONE STAR - MI CALLE', 'pos': '0', 'id': '1'}


    if 'title' in song_info:
        songtitle = song_info["title"]
        art_endpos = songtitle.find(PREFIX_SONG)
        song_pos = art_endpos + 3

        artist = songtitle[:art_endpos]
        song = songtitle[song_pos:]
    elif 'name' in song_info:
        song = song_info["name"]
        artist = " "
    elif 'file' in song_info:
        song = song_info["title"]
        artist = " "
    else:
        song = "Unknown radio"
        artist = " "

    width_artist = font.getsize(artist)[0]
#    print (width_artist)
    width_song = font.getsize(song)[0]
#    print (width_song)

#    if(width_song > 128):
#        diff_song = width_song - 128
#        indent = indent - 1
#        x = x + indent

    # Write two lines of text.

    draw.text((x, top), str(song),  font=font, fill=255)
    draw.text((x, top+16),str(artist), font=font, fill=255)

    # Display image.
    disp.image(image)
    disp.display()
    time.sleep(1)
