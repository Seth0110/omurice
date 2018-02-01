pp#!/usr/bin/python3

# Copyright 2018 Seth Sevier

# Permission is hereby granted, free of charge, to any person obtainning a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

### Python3 port of ATRLOCK.PAS ###
# TODO:
# What is btrim()???
# Figure out how check if a filename is valid().
# Figure out where the read in line disappears, in encode() somewhere
# Should encode() be adding spaces between all the characters like it currently is?
# Find out of lstr() does what I expect

import os, pdb, random, sys, time

# REMOVE AFTER PORT IS COMPLETED
from subprocess import call
call(['rm','SNIPER.ATL']) 

LOCKTYPE = 3
lock_code = 0
lock_pos = 0
lock_dat = 0

def encode(s):
    global lock_pos
    global lock_code
    global lock_dat
    if lock_code != '':
        for i in s:
            lock_pos += 1
            if lock_pos > len(lock_code):
                lock_pos = 0
            if ((ord(i) in range(0,31)) or (ord(i) in range(128,255))):
                this_dat = ord(i) & 15
                i = chr((ord(i)) ^ ord(lock_code[lock_pos % len(lock_code)]) ^ lock_dat + 1)
                lock_dat = this_dat
    return s

def prepare(s1):
    s = ''
    # remove comments
    if (len(s1) == 0) or (s1[0] == ';'):
        s1 = ''
    else:
        k = 0
        for i in enumerate(reversed(s1),k):
            if i == ';':
                k = i
            if k > 0:
                s1 = s1[k - 1] ### This was originally lstr(s1,k - 1) 
    # remove excess spaces
    s2 = ''
    for i in range(0,len(s1)):
        if not (i in [' ','\b','\t','\n',',']):
            s2 = s2 + s1[i]
            if s2 != '':
                s = s + s2 # originally also added + ' '
                s2 = ''
    if s2 != '':
        s = s + s2
    return s

def write_line(s1):
    s = prepare(s1)
    if len(s) > 0:
        s = encode(s)
        f2.write(s + '\n')

random.seed(time.time())
lock_pos = 0
lock_dat = 0

if (len(sys.argv) < 2) | (len(sys.argv) > 4):
    print('Usage: ATRLOCK <robot[.at2]> [locked[.atl]]');
    sys.exit(0)
fn1 = sys.argv[1] # Needs a btrim()
if not fn1.endswith('.AT2'):
    fn1 = fn1 + '.AT2'
if not os.path.isfile(fn1):
    print('Robot "' + fn1 + '" not found!')
    sys.exit(0)
if len(sys.argv) == 3:
    fn2 = sys.argv[2] # Needs a btrim()
else:
    fn2 = os.path.splitext(fn1)[0] + '.ATL'
if not True: # should be a properly functioning valid(fn2):
    print('Output name "' + fn2 + '" not valid!')
    sys.exit(0)
if fn1 == fn2:
    print('Filenames can not be the same!')
    sys.exit(0)

f1 = open(fn1,'r')
f2 = open(fn2,'x')

# copy comment header
f2.write(';------------------------------------------------------------------------------\n')

for s in f1:
    if s[0] == ';':
        f2.write(s)
        s = f1.readline()
    else: break

# lock header
f2.write(';------------------------------------------------------------------------------\n')
f2.write('; ' + os.path.basename(fn1) + ' Locked on ' + time.strftime('%d/%m/%Y') + '\n')
f2.write(';------------------------------------------------------------------------------\n')
lock_code = ''
k = random.randint(0,20) + 20
for i in range(1,k):
   lock_code = lock_code + chr(random.randint(0,31) + 65)
f2.write('#LOCK' + str(LOCKTYPE) + ' ' + lock_code)

# decode lock-code
for i in lock_code:
    i = chr(ord(i) - 65)

print('Encoding "' + fn1 + '"...')


# encode robot
if len(s) > 0:
    write_line(s.upper())
f1.seek(0)
for s1 in f1:
    # read line
    s1 = f1.readline()
    s1 = s1.upper() # still needs a btrim function
    # write line
    write_line(s1)

print('Done. Used LOCK Format #' + str(LOCKTYPE) + '.')
print('Only ATR2 v2.08 or later can decode.')
print('LOCKed robot saved as "' + fn2 + '"')

f1.close()
f2.close()
