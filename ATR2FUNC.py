#!/usr/bin/python

import os
import math

# globals:
delay_per_sec = 0
registered = False
graphix = False
sound_on = False
reg_name = ''
reg_num = 0
sint = [0 for i in range(0, 256)]
cost = [0 for i in range(0, 256)]

# def textxy(x,y,s)       GRAPHICAL
# def coltextxy(x,y,s,c)  GRAPHICAL

# convert a 4 bit unsigned int to a hex string
def hexnum(num):
    if num == 0:
        return '0'
    elif num == 1:
        return '1'
    elif num == 2:
        return '2'
    elif num == 3:
        return '3'
    elif num == 4:
        return '4'
    elif num == 5:
        return '5'
    elif num == 6:
        return '6'
    elif num == 7:
        return '7'
    elif num == 8:
        return '8'
    elif num == 9:
        return '9'
    elif num == 10:
        return 'A'
    elif num == 11:
        return 'B'
    elif num == 12:
        return 'C'
    elif num == 13:
        return 'D'
    elif num == 14:
        return 'E'
    elif num == 15:
        return 'F'
    else:
        return 'X'

# convert an 8 bit unsigned int to a hex string
def hexb(num):
    return hexnum(num >> 4) + hexnum(num & 15)

# convert a 16 bit unsigned int to a hex string
def hex(num): # num:word
    return hexb(int(num) >> 8) + hexb(int(num) & 255)

# casts a string to int, returns 0 if unsuccessful
def valuer(i): # i:string
    try:
        return int(i)
    except:
        return 0

# typecast used in old code from int to longint
def value(i):
    return i

# typecast a value (originally just a real) to a string
def cstrr(i):
    return str(i)

# identical to cstrr in Python
def cstr(i):
    return str(i)

# pad an int n to be l characters long, returns a string
def zero_pad(n,l):
    s = cstr(n)
    while len(s) < l:
        s = '0' + s
    return s

# identical to zero_pad in Python
def zero_pads(s,l):
    return zero_pad(s,l)

# add spaces to the left of string b to make it length l
def addfront(b,l):
    while len(b) < l:
        b = ' ' + b
    return b

# add spaces to the right of string b to make it length l
def addrear(b,l):
    while len(b) < l:
        b = b + ' '
    return b

# make string s uppercase
def ucase(s):
    return s.upper()

# make string s lowercase
def lcase(s):
    return s.lower()

# return a string of spaces of length i
def space(i):
    s = ''
    if i > 0:
        for k in range(0,i):
            s = s + ' '
    return s

# return a string of character c of length i
def repchar(c,i):
    s = ''
    if i > 0:
        for k in range(0,i):
            s = s + c
    return s

# trim off the left whitespace
def ltrim(s1):
    return s1.lstrip()

# trim off the right whitespace
def rtrim(s1):
    return s1.rstrip()

# trim off whitespace from both sides
def btrim(s1):
    return ltrim(rtrim(s1))

# return a string of the l leftmost characters
def lstr(s1,l):
    if len(s1) <= 1:
        return s1
    else:
        return s1[0:l]

# return a string of the l rightmost characters
def rstr(s1,l):
    if len(s1) <= l:
        return s1
    else:
        return s1[-l:]

# def FlushKey: # not needed in Python
# def calibrate_timing() GRAPHICAL
# def time_delay(n) GRAPHICAL

# THE ORIGINAL EDITS A GLOBAL VARIABLE THAT'S NEVER DECLARED IN THE FILE, THIS RETURNS A BOOLEAN
# checks validity of the ATR2.REG file
def check_registration():
    registered = False
    if os.path.isfile('ATR2.REG'):
        f = open('ATR2.REG','r')
        reg_name = f.readline()
        reg_num = f.readline()
        f.close()
        w = 0
        s = btrim(reg_name.upper())
        for i in s:
            print(i)
            w = w + ord(i)
        w = w ^ 0x5AA5
        if w == reg_num:
            registered = True
    return registered

# rolls the bits in n left k times
def rol(n,k):
    s = _bin(n)
    k = k % len(s)
    return s[k:] + s[:k]

# rolls the bits in n right k times
def ror(n,k):
    s = _bin(n)
    if k > len(s):
        return len(s) * '0'
    return s[len(s)-k:] + s[:len(s)-k]

# shifs the bits in n left k times
def sal(n,k):
    s = _bin(n)
    if k > len(s):
        return len(s) * '0'
    return s[k:] + k * '0'

# shifts the bits in n right k times
def sar(n,k):
    s = _bin(n)
    if k > len(s):
        return len(s) * '0'
    return k * '0' + s[:-k]

# GRAPHICAL FUNCTIONS
def viewport(x1,y1,x2,y2):
    pass
def main_viewport():
    viewport(5,5,474,474)

# calculates sine and cosine tables
def make_tables():
    for i in range(0,256):
        sint[i] = math.sin(i/128*math.pi)
        cost[i] = math.cos(i/128*math.pi)

# a lookup for determining color values
def robot_color(n): # n:integer
    k = 7
    m = n % 14
    if m == 0:
        k = 10
    elif m == 1:
        k = 12
    elif m == 2:
        k = 9
    elif m == 3:
        k = 11
    elif m == 4:
        k = 13
    elif m == 5:
        k = 14
    elif m == 6:
        k = 7
    elif m == 7:
        k = 6
    elif m == 8:
        k = 2
    elif m == 9:
        k = 4
    elif m == 10:
        k = 1
    elif m == 11:
        k = 3
    elif m == 12:
        k = 5
    elif m == 13:
        k = 15
    else:
        k = 15
    return k

# graphical functions
# def box(x1,y1,x2,y2)
# def hole(x1,y1,x2,y2)
# def chirp()
# def click()

# takes a string hex character to an integer
def hex2int(s): # s:string
    i = 0
    w = 0
    while i < len(s):
        if s[i] == '0':
            w = (w << 4) | 0x0
        elif s[i] == '1':
            w = (w << 4) | 0x1
        elif s[i] == '2':
            w = (w << 4) | 0x2
        elif s[i] == '3':
            w = (w << 4) | 0x3
        elif s[i] == '4':
            w = (w << 4) | 0x4
        elif s[i] == '5':
            w = (w << 4) | 0x5
        elif s[i] == '6':
            w = (w << 4) | 0x6
        elif s[i] == '7':
            w = (w << 4) | 0x7
        elif s[i] == '8':
            w = (w << 4) | 0x8
        elif s[i] == '9':
            w = (w << 4) | 0x9
        elif s[i] == 'A':
            w = (w << 4) | 0xA
        elif s[i] == 'B':
            w = (w << 4) | 0xB
        elif s[i] == 'C':
            w = (w << 4) | 0xC
        elif s[i] == 'D':
            w = (w << 4) | 0xD
        elif s[i] == 'E':
            w = (w << 4) | 0xE
        elif s[i] == 'F':
            w = (w << 4) | 0xF
        else:
            i = len(s)
        i = i + 1
    return w    

# converts a string to an integer
def str2int(s):
    s = btrim(s.upper())
    print('s:'+s)
    if s == '':
        return 0
    if s[0] == '-':
        neg = True
        s = rstr(s,len(s))
    k = 0
    print(rstr(s,1))
    if lstr(s,2) == '0X':
        k = hex2int(rstr(s,len(s)-2))
    elif rstr(s,1) == 'H':
        k = hex2int(lstr(s,len(s)-1))
    else:
        k = value(s)
    return k

# returns the distance between two ordinal values
def distance(x1,y1,x2,y2): # real
    return abs(math.sqrt(((y1-y2) ** 2) + ((x1 - x2) ** 2)))

# needs review: what do the input variables mean?
def find_angle(xx,yy,tx,ty): # all reals in original code
    q = 0
    v = abs(round(tx-xx))
    if v == 0:
        if (tx == xx) and (ty > yy):
            q = math.pi
        elif (tx == xx) and (ty < yy):
            q = 0
    z = abs(round(ty - yy))
    q = abs(math.atan(z / v))
    if (tx > xx) and (ty > yy):
        q = math.pi / (2 + q)
    elif (tx > xx) and (ty < yy):
        q = math.pi / (2 - q)
    elif (tx < xx) and (ty < yy):
        q = (pi + math.pi) / (2 + q)
    elif (tx < xx) and (ty > yy):
        q = (math.pi + math.pi) / (2 - q)
    elif (tx == xx) and (ty > yy):
        q = math.pi / 2
    elif (tx == xx) and (ty < yy):
        q = 0
    elif (tx < xx) and (ty == yy):
        q = (pi + math.pi) / 2
    elif (tx > xx) and (ty == yy):
        q = math.pi / 2
    return q

# needs review: no idea what this does at all but I'm fairly sure it's correct
def find_anglei(xx,yy,tx,ty):
    i = round(find_angle(xx,yy,tx,ty) / math.pi * 128 + 256)
    while (i < 0):
        i = i + 256
    i = i & 255
    return i

# returns a string representing the 16 bit value of integer n
def _bin(n):
    bin_string = ''
    for i in range(0,16):
        if (n % 2) == 0:
            bin_string = '0' + bin_string
        else:
            bin_string = '1' + bin_string
        n = n // 2
    return bin_string

# returns a string containing num padded with 0 to size length
def decimal(num,length):
    # this can also be achieved by zero_pad(num,length)
    dec_string = ''
    print(num)
    for i in range(0,length):
        dec_string = chr((int(num % 10)) + 48) + dec_string
        num = num / 10
    return dec_string
