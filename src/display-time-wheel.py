#!/usr/bin/python3
#
# https://www.tweaking4all.com/hardware/arduino/adruino-led-strip-effects/
#

import board
import neopixel
import sys
import time
import datetime
import random

VERSION = "0.1.5"

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

pix = neopixel.NeoPixel(board.D18, N, auto_write=False)

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

def time_wheel(pix):
    prv_msg = ""
    colour = [255,0,0]

    cycle_s = 5*60

    debug_count = 0
    debug_disp = 60

    end_wheel_pos = 85
    while True:

        start_time = datetime.datetime.now()
        tot_sec = int(start_time.strftime("%s"))

        if debug_count==0:
            print(tot_sec)
        debug_count+=1
        debug_count%=debug_disp


        pos = int(255.0 * float(int(tot_sec) % (cycle_s)) / float(cycle_s))
        colour = wheel(pos)

        s = start_time.strftime("%S")
        mi = start_time.strftime("%M")
        hr = start_time.strftime("%H")


        hr = str(int(start_time.strftime("%I"))%12)
        hr_i = int(hr)%12
        if hr_i >= 10:
            hr = chr(hr_i - 10 + ord('A'))

        msg = hr + mi + s

        if prv_msg != msg:
            clear_segment(pix, False)
            show_message(pix, msg, colour, False)
            pix.show()
            prv_msg = msg

        time.sleep(1.0/60.0)

def countdown_wheel(pix, target_time):
    prv_msg = ""
    colour = [255,0,0]
    start_time = datetime.datetime.now()
    tot_sec = (target_time - start_time).total_seconds()

    end_wheel_pos = 85
    while True:

        del_sec = (target_time - datetime.datetime.now()).total_seconds()

        if del_sec <= (60*10):
            colour = [255,0,0]
        else:
            pos = int(255.0 * float(del_sec) / float(tot_sec))
            pos = (pos+end_wheel_pos) % 255
            colour = wheel(pos)

            



        if del_sec < 0:
            if del_sec < -5: break

            oddeven = int(4*del_sec)%2

            clear_segment(pix, False)
            if oddeven==1:
                show_message(pix, '00000', colour, False)
            pix.show()

        elif del_sec < 10:
            msg = ""
            for i in range(NDIGIT):
                msg += str(int(del_sec))

            del_ms = del_sec % 1
            fade_col = [ int(colour[0]*del_ms), int(colour[1]*del_ms), int(colour[2]*del_ms) ]
            show_message(pix, msg, fade_col, False)
            pix.show()

        # more than 10mins, show full hour min sec
        #
        elif del_sec > (10*60):

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


        # else shift to m ss uu
        #
        else:
            ms = int(del_sec*100) % 60
            s = int(del_sec) % 60
            mi = int(del_sec/60) % 60

            msg = ""
            msg += str(mi%10)
            if s < 10:
                msg += '0'
            msg += str(s)
            if ms < 10:
                msg += '0'
            msg += str(ms)

            if prv_msg != msg:
                clear_segment(pix, False)
                show_message(pix, msg, colour, False)
                pix.show()
                prv_msg = msg

        #time.sleep(1.0/1024.0)
        time.sleep(1.0/60.0)

def countdown(pix, target_time, colour = [255,0,0]):
    prv_msg = ""
    while True:

        del_sec = (target_time - datetime.datetime.now()).total_seconds()
        if del_sec < 0:
            if del_sec < -5: break

            oddeven = int(4*del_sec)%2

            clear_segment(pix, False)
            if oddeven==1:
                show_message(pix, '00000', colour, False)
            pix.show()

        elif del_sec < 10:
            msg = ""
            for i in range(NDIGIT):
                msg += str(int(del_sec))

            del_ms = del_sec % 1
            fade_col = [ int(colour[0]*del_ms), int(colour[1]*del_ms), int(colour[2]*del_ms) ]
            show_message(pix, msg, fade_col, False)
            pix.show()

        # more than 10mins, show full hour min sec
        #
        elif del_sec > (10*60):

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


        # else shift to m ss uu
        #
        else:
            ms = int(del_sec*100) % 60
            s = int(del_sec) % 60
            mi = int(del_sec/60) % 60

            msg = ""
            msg += str(mi%10)
            if s < 10:
                msg += '0'
            msg += str(s)
            if ms < 10:
                msg += '0'
            msg += str(ms)

            if prv_msg != msg:
                clear_segment(pix, False)
                show_message(pix, msg, colour, False)
                pix.show()
                prv_msg = msg

        #time.sleep(1.0/1024.0)
        time.sleep(1.0/60.0)

def heatcolor(pix, pos, temp):
    t192 = int((temp/255.0)*191)
    heatramp = t192 & 0x3f
    heatramp *= 4

    if (t192 > 0x80):
        pix[pos] = (255,255,heatramp)
    elif (t192 > 0x40):
        pix[pos] = (255,heatramp,0)
    else:
        pix[pos] = (heatramp,0,0)

def wheel(pos):
    c = [0,0,0]
    if (pos < 85):
        c[0] = pos * 3
        c[1] = 255 - pos * 3
        c[2] = 0
    elif pos < 170:
        pos -= 85
        c[0] = 255 - pos*3
        c[1] = 0
        c[2] = pos*3
    else:
        pos -= 170
        c[0] = 0
        c[1] = pos*3
        c[2] = 255 - pos*3
    return c


def fire(cooling, sparking, speeddelay, ds):
    heat = []
    M = PIXPERDIGIT
    for dig in range(NDIGIT):
        heat.append([])
        for i in range(PIXPERDIGIT):
            heat[dig].append(0)

    start = datetime.datetime.now()
    while True:
        for dig in range(NDIGIT):
            for i in range(M):
                cooldown = int(random.random()*float(cooling)*10.0/float(N) + 2.0)
                if cooldown > heat[dig][i]:
                    heat[dig][i] = 0
                else:
                    heat[dig][i] = heat[dig][i] - cooldown

            for k in range(M-1, 2, -1):
                heat[dig][k] = (heat[dig][k-1] + heat[dig][k-2] + heat[dig][k-2])/3

            if ( int(random.random()*255.0) < sparking ):
                y = int(random.random()*7.0)
                heat[dig][y] = heat[dig][y] = int(random.random()*(255-160)) + 160

            for j in range(M):
                heatcolor(pix,j + M*dig,heat[dig][j])

        pix.show()
        time.sleep(1.0/30.0)

        cur = datetime.datetime.now()
        ts = (cur - start).total_seconds()
        if ts > ds: break


def rainbow(pix, ds):
    start = datetime.datetime.now()
    p = 0
    while True:
        p += 1
        for i in range(N):
            c = wheel((i+p)%255)
            pix[i] = (c[0], c[1], c[2])
        pix.show()
        time.sleep(1.0/30.0)

        cur = datetime.datetime.now()
        ts = (cur - start).total_seconds()
        if ts > ds: break

def fadetoblack(pix, pos, val):
    c = pix[pos]

    r = c[0]
    g = c[1]
    b = c[2]

    if (r<10): r = 0
    else: r = int(float(r) - (float(r)*float(val)/256.0))

    if (g<10): g = 0
    else: g = int(float(g) - (float(g)*float(val)/256.0))

    if (b<10): b = 0
    else: b = int(float(b) - (float(b)*float(val)/256.0))

    if r<0: r = 0
    if g<0: g = 0
    if b<0: b = 0

    pix[pos] = (r,g,b)


def meteorrain(r,g,b,sz,traildecay,ds):
    M = PIXPERDIGIT
    start = datetime.datetime.now()
    clear_segment(pix, False)
    while True:

        for i in range(2*M):

            for dig in range(NDIGIT):

                for j in range(M):
                    fadetoblack(pix, j + M*dig, traildecay)
                    #if random.random() > 0.5:
                    #    fadetoblack(pix, j + M*dig, traildecay)
                for j in range(sz):
                    if ((i-j)<M) and ((i-j)>=0):
                        pix[(i-j) + M*dig] = (r,g,b)

            pix.show()
            time.sleep(1.0/30.0)

            cur = datetime.datetime.now()
            ts = (cur - start).total_seconds()
            if ts > ds: break


        cur = datetime.datetime.now()
        ts = (cur - start).total_seconds()
        if ts > ds: break

def randseg(pix, ds, dt=0.1):
    _seg = "abcdefghijklmn"
    start = datetime.datetime.now()
    while True:
        clear_segment(pix)

        for dig in range(NDIGIT):

            n = int(random.random()*14.0) + 0
            for _x in range(n):
                idx = int(random.random()*len(_seg))
                randcol = [ int(random.random()*255.0), int(random.random()*255.0), int(random.random()*255.0)]
                s = _seg[idx]
                show_segment(pix, s, randcol, dig, False)
        pix.show()
        _dt = random.random() * 0.15
        time.sleep(dt + _dt)

        cur = datetime.datetime.now()
        ts = (cur - start).total_seconds()
        if ts > ds: break

time_wheel(pix)
#countdown_wheel(pix, target_time)

msg_delay = 1

clear_segment(pix, False)
show_message(pix, "HAPPY", [255,255,255], False)
pix.show()
time.sleep(msg_delay)

clear_segment(pix, False)
show_message(pix, "NEW  ", [255,255,255], False)
pix.show()
time.sleep(msg_delay)

clear_segment(pix, False)
show_message(pix, " YEAR", [255,255,255], False)
pix.show()
time.sleep(msg_delay)


while True:

    mode = int(random.random()*4.0)

    if mode==0:
        rainbow(pix, 60)
    elif mode == 1:
        fire(20, 100, 50, 60)
    elif mode == 2:
        r = int(random.random()*255.0)
        g = int(random.random()*255.0)
        b = int(random.random()*255.0)
        meteorrain(r,g,b, 10, 16,30)
    elif mode == 3:
        randseg(pix, 60)



