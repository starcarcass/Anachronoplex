#!/usr/bin/python3

import board
import neopixel
import sys
import time
import random

from PIL import Image
from PIL import GifImagePlugin
import sys

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

#  0   1   2   3   4   5   6   7   8   9  10
gif_map = [
  -1,  8,  7,  6,  5,  4,  3,  2,  1,  0, -1,
   9, -1, -1, -1, -1, -1, -1, -1, -1, -1, 34,
  10, -1, 21, -1, -1, 22, -1, -1, 33, -1, 35,
  11, -1, 20, -1, -1, 23, -1, -1, 32, -1, 36,
  12, -1, -1, 19, -1, 24, -1, 31, -1, -1, 37,
  13, -1, -1, 18, -1, 25, -1, 30, -1, -1, 38,
  14, -1, -1, -1, 17, 26, 29, -1, -1, -1, 39,
  15, -1, -1, -1, -1, 27, -1, -1, -1, -1, 40,
  16, -1, -1, -1, -1, 28, -1, -1, -1, -1, 41,
  -1, 49, 48, 47, 46, -1, 45, 44, 43, 42, -1,
  50, -1, -1, -1, -1, 63, -1, -1, -1, -1, 75,
  51, -1, -1, -1, -1, 64, -1, -1, -1, -1, 76,
  52, -1, -1, -1, 62, 65, 74, -1, -1, -1, 77,
  53, -1, -1, 61, -1, 66, -1, 73, -1, -1, 78,
  54, -1, -1, 60, -1, 67, -1, 72, -1, -1, 79,
  55, -1, 59, -1, -1, 68, -1, -1, 71, -1, 80,
  56, -1, 58, -1, -1, 69, -1, -1, 70, -1, 81,
  57, -1, -1, -1, -1, -1, -1, -1, -1, -1, 82,
  -1, 91, 90, 89, 88, 87, 86, 85, 84, 83, -1,
]


###

def chunk(seq, size, groupByList=True):
    func = tuple
    if groupByList:
        func = list
    return [ func(seq[i:i+size]) for i in range(0, len(seq), size) ]

def getPaletteInRgb(img):
    assert img.mode == 'P', "image should be palette mode"
    pal = img.getpalette()
    colors = chunk(pal, 3, False)
    return colors

def unpack_gif(img):
    unpack = {
            "width" : img.width,
            "height" : img.height,
            "n_frames" : img.n_frames,
            "rgb" : []
            }
    WIDTH = img.width
    HEIGHT = img.height
    NFRAME = img.n_frames
    pal = getPaletteInRgb(img)

    unpack["palette"] = pal

    for frame in range(img.n_frames):
        img.seek(frame)
        dat = img.getdata()

        a = []
        for y in range(HEIGHT):
            s = ""
            for x in range(WIDTH):
                d = dat[y*WIDTH + x]
                vv = str(pal[d][0]) + "," + str(pal[d][1]) + "," + str(pal[d][2])
                s += " " + str(dat[ y*WIDTH + x ]) + ":" + vv
                a.append([pal[d][0], pal[d][1], pal[d][2]])
            #print(s)
        unpack["rgb"].append(a)
    return unpack

###


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

def animate_gif(pix, gif_fn, dt=0.02, rep=1):
    img = Image.open(gif_fn)
    data = unpack_gif(img)

    rgb = data["rgb"]

    for rep in range(rep):
        clear_segment(pix)
        for frame_idx in range(len(rgb)):
            frame = rgb[frame_idx]

            for ii in range(len(frame)):
                if gif_map[ii] < 0: continue

                pix[ gif_map[ii] ] = ( frame[ii][0], frame[ii][1], frame[ii][2] )

            pix.show()


            time.sleep(dt)


pix = neopixel.NeoPixel(board.D18, N, auto_write=False)

animate_gif(pix, "heart.gif", 0.100, 20)



## fill from bottom to top, then from top to bottom (drain)
## caligraphy trace out path
def example_unpack_usage():
    img = Image.open("./draw2.gif")
    #print(img.is_animated)
    #print(img.n_frames)
    #print(img.width, img.height)

    unpack = unpack_gif(img)

    print("...", len(unpack["rgb"]), len(unpack["rgb"][0]))

    for frame in range(len(unpack["rgb"])):
        w = unpack["width"]
        h = unpack["height"]
        rgb = unpack["rgb"]
        for y in range(h):
            s = ""
            for x in range(w):
                s += " " + str(rgb[frame][y*w + x][0]) + ","+ str(rgb[frame][y*w + x][1]) + ","+ str(rgb[frame][y*w + x][2])
            print(s)
        print( "---")



