#!/usr/bin/python3

import board
import neopixel
import sys
import time
import random

N = 92

char_seg_map = {
  "0" : "abfimn", "1" : "efm", "2" : "afghin",
  "3" : "afghmn", "4" : "bfghm", "5" : "abghmn",
  "6" : "abghimn", "7" : "afm", "8" : "abfghimn",
  "9" : "abfghmn",

  "a" : "", "b" : "", "c" : "",
  "d" : "",
  "e" : ""
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

def randseg(pix, col, dt=0.1, reps=10):
    _seg = "abcdefghijklmn"
    for rep in range(reps):
        clear_segment(pix)

        n = int(random.random()*4.0) + 0
        for _x in range(n):
            idx = int(random.random()*len(_seg))

            randcol = [ int(random.random()*255.0),int(random.random()*255.0),int(random.random()*255.0)]
            s = _seg[idx]
            show_segment(pix, s, randcol, True)
        time.sleep(dt)



def spinner(pix, col):
    seq = "gcdehlkjbafmni"
    for seqidx in range(len(seq)):
        seg = seq[seqidx]
        clear_segment(pix)
        show_segment(pix, seg, col, True)
        time.sleep(0.01)

#randseg(pix, [255,0,0], 0.05, 10000)

pix = neopixel.NeoPixel(board.D18, N, auto_write=False)

led_list = []

if len(sys.argv) > 1:
    ledstr = sys.argv[1]
    sa = ledstr.split(",")
    for x in sa:
        print( x)
        led_list.append( int(x) )

color = [255, 255, 255]
if len(sys.argv) > 2:
    sa = sys.argv[2].split(",")
    if len(sa) > 0:
        color[0] = int(sa[0])
    if len(sa) > 1:
        color[1] = int(sa[1])
    if len(sa) > 2:
        color[2] = int(sa[2])

clear_segment(pix)
for pos in led_list:
    print(pos)
    pix[pos] = ( color[0], color[1], color[2] )

pix.show()



