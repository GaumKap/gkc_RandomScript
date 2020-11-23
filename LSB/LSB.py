#!/usr/bin/env python3
# la ligne ci dessus est pour l'exectution sous Ubuntu 20.04 avec Python 3.8
# Si incorècte changer la ligne ou executez la commande avec "python3 LSB.py"
#
# Script Décodage LSB Python #
# GaumKap 2020
# Licence GPL-3.0
# version 0.0.1.0
#
# Utilisez virtualenv pour ce script ou installez les dépendances:
#   Pillow
########################
import sys
from PIL import Image
import os

if (len(sys.argv) < 3):
    print("something is missing : \n\t python LSB.py <in.png> <out.png>")
    exit(1)
########################
#Imaginez que ces variables sont des #dfine parce-que C++ est mieu mais complexe
define_fichier = sys.argv[1]
define_output = sys.argv[2]
########################


if not (os.path.isfile(define_fichier)):
    print("Error entry file don't exist")
    exit(1)
##################################################################
def rgb2hex(r, g, b):
    """
    Cette fonction converti les vlaeurs RGB d'un pixel en sa valeur Héxadécimal.
    exemple : 255 255 255 ---> #ffffff
    """
    return '#{:02x}{:02x}{:02x}'.format(r, g, b)
##################################################################

##################################################################
def decimalToBinary(num):
    """Cette fonction permet de convertir une valeur décimal en valeur binaire dans un string"""
    bin_sr = str(bin(num)[2:])

    i = len(bin_sr)
    result = ""
    if i >= 8 :
        result = bin_sr
    else:
        while i < 8:
            result = "0"+result
            i += 1
        result += bin_sr
    return result
##################################################################

##################################################################
def rgb_lsb(num):
    """
    rgb_lsb(string num)
    Cette fonction inverse les 4 bit de poid faible et les 4 bits de poid fort pour une seul couleur RGB
    Exemple : 1010 1100 --> 1100 1010
    La fonction prend en entrée un string contenant la valeur binaire de la couleur
    puis retourne un int qui corréspond a la valeur pour la couleur indiquée en entré
    """

    lsb = num[4:] # 4 dernieres char de la chaine
    hsb = num[:4] # 4 premieres char de la chaine

    # Recalcule de la valeur décimal du pixel
    result = (int(lsb[0])*128) + (int(lsb[1])*64) + (int(lsb[2])*32) + (int(lsb[3])*16) + (int(hsb[0])*8) + int(hsb[1])*4 + int(hsb[2])*2 + int(hsb[3])*1

    return result
##################################################################


im_source = Image.open(define_fichier) # ouverture de la source
width, height = im_source.size #Récuperation de la taille du tableau (image)
print("Image DATA : width=",width,", height=",height)

i=0 # lines
j=0 # colums
im_dest = im_source # Duplication de l'image au cas ou
while i < height:
    while j < width:

        r, g, b = im_source.getpixel((j, i)) # get color from current pixel
        bin_r = decimalToBinary(r) # string Rouge
        bin_g = decimalToBinary(g) # string Vert
        bin_b = decimalToBinary(b) # string Bleu

        r = rgb_lsb(bin_r) # New red
        g = rgb_lsb(bin_g) # New green
        b = rgb_lsb(bin_b) # New blue
        im_dest.putpixel((j,i),(int(r),int(g),int(b))) # New pixel
        j += 1

    os.system('cls')
    print(i,"/",height)
    i += 1
    j = 0 # go to beginig of line

im_dest.save(define_output) # save new picture to destination file