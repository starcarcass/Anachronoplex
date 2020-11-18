#!/usr/bin/python3

import board
import neopixel
import sys
import time
import datetime
import random

NDIGIT= 5
PIXPERDIGIT=92
N = NDIGIT*PIXPERDIGIT

epoch = datetime.datetime(1970, 1, 1)

dsec = 30
tnow = datetime.datetime.now()
target_time = datetime.datetime.now() + datetime.timedelta(0,30)

print("## YYYY-MM-DD HH:MM:SS TZ")

if len(sys.argv) > 1:
    target_time = datetime.datetime.strptime(sys.argv[1], '%Y-%m-%d %H:%M:%S %Z')

    #dt = dateparser.parse(sys.argv[1])
    #_sec = (dt - datetime.datetime(1970,1,1)).total_seconds()
    #dsec = time.time() - _sec

print(target_time)

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

def clear_digit(pix, dig=0, flush=False):
    for idx in range(PIXPERDIGIT):
        pix[ idx + PIXPERDIGIT*dig ] = ( 0, 0, 0 )

def show_segment(pix, segname, col, dig=0, flush=False):
    seg = digit_segment[segname]

    fudge = -1
    if seg[2] < 0: fudge = 1
    for _p in range(seg[0], seg[1]-fudge, seg[2]):
        p = _p + dig*PIXPERDIGIT
        pix[p] = (col[0], col[1], col[2])
    if flush:
        pix.show()

def show_char(pix, ch, col, dig=0, flush=False):
    if not ( ch in char_seg_map ):
        return
    segnames = char_seg_map[ch]
    #clear_segment(pix)
    clear_digit(pix, dig, flush)
    for sidx in range(len(segnames)):
        s = segnames[sidx]
        show_segment(pix, s, col, dig)
    if flush:
        pix.show()


def randseg(pix, ndig=1, dt=0.1, reps=10):
    _seg = "abcdefghijklmn"
    for rep in range(reps):
        clear_segment(pix)

        for dig in range(ndig):

            n = int(random.random()*14.0) + 0
            for _x in range(n):
                idx = int(random.random()*len(_seg))

                randcol = [ int(random.random()*255.0), int(random.random()*255.0), int (random.random()*255.0)]
                s = _seg[idx]
                show_segment(pix, s, randcol, dig, False)

        pix.show()

        _dt = random.random() * 0.15
        time.sleep(dt + _dt)

pix = neopixel.NeoPixel(board.D18, N, auto_write=False)

randseg(pix, NDIGIT, 0.05, 10000)

sys.exit(0)

#dig = "0123456789"
#dig = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
#dig = " BUTTS"
msg = "BUTTS"

def show_message(pix, msg, col, flush=False):
    curdig=NDIGIT-1
    for msg_idx in range(len(msg)):

        show_char(pix, msg[msg_idx], col, curdig)
        curdig -= 1
        if curdig < 0: break

    if flush: pix.show()


def show_message_fade(pix, msg, col, flush=False):

    tfac = 1.0/2.0
    t = time.time()*tfac
    itime_prv = int(t)
    itime = itime_prv
    ftime = t % 1

    percent = .7
    while itime_prv == itime:
        if ftime <percent:
            c = 255
        else : 
            c = 255 - int(255.0*(ftime-percent)/(1-percent))

        curdig = NDIGIT-1
        for msg_idx in range(len(msg)):

            show_char(pix, msg[msg_idx], [c,0,0], curdig)
            curdig -= 1
            if curdig < 0: break

        if flush: pix.show()

        t = time.time()*tfac
        itime = int(t)
        ftime = t%1

    clear_segment (pix,True)

def countdown1(target_time):
    prv_msg = ""

    start_sec = (target_time - datetime.datetime.now()).total_seconds()
    while True:

        del_sec = (target_time - datetime.datetime.now()).total_seconds()
        if del_sec < 0: break

        s = int(del_sec) % 60
        mi = int(del_sec/60) % 60
        hr = int(del_sec/(60*60)) % 60

        msg = ""
        msg += str(hr%10)
        if mi < 10:
            msg += '0'
        msg += str(mi)
        if s < 10:
            msg += '0'
        msg += str(s)

        #c = int(255.0 * del_sec / start_sec )
        c = int(128.0 * (del_sec - 1)/ start_sec )
        if c < 0 : c = 0
        print(c)

        if prv_msg != msg:
            clear_segment(pix, False)
            show_message(pix, msg, [255,0,c], False)
            pix.show()
            prv_msg = msg

        time.sleep(1.0/1024.0)

def countdown(target_time, colour = [255,0,0]):
    prv_msg = ""
    while True:

        del_sec = (target_time - datetime.datetime.now()).total_seconds()
        if del_sec < 0: break

        s = int(del_sec) % 60
        mi = int(del_sec/60) % 60
        hr = int(del_sec/(60*60)) % 60

        msg = ""
        msg += str(hr%10)
        if mi < 10:
            msg += '0'
        msg += str(mi)
        if s < 10:
            msg += '0'
        msg += str(s)

        if prv_msg != msg:
            clear_segment(pix, False)
            #show_message(pix, msg, [255,0,0], False)
            show_message(pix, msg, colour, False)
            pix.show()
            prv_msg = msg

        time.sleep(1.0/1024.0)

countdown(target_time)

