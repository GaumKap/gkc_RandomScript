#!/usr/bin/env python3
"""
Decode Text in image with LSB method,
note : this version 0.0.1.0 ask position in image this script can be modify to analyse all picture.

GaumKap 2020 GPL-3.0
version 0.0.1.0
Use Python 3.8 minimum

This script use :
    Pillow
    Pillow-PIL
"""
########################
import sys
from PIL import Image
import os
import binascii
import base64

if len(sys.argv) < 2:
    print("something is missing : \n\t python LSB.py <in.png> <out.png>")
    exit(1)
########################
define_fichier = sys.argv[1]
########################

def binToHex(num):
    return hex(int(num, 2))



if not (os.path.isfile(define_fichier)):
    print("Error entry file don't exist")
    exit(1)

#Get position of information to decode
str_begin = input("Enter the first pixel of Array : ")
str_ending = input("Enter the last pixel of Array : ")
str_line = input("Enter the line to read in picture : ")

im_source = Image.open(define_fichier)  # open png file source
width, height = im_source.size  # Get width and height of source image
x = (int(str_ending) - int(str_begin)) # Get lenght of pixel array
im_dest = Image.new('RGB', (x, 1) ) # Créate new empty image
i = int(str_begin) # Poistion in source image
x = 0 # position in new image
while i < (int(str_ending)):
    r, g, b = im_source.getpixel((i, int(str_line)))  # get color from current pixel
    im_dest.putpixel((x, 0), (int(r), int(g), int(b)))  # New pixel
    i += 1
    x += 1

####################

width, height = im_dest.size  # Get width and height of new image
i = 0  # lines
j = 0  # columns
bin_line = [] #tab of binary informations
while i < height:
    while j < width:
        r, g, b = im_dest.getpixel((j, i))  # get color from current pixel

        bin_line.append(bin(r)[-1]) #LSB
        bin_line.append(bin(g)[-1]) #LSB
        bin_line.append(bin(b)[-1]) #LSB

        j += 1
    i += 1
    j = 0  # go to beginning of line

chars = [] # array of ASCII Base64 message
for i in range(int(len(bin_line)/8)):
    byte = bin_line[i*8:(i+1)*8]
    chars.append(chr(int(''.join([str(bit) for bit in byte]), 2)))

str_mess = '' # The true correct message but empty
for c in chars:
    str_mess += c # Add one char to string
print("base64 : "+str_mess) # draw message encoded in Base64

str_mess += "=" * ((4 - len(str_mess) % 4) % 4) # Just modify string to work with base64 decoder in Python 3.9
str_mess = base64.b64decode(str_mess) # DECODE base64
str_mess = str(str_mess) # convert to string
str_mess = str_mess[2:(len(str_mess)-1)] # remove b' ... '
print("decoded : " + str_mess) # draw decoded information