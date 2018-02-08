#!/usr/bin/python3

# Copyright 2018 Seth Sevier, Viktoria Koscinski, Myron Xu, Amurldin Jamalli, Steffan Sampson

# Permission is hereby granted, free of charge, to any person obtainning a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

### Python3 port of ATRLOCK.PAS ###
# TODO:
# Change software license to original
# Implement a filename validation function valid()
#
# Encryption algoritm not identical to ATRLOCK.EXE output
# - The logic of this program is equivalent to ATRLOCK.PAS
# - To get this to work, we need to figure out how '#' and 'V' makes '7'

import os, random, sys, time

# REMOVE AFTER PORT IS COMPLETED
import pdb
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
        t = ''
        for i in s:
            lock_pos += 1
            if lock_pos > len(lock_code):
                lock_pos = 0
            if ((ord(i) in range(0,32)) or (ord(i) in range(128,256))):
                i = ' '
            this_dat = ord(i) & 15
            t = t + chr((ord(i) ^ (ord(lock_code[lock_pos - 1]) ^ lock_dat)) + 1)
            lock_dat = this_dat
    return t

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
                s1 = s1[k - 1]
                
    # remove excess spaces
    s2 = ''
    for i in s1:
        if not (i in [' ','\b','\t','\n',',']):
            s2 = s2 + i
        elif s2 != '':
            s = s + s2 + ' '
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
    else: break

# lock header
f2.write(';------------------------------------------------------------------------------\n')
f2.write('; ' + os.path.basename(fn1) + ' Locked on ' + time.strftime('%d/%m/%Y') + '\n')
f2.write(';------------------------------------------------------------------------------\n')
lock_code = ''
k = random.randint(0,21) + 20
for i in range(1,k):
   lock_code = lock_code + chr(random.randint(0,31) + 65)
lock_code = 'VMWVRXAJZ\\M]RGRYG^T]AD[GIMTA]DILPZ\\' # remove line when done testing
f2.write('#LOCK' + str(LOCKTYPE) + ' ' + lock_code + '\n')

# decode lock-code
j = ''
for i in lock_code:
    j = j + chr(ord(i) - 65)

print('Encoding "' + fn1 + '"...')


# encode robot
s = s[1:-1]
if len(s) > 0:
    write_line(s.upper())
f1.seek(0)
for s1 in f1:
    # read line
    s1 = f1.readline()
    s1 = s1.upper() # still needs a btrim function
    s1 = s1[1:-1]
    # write line
    write_line(s1)

print('Done. Used LOCK Format #' + str(LOCKTYPE) + '.')
print('Only ATR2 v2.08 or later can decode.')
print('LOCKed robot saved as "' + fn2 + '"')

f1.close()
f2.close()
