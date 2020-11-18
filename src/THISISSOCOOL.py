#!/usr/bin/python3

import board
import neopixel
import sys
import time

N = 92

char_seg_map = {
  "0" : "abfimn", "1" : "efm", "2" : "afghin",
  "3" : "afghmn", "4" : "bfghm", "5" : "abghmn",
  "6" : "abghimn", "7" : "afm", "8" : "abfghimn",
  "9" : "abfghmn",

  "a" : "afghimn", "b" : "bghimn", "c" : "ghin",
  "d" : "fghimn", "e" : "abfghin", "f" : "eghk",
  "g" : "acfhmn", "h" : "bghim", "i" : "k",
  "j" : "fmn", "k" : "dekl", "l" : "dkn",
  "m" : "ghikm", "n" : "gil", "o" : "ghimn",
  "p" : "abegi", "q" : "acfhm", "r" : "ghi",
  "s" : "hln", "t" : "bgin", "u" : "imn",
  "v" : "ij", "w" : "ijlm", "x" : "ceghjl",
  "y" : "dfhmn", "z" : "gjn",
  
  "A" : "abfghim", "B" : "adfkmnh", "C" : "abin",
  "D" : "adfkmn", "E" : "abghin", "F" : "abghi",
  "G" : "abimnh", "H" : "bfghim", "I" : "adkn",
  "J" : "fimn", "K" : "begil", "L" : "bin",
  "M" : "bcefim", "N" : "bcfilm", "O" : "abfimn",
  "P" : "abfghi", "Q" : "abfilmn", "R" : "abfghil",
  "S" : "abghmn", "T" : "adk", "U" : "bfimn",
  "V" : "beij", "W" : "bfijlm", "X" : "cejl",
  "Y" : "cek", "Z" : "aejn",
  
  "\\" : "cl", "/" : "ej", "'" : "e", '"' : "df"
}

digit_segment = {

  # top
  "a" : [8, 0, -1],

  # left up
  "b" : [9, 16, 1],

  # diag up left
  "c" : [21, 17, -1],

  # middle vert
  "d" : [22, 28, 1],

  # up right diag
  "e" : [33, 29, -1],

  # up right vert
  "f" : [34, 41, 1],

  # middle horiz, left
  "g" : [49, 46, -1],

  # middle horiz. right
  "h" : [45, 42, -1],

  # lower vert left
  "i" : [50, 57, 1],

  # lower diag left
  "j" : [58, 62, 1],

  # lower vert
  "k" : [63, 69, 1],

  # lower diag right
  "l" : [70, 74, 1],

  # lower right vert
  "m" : [75, 82, 1],

  # bottom segment (horiz)
  "n" : [83, 91, 1]
}

def clear_segment(pix, flush=False):
    for i in range(N):
        pix[i] = (0, 0, 0)
    if flush:
        pix.show()

def show_segment(pix, segname, col, flush=False):
    seg = digit_segment[segname]

    fudge = -1
    if seg[2] < 0: fudge = 1
    for p in range(seg[0], seg[1]-fudge, seg[2]):
        pix[p] = (col[0], col[1], col[2])
    if flush:
        pix.show()

def show_char(pix, ch, col, flush=False):
    if not ( ch in char_seg_map ):
        return
    segnames = char_seg_map[ch]
    clear_segment(pix)
    for sidx in range(len(segnames)):
        s = segnames[sidx]
        show_segment(pix, s, col)
    if flush:
        pix.show()

pix = neopixel.NeoPixel(board.D18, N, auto_write=False)

#dig = "0123456789"
#dig = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
dig = " THISISSOCOOL"

#dp = 1
for digidx in range(len(dig)):
    #print(dp)

    t = time.time()*2.0
    itime_prv = int(t)
    itime = itime_prv
    ftime = t % 1

    d = dig[digidx]
    percent = .7
    while itime_prv == itime:
        if ftime <percent:
            c = 255
        else : 
            c = 255 - int(255.0*(ftime-percent)/(1-percent))
        #c = 255 - int(255.0*ftime)
        #c = 255
        show_char(pix, d, [0,0,c], True)

        t = time.time()*2.0
        itime = int(t)
        ftime = t%1
    clear_segment (pix,True)


    #for p in range(0, 255, dp):
    #    show_char(pix, d, [p,0,0], True)
    #for p in range(255, -1, -dp):
    #    show_char(pix, d, [p,0,0], True)
    #clear_segment(pix, True)



def misc():
    segnames = "abcdefghijklmn"
    for sidx in range(len(segnames)):
        s = segnames[sidx]
        print( s)
        clear_segment(pix)
        show_segment(pix, s)
        time.sleep(0.5)



## fill from bottom to top, then from top to bottom (drain)
## caligraphy trace out path
