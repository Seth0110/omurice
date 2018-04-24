#!/usr/bin/python

### A very incomplete to-do list, please add to this things you see wrong!##########################
# Robots aren't being compiled properly
# Need to figure out what keypressed is supposed to do, can use pygame for this, until then keypressed returns false

# keypressed basically shows whether a key was pressed or not but it
# unfortunately has something to do with checking the buffer (which is the 
# reason for all of those calls to 'clear buffer'). I'm not sure whether or not
# this'll cause a problem once we use Pygame. 
# More info: https://www.freepascal.org/docs-html/rtl/crt/keypressed.html 
####################################################################################################

# Copyright (c) 1999, Ed T. Toton III. All rights reserved.
#
# Bug fixes and additional additions Copyright (c) 2014, William "Amos" Confer

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:

#    Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.

#    Redistributions in binary form must reproduce the above copyright notice, 
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.

#    All advertising materials mentioning features or use of this software
#    must display the following acknowledgement:

#         This product includes software developed by Ed T. Toton III &
#         NecroBones Enterprises.

#    No modified or derivative copies or software may be distributed in the
#    guise of official or original releases/versions of this software. Such
#    works must contain acknowledgement that it is modified from the original.

#    Neither the name of the author nor the name of the business or
#    contributers may be used to endorse or promote products derived
#    from this software without specific prior written permission.

# THIS SOFTWARE IS PROVIDED BY THE AUTHOR AND CONTRIBUTORS ``AS IS'' AND ANY 
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED 
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE AUTHOR OR CONTRIBUTORS BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF
# THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

def keypressed():
    return False

from ATR2FUNC import *
import random
import time
import os
import pdb
import pygame
import sys

progname = 'AT-Robots'
version = '2.11'
cnotice1 = 'Copyright 1997 ''99, Ed T. Toton III'
cnotice2 = 'All Rights Reserved.'
cnotice3 = 'Copyright 2014, William "Amos" Confer'
main_filename = 'ATR2'
robot_ext = '.AT2'
locked_ext = '.ATL'
config_ext = '.ATS'
compile_ext = '.CMP'
report_ext = '.REP'
_T = True
_F = False
maxint = 32787
minint = -32768

# debugging/compiler
show_code = True
compile_by_line = False
max_var_len = 16
debugging_compiler = True

# robots
max_robots = 31  # starts at 0, so total is max_robots + 1
max_code = 1023  # same here
max_op = 3  # etc...
stack_size = 256
stack_base = 768
max_ram = 1023  # but this does start at 0 (odd #, 2 ^ n - 1)
max_vars = 256
max_labels = 256
acceleration = 4
turn_rate = 8
max_vel = 4
max_missiles = 1023
missile_spd = 32
hit_range = 14
blast_radius = 25
crash_range = 8
max_sonar = 250
com_queue = 512
max_queue = 255
max_config_points = 12
max_mines = 63
mine_blast = 35


# simulator & graphics

screen_scale = 0.46
screen_x = 5
screen_y = 5
robot_scale = 6
default_delay = 20
default_slice = 5

mine_circle = int(mine_blast * screen_scale) + 1
blast_circle = int(blast_radius * screen_scale) + 1
mis_radius = int(hit_range / 2.0) + 1
max_robot_lines = 8
# gray50 thing goes here

class op_rec:
    op = [0 for i in range(0, max_op + 1)]
    
prog_type = [op_rec() for i in range(0, max_code + 1)]
# note: must be careful when accessing values of prog_type if we need attribute of class

class config_rec:
    scanner = 0 
    weapon = 0
    armor = 0
    engine = 0
    heatsinks = 0
    shield = 0
    mines = 0

class mine_rec:
    x = 0
    y = 0
    detect = 0
    _yield = 0
    detonate = False

class robot_rec:
    is_locked = False
    mem_watch = 0
    x = 0
    y = 0
    lx = 0
    ly = 0
    xv = 0
    yv = 0
    speed = 0
    shotstrength = 0
    damageadj = 0
    speedadj = 0
    meters = 0
    hd = 0
    thd = 0
    lhd = 0
    spd = 0
    tspd = 0
    armor = 0
    larmor = 0
    heat = 0
    lheat = 0
    ip = 0
    plen = 0
    scanarc = 0
    accuracy = 0
    shift = 0
    err = 0
    delay_left = 0
    robot_time_limit = 0
    max_time = 0
    time_left = 0
    lshift = 0
    arc_count = 0
    sonar_count = 0
    scanrange = 0
    last_damage = 0
    last_hit = 0
    transponder = 0
    shutdown = 0
    channel = 0
    lendarc = 0
    endarc = 0
    lstartarc = 0
    startarc = 0
    mines = 0
    tx = [0 for i in range(0, max_robot_lines)]
    ltx = [0 for i in range(0, max_robot_lines)]
    ty = [0 for i in range(0, max_robot_lines)]
    lty = [0 for i in range(0, max_robot_lines)]
    wins = 0
    trials = 0
    kills = 0
    deaths = 0
    startkills = 0
    shots_fired = 0
    match_shots = 0
    hits = 0
    damage_total = 0
    cycles_lived = 0
    error_count = 0
    config = config_rec
    name = ''
    fn = ''
    shields_up = False
    lshields = False
    overburn = False
    keepshift = False
    cooling = False
    won = False
    code = prog_type
    ram = [0 for i in range(0, max_ram + 1)]
    mine = [mine_rec() for i in range(0, max_mines + 1)]
    errorlog = open('errorlog', 'a').close() # not sure who removed this/why, but it's needed by many functions
    
class missile_rec:
    x = 0
    y = 0
    lx = 0
    ly = 0
    mult = 0
    mspd = 0
    source = 0
    a = 0
    hd = 0
    rad = 0
    lrad = 0
    max_rad = 0

missile = []
missile = [missile_rec() for i in range(0, max_missiles + 1)]

robot = []
robot = [robot_rec() for i in range(-2, max_robots + 3)]

# NOTE: in the original code these were just declarations, I've picked values that make sense for them to have
# robot variables
num_robots = 2

# compiler variables
# f = open('f', 'a').close()
numvars = 0
numlabels = 0
maxcode = 0
lock_pos = 0
lock_dat = 0
varname = []
varname = ['' for i in range(1, max_vars + 1)]
varloc = []
varloc = [0 for i in range(1, max_vars + 1)]
labelname = []
labelname = ['' for i in range(1, max_vars + 1)]
labelnum = [x for x in range(max_labels)]
varnum = []
varnum = [0 for i in range(1, max_labels + 1)]
show_source = True
compile_only = False
lock_code = ''

# simulator/graphics variables
bout_over = False # made global from procedure bout
step_mode = 0     # 0=off, for (0<step_mode<=9) = #of game cycles per step
temp_mode = 0     # stores previous step_mode for return to step
step_count = 1    # step counter used as break flag
step_loop = False # break flag for stepping
# show_debugger = False # flag for viewing debugger panel vs. robot stats
matches = 1
played = 0
old_shields = False
insane_missiles = False
debug_info = False
windoze = False
no_gfx = False
logging_errors = False
timing = False
show_arcs = False
game_delay = 0
time_slice = 1
insanity = 0
update_timer = 1
max_gx = 1000
max_gy = 1000
stats_mode = 0
game_limit = 100
game_cycle = 0

# general settings
_quit = False
report = True
show_cnotice = False
kill_count = 0
report_type = 0

def operand(n,m):
    s = chr(n)
    #    Microcode:
    #  0 = instruction, number, constant
    #  1 = variable, memory access
    #  2 = :label
    #  3 = !label (unresolved)
    #  4 = !label (resolved)
    # 8h mask = inderect addressing (enclosed in [])
    x = m & 7
    if x == 1:
        s = '@' + s
    if x == 2:
        s = ':' + s
    if x == 3:
        s = '$' + s
    if x == 4:
        s = '!' + s
    else:
        s = cstr(n)
    if (m and 8) > 0:
        s = '[' + s + ']'
    return s

def mnemonic(n,m):
    s = chr(n)
    if m == 0:
        if n == 0:
            s = 'NOP'
        elif n == 1:
            s = 'ADD'
        elif n == 2:
            s = 'SUB'
        elif n == 3:
            s = 'OR'
        elif n == 4:
            s = 'AND'
        elif n == 5:
            s = 'XOR'
        elif n == 6:
            s = 'NOT'
        elif n == 7:
            s = 'MPY'
        elif n == 8:
            s = 'DIV'
        elif n == 9:
            s = 'MOD'
        elif n == 10:
            s = 'RET'
        elif n == 11:
            s = 'CALL'
        elif n == 12:
            s = 'JMP'
        elif n == 13:
            s = 'JLS'
        elif n == 14:
            s = 'JGR'
        elif n == 15:
            s = 'JNE'
        elif n == 16:
            s = 'JE'
        elif n == 17:
            s = 'SWAP'
        elif n == 18:
            s = 'DO'
        elif n == 19:
            s = 'LOOP'
        elif n == 20:
            s = 'CMP'
        elif n == 21:
            s = 'TEST'
        elif n == 22:
            s = 'MOV'
        elif n == 23:
            s = 'LOC'
        elif n == 24:
            s = 'GET'
        elif n == 25:
            s = 'PUT'
        elif n == 26:
            s = 'INT'
        elif n == 27:
            s = 'IPO'
        elif n == 28:
            s = 'OPO'
        elif n == 29:
            s = 'DELAY'
        elif n == 30:
            s = 'PUSH'
        elif n == 31:
            s = 'POP'
        elif n == 32:
            s = 'ERR'
        elif n == 33:
            s = 'INC'
        elif n == 34:
            s = 'DEC'
        elif n == 35:
            s = 'SHL'
        elif n == 36:
            s = 'SHR'
        elif n == 37:
            s = 'ROL'
        elif n == 38:
            s = 'ROR'
        elif n == 39:
            s = 'JZ'
        elif n == 40:
            s = 'JNZ'
        elif n == 41:
            s = 'JGE'
        elif n == 42:
            s = 'JLE'
        elif n == 43:
            s = 'SAL'
        elif n == 44:
            s = 'SAR'
        elif n == 45:
            s = 'NEG'
        elif n == 46:
            s = 'JTL'
        else:
            s = 'XXX'
    else:
        s = operand(n,m)
        return s

def log_error(n,i,ov):
    if not logging_errors:
        return
    else:
        for n in robot:
            if i == 1:
                s = 'Stack full - Too many CALLs?'
            elif i == 2:
                s = 'Label not found. Hmmm.'
            elif i == 3:
                s = 'Can\'t assign value - Tisk tisk.'
            elif i == 4:
                s = 'Illegal memory reference'
            elif i == 5:
                s = 'Stack empty - Too many RETs?'
            elif i == 6:
                s = 'Illegal instruction. How bizarre.'
            elif i == 7:
                s = 'Return out of range - Woops!'
            elif i == 8:
                s = 'Divide by zero'
            elif i == 9:
                s = 'Unresolved !label. WTF?'
            elif i == 10:
                s = 'Invalid Interrupt Call'
            elif i == 11:
                s = 'Invalid Port Access'
            elif i == 12:
                s = 'Com Queue empty'
            elif i == 13:
                s = 'No mine-layer, silly.'
            elif i == 14:
                s = 'No mines left'
            elif i == 15:
                s = 'No shield installed - Arm the photon torpedoes instead. :-)'
            elif i == 16:
                s = 'Invalid Microcode in instruction.'
            else:
                s = 'Unknown error'

            print(robot[n].errorlog + '<' + i + '> ' + s + ' (Line #' + robot[n].ip + ') [Cycle: ' + game_cycle + ', Match: ' + played + '/' + matches + ']\n')
            print(robot[n].errorlog + ' ' + mnemonic(robot[n].code[robot[n].ip].op[0] + robot[n].code[robot[n].ip].op[3] and 15) + '  ' + 
                  operand(robot[n].code[robot[n].ip].op[1] + (robot[n].code[robot[n].ip].op[3] >> 4) & 15) + ' +  ' + 
                  operand(robot[n].code[robot[n].ip].op[2] + (robot[n].code[robot[n].ip].op[3] >> 8) & 15))
            if ov != '':
                print(robot[n].errorlog + '    (Values: ' + ov + ')')
            else:
                print(robot[n].errorlog)
                
            print(robot[n].errorlog + ' AX=' + addrear(chr(robot[n].ram[65])+',',7))
            print(robot[n].errorlog + ' BX=' + addrear(chr(robot[n].ram[66])+',',7))
            print(robot[n].errorlog + ' CX=' + addrear(chr(robot[n].ram[67])+',',7))
            print(robot[n].errorlog + ' DX=' + addrear(chr(robot[n].ram[68])+',',7))
            print(robot[n].errorlog + ' EX=' + addrear(chr(robot[n].ram[69])+',',7))
            print(robot[n].errorlog + ' FX=' + addrear(chr(robot[n].ram[70])+',',7))
            print(robot[n].errorlog + ' Flags=' + robot[n].ram[64] + '\n')
            print(robot[n].errorlog + ' AX=' + addrear(hex(robot[n].ram[65])+',',7))
            print(robot[n].errorlog + ' BX=' + addrear(hex(robot[n].ram[66])+',',7))
            print(robot[n].errorlog + ' CX=' + addrear(hex(robot[n].ram[67])+',',7))
            print(robot[n].errorlog + ' DX=' + addrear(hex(robot[n].ram[68])+',',7))
            print(robot[n].errorlog + ' EX=' + addrear(hex(robot[n].ram[69])+',',7))
            print(robot[n].errorlog + ' FX=' + addrear(hex(robot[n].ram[70])+',',7))
            print(robot[n].errorlog + ' Flags=' + hex(robot[n].ram[64]))
            print(robot[n].errorlog)

def max_shown():
    if stats_mode == 1:
        return 12
    elif stats_mode == 2:
        return 32
    else:
        return 6
    
def graph_check(n):
    ok = True
    if (not graphix) or (n < 0) or (n > num_robots) or (n >= max_shown):
        ok = False
    return ok

def robot_graph(n):
    if stats_mode == 1:
        viewport(480,4+n*35,635,37+n*35)
        max_gx = 155
        max_gy = 33
    elif stats_mode == 2:
        viewport(480,4+n*13,635,15+n*13)
        max_gx = 155
        max_gy = 11
    else:
        viewport(480,4+n*70,n*70)
        max_gx = 155
        max_gy = 66
    setfillstyle(1,robot_color(n))
    setcolor(robot_color(n))

def update_armor(n):
    if graph_check(n) & step_mode <=0:
        #needs more work
        robot[n].n
        robot_graph(n)
        if robot[n].armor>0:
            if stats_mode == 1:
                bar(30,13,29+robot[n].armor,18)
                bar(88,3,87+(robot[n].armor >> 2),8)
            else:
                bar(30,25,29+robot[n].armor,30)
        setfillstyle(1,8)
        if robot[n].armor < 100:
            if stats_mode == 1:
                bar(30+robot[n].armor,13,129,18)
            elif stats_mode == 2:
                bar(88+(robot[n].armor >> 2), 3,111,8)
            else:
                bar(30+robot[n].armor,25,129,30)
                
def update_heat(n):
    if graph_check(n) & step_mode <= 0:
        robot[n].n
        robot_graph(n)
        if robot[n].heat > 5:
            if stats_mode == 1:
                bar(30,23,29+(robot[n].heat // 5), 28)
            elif stats_mode == 2:
                bar(127,3,126+(robot[n].heat // 20),8)
            else:
                bar(30,35,29+(robot[n].heat // 5),40)
        setfillstyle(1,8)
        if robot[n].heat<500:
            if stats_mode == 1:
                bar(30,(robot[n].heat // 5),23,129,28)
            elif stats_mode == 2:
                bar(127+(robot[n].heat // 20), 3,151,8) # find *(heat div 20)
            else:
                bar(30+(robot[n].heat // 5), 35,129,40)
                
def robot_error(n, i, ov):
    if graph_check(n) and step_mode <= 0:
        if stats_mode == 0:
            robot_graph(n)
            setfillstyle(1,0)
            bar(66,56,154,64)
            setcolor(robot_color(n))
            outtextxy(66,56,addrear(cstr(i), 7) + hex(i))
            chirp()
        if logging_errors:
            log_error(n,i,ov)
    robot[n].error_count +=1
            
def update_lives(n):
    if graph_check(n) and stats_mode == 0 and step_mode <= 0:
        robot[n].n
        robot_graph(n)
        setcolor(robot_color(n)-8)
        setfillstyle(1,0)
        bar(11,46,'K:')  # check K:
        outtextxy(11,46,'K:')
        outtextxy(29,46,zero_pad(robot[n].kills,4))
        outtextxy(80,46,'D:')   # check D:
        outtextxy(98,46,zero_pad(robot[n].deaths,4))

def update_cycle_window():
    if not graphix:
        print('\t' + 'Match ' + str(played) +  '/' + str(matches) + ', Cycle: ' + zero_pad(game_cycle,9))
    # else:
        # viewport(480,440,635,475)
        # setfillstyle(1,0)
        # bar(59,2,154,10)
        # setcolor(7)
        # outtextxy(75,03,zero_pad(game_cycle,9))
        
def setscreen():
    if not graphix:
        sys.exit()
    # BIG GRAPHICAL PART GOES HERE
    
def graph_mode(on):
    if on and not graphix:
        Graph_VGA
        cleardevice
        graphix = True
    else:
        if (not on) and graphix:
            closegraph
            graphix = False

def prog_error(n, ss):
    #graph_mode(False) # graphics related
    #textcolor(15) # graphics related
    print("Error #", n, ": ", end = '')
    if n == 0:
        s = ss
    elif n == 1:
        s = "Invalid :label - \"" + ss + "\", silly mortal."
    elif n == 2:
        s = "Undefined identifier - \"" + ss + "\". A typo perhaps?"
    elif n == 3:
        s = "Memory access out of range - \"" + ss + "\""
    elif n == 4:
        s = "Not enough robots for combat. Maybe we should just drive in circles."
    elif n == 5:
        s = "Robot names and settings must be specified. An empty arena is no fun."
    elif n == 6:
        s = "Config file not found - \"" + ss + "\""
    elif n == 7:
        s = "Cannot access a config file from a config file - \"" + ss + "\""
    elif n == 8:
        s = "Robot not found \"" + ss + "\". Perhaps you mistyped it?"
    elif n == 9:
        s = "Insufficient RAM to load robot: \"" + ss + "\"... This is not good."
    elif n == 10:
        s = "Too many robots! We can only handle " + str(max_robots + 1) + "! Blah.. limits are limits."
    elif n == 11:
        s = "You already have a perfectly good #def for \"" + ss + "\", silly."
    elif n == 12:
        s = "Variable name too long! (Max:" + str(max_var_len) + ") \"" + ss + "\""
    elif n == 13:
        s = "!Label already defined \"" + ss + "\", silly."
    elif n == 14:
        s = "Too many variables! (Var Limit: " + str(max_vars) + ")"
    elif n == 15:
        s  = "Too many !labels! (!Label Limit: " + str(max_labels) + ")"
    elif n == 16:
        s = "Robot program too long! Boldly we simplify, simplify along..." + ss
    elif n == 17:
        s = "!Label missing error. !Label #" + ss + "."
    elif n == 18:
        s = "!Label out of range: " + ss
    elif n == 19:
        s = "!Label not found. " + ss
    elif n == 20:
        s = "Invalid config option: \"" + ss + "\". Inventing a new device?"
    elif n == 21:
        s = "Robot is attempting to cheat; Too many config points (" + ss + ")"
    elif n == 22:
        s = "Insufficient data in data statement: \"" + ss + "\""
    elif n == 23:
        s = "Too many asterisks: \"" + ss + "\""
    elif n == 24:
        s = "Invalid step count: \"" + ss + "\""
    elif n == 25:
        s = "\"" + ss + "\""
    else:
        s = ss
    print(s)
    print()
    exit()   

def print_code(n, p):
    i = 0
    print(hex(p)+': ')
    for i in range(max_op):
        sys.stdout.write(str(zero_pad(robot[n].code[p].op[i],5)) + ' ')
    sys.stdout.write('=  ')
    for i in range(max_op):
        sys.stdout.write(str(hex(robot[n].code[p].op[i])) + 'h ')
    print('\n')

def parse1(n, p, s):
    global numlabels
    ss = ''
    for i in range(max_op-1):
        k = 0
        found = False
        opcode = 0
        microcode = 0
        s[i] = btrim(ucase(s[i]))
        indirect = False
        # Microcode:
        #  0 = instruction, number, constant
        #  1 = variable, memory access
        #  2 = :label
        #  3 = !label (unresolved)
        #  4 = !label (resolved)
        # 8h mask = inderect addressing (enclosed in [])
        if s[i] == '':
            opcode = 0
            microcode = 0
            found = True
        if lstr(s[i], 1) == '[' and (rstr(s[i], 1) == ']'):
            s[i] = copy(s[i], 2, len(s[i]) - 2)
            indirect = True        
        if (not found) and (s[i][0] == '!'):
            ss = s[i]
            ss = btrim(rstr(ss,len(ss)-1))
            if numlabels > 0:
                for j in range(1,numlabels):
                    if ss == labelname[i]:
                        found = True
                        if labelnum[j] > 0:
                            opcode = labelnum[j]
                            microcode = 4    # resovled !label
                        else:
                            opcode = j  
                            microcode = 3    # unresovled !label
        if not found:
            numlabels +=1
            if numlabels>max_labels:
                prog_error(15, ' ')
            else:
                labelname[numlabels] = ss
                labelnum[numlabels] = -1
                opcode = numlabels
                microcode = 3   # unresolved !label
                found = True        
        if numvars > 0 and not found:            
            for j in range(1,numvars):
                if s[i] == varname[j]:
                    opcode = varloc[j]
                    microcode = 1
                    found = True
        # instructions
        if s[i] == 'NOP':
            opcode = 000
            found = True
        elif s[i] == 'ADD':
            opcode = 1
            found = True
        elif s[i] == 'SUB':
            opcode = 2
            found = True
        elif s[i] == 'OR':
            opcode = 3
            found = True
        elif s[i] == 'AND':
            opcode = 4
            found = True
        elif s[i] == 'XOR':
            opcode = 5
            found = True
        elif s[i] == 'NOT':
            opcode = 6
            found = True
        elif s[i] == 'MPY':
            opcode = 7
            found = True
        elif s[i] == 'DIV':
            opcode == 7
            found = True
        elif s[i] == 'MOD':
            opcode= 9
            found= True
        elif s[i] == 'RET':
            opcode = 10
            found = True
        elif s[i] == 'RETURN':
            opcode = 10
            found = True
        elif s[i] == 'GSB':
            opcode = 11
            found = True
        elif s[i] == 'GOSUB':
            opcode = 11
            found = True
        elif s[i] == 'CALL':
            opcode = 11
            found = True
        elif s[i] == 'JMP':
            opcode = 12
            found = True
        elif s[i] == 'JUMP':
            opcode = 12
            found = True
        elif s[i] == 'GOTO':
            opcode = 12
            found = True
        elif s[i] == 'JLS':
            opcode = 13
            found = True
        elif s[i] == 'JB':
            opcode = 13
            found = True
        elif s[i] == 'JGR':
            opcode = 14
            found = True
        elif s[i] == 'JA':
            opcode = 14
            found = True
        elif s[i] == 'JNE':
            opcode = 15
            found = True
        elif s[i] == 'JEQ':
            opcode = 16
            found = True
        elif s[i] == 'JE':
            opcode = 16
            found = True
        elif s[i] == 'XCHG':
            opcode = 17
            found = True
        elif s[i] == 'SWAP':
            opcode = 17
            found = True
        elif s[i] == 'DO':
            opcode = 18
            found= True
        elif s[i] == 'LOOP':
            opcode = 19
            found = True
        elif s[i] == 'CMP':
            opcode = 20
            found = True
        elif s[i] == 'TEST':
            opcode = 21
            found = True
        elif s[i] == 'SET':
            opcode = 22
            found = True
        elif s[i] == 'MOV':
            opcode = 22
            found = True
        elif s[i] == 'LOC':
            opcode = 23
            found = True
        elif s[i] == 'ADDR':
            opcode = 23
            found = True
        elif s[i] == 'GET':
            opcode = 24
            found= True
        elif s[i] == 'PUT':
            opcode = 25
            found = True
        elif s[i] == 'INT':
            opcode = 26
            found = True
        elif s[i] == 'IPO':
            opcode = 27
            found = True
        elif s[i] == 'IN':
            opcode = 27
            found = True
        elif s[i] == 'OPO':
            opcode = 28
            found = True
        elif s[i] == 'OUT':
            opcode = 28
            found = True
        elif s[i] == 'DEL':
            opcode = 29
            found = True
        elif s[i] == 'DELAY':
            opcode = 29
            found = True
        elif s[i] == 'PUSH':
            opcode = 30
            found = True
        elif s[i] == 'POP':
            opcode = 31
            found = True
        elif s[i] == 'ERR':
            opcode = 32
            found = True
        elif s[i] == 'ERROR':
            opcode = 32
            found = True
        elif s[i] == 'INC':
            opcode = 33
            found = True
        elif s[i] == 'DEC':
            opcode = 34
            found = True
        elif s[i] == 'SHL':
            opcode = 35
            found = True
        elif s[i] == 'SHR':
            opcode == 36
            found = True
        elif s[i] == 'ROL':
            opcode = 37
            found = True
        elif s[i] == 'ROR':
            opcode = 37
            found = True
        elif s[i] == 'JZ':
            opcode = 39
            found = True
        elif s[i] == 'JNZ':
            opcode = 40
            found = True
        elif s[i] == 'JAE':
            opcode = 41
            found = True
        elif s[i] == 'JGE':
            opcode = 41
            found = True
        elif s[i] == 'JLE':
            opcode = 42
            found = True
        elif s[i] == 'JBE':
            opcode = 42
            found = True
        elif s[i] == 'SAL':
            opcode = 43
            found = True
        elif s[i] == 'SAR':
            opcode = 44
            found = True
        elif s[i] == 'NEG':
            opcode = 45
            found = True
        elif s[i] == 'JTL':
            opcode = 46
            found = True        
        # registers 
        elif s[i] == 'COLCNT':
            opcode = 8
            microcode = 1
            found = True
        elif s[i] == 'METERS':
            opcode = 9
            microcode = 1
            found = True
        elif s[i] == 'COMBASE':
            opcode = 10
            microcode = 1
            found = True
        elif s[i] == 'COMEND':
            opcode = 11
            microcode = 1
            found = True
        elif s[i] == 'FLAGS':
            opcode = 64
            microcode = 1
        elif s[i] == 'AX':
            opcode = 64
            microcode = 1
            found = True
        elif s[i] == 'BX':
            opcode = 66
            microcode = 1
            found = True
        elif s[i] == 'CX':
            opcode = 67
            microcode = 1
            found = True
        elif s[i] == 'DX':
            opcode = 68
            microcode = 1
            found = True
        elif s[i] == 'EX':
            opcode = 69
            microcode = 1
            found = True
        elif s[i] == 'FX':
            opcode = 70
            microcode = 1
            found = True
        elif s[i] == 'SP':
            opcode = 71
            microcode = 1
            found = True
        # constants
        elif s[i] == 'MAXINT':
            opcode = 32767
            microcode = 0
            found = True
        elif s[i] == 'MININT':
            opcode = 32768
            microcode = 0
            found = True
        
        elif s[i] == 'P_SPEDOMETER':
            opcode = 1
            microcode = 0
            found = True
        elif s[i] == 'P_HEAT':
            opcode = 2
            microcode = 0
            found = True
            
        elif s[i] == 'P_COMPASS':
            opcode = 3 
            microcode = 0
            found = True
        
        elif s[i] == 'P_TANGLE':
            opcode = 4
            microcode = 0
            found = True
        
        elif s[i] == 'P_TURRENT_OFS':
            opcode = 4
            microcode = 0
            found = True
        elif s[i] == 'P_THEADING':
            opcode = 5
            microcode = 0
            found = True
        elif s[i] == 'P_TURRENT_ABS':
            opcode = 5
            microcode = 0
            found = True
        
        elif s[i] == 'P_ARMOR':
            opcode = 6
            microcode = 0
            found = True
        
        elif s[i] == 'P_DAMAGE':
            opcode = 6
            microcode = 0
            found = True
        elif s[i] == 'P_SCAN':
            opcode = 7
            microcode = 0
            found = True
        elif s[i] == 'P_ACCURACY':
            opcode = 8
            microcode = 0
            found = True
        elif s[i] == 'P_RADAR':
            opcode = 9
            microcode = 0
            found = True
        elif s[i] == 'P_RANDOM':
            opcode = 10
            microcode = 0
            found = True
        elif s[i] == 'P_RAND':
            opcode = 10
            microcode = 0
            found = True
        elif s[i] == 'P_THROTTLE':
            opcode = 11
            microcode = 0
            found = True
        
        elif s[i] == 'P_TROTATE':
            opcode = 12
            microcode = 0
            found = True
        elif s[i] == 'P_OFS_TURRENT':
            opcode = 12
            microcode = 0
            found = True
        elif s[i] == 'P_TAIM':
            opcode = 13
            microcode = 0
            found = True
        elif s[i] == 'P_ABS_TURRENT':
            opcode = 13
            microcode = 0
            found = True
        elif s[i] == 'P_STEERLING':
            opcode = 14
            microcode = 0
            found = True
        elif s[i] == 'P_WEAP':
            opcode = 15
            microcode = 0
            found = True
        elif s[i] == 'P_WEAPON':
            opcode = 15
            microcode = 0
            found = True
        elif s[i] == 'P_FIRE':
            opcode = 15
            microcode = 0
            found = True
        elif s[i] == 'P_SONAR':
            opcode = 16
            microcode = 0
            found = True
        elif s[i] == 'P_ARC':
            opcode = 17
            microcode = 0
            found = True
        elif s[i] == 'P_SCANARC':
            opcode = 17
            microcode = 0
            found = True
        elif s[i] == 'P_OVERBURN':
            opcode = 18
            microcode = 0
            found = True
        elif s[i] == 'P_TRANSPONDER':
            opcode = 19
            microcode = 0
            found = True
        elif s[i] == 'P_SHUTDOWN':
            opcode = 20
            microcode = 0
            found = True
        elif s[i] == 'P_CHANNEL':
            opcode = 21
            microcode = 0
            found = True
        elif s[i] == 'P_MINELAYER':
            opcode = 22
            microcode = 0
            found = True
        elif s[i] == 'P_MINETRIGGER':
            opcode = 23
            microcode = 0
            found = True
        elif s[i] == 'P_SHIELD':
            opcode = 24
            microcode = 0
            found = True
        elif s[i] == 'P_SHIELDS':
            opcode = 24
            microcode = 0
            found = True
        elif s[i] == 'I_DESTRUCT':
            opcode = 0
            microcode = 0
            found = True
        elif s[i] == 'I_RESET':
            opcode = 1
            microcode = 0
            found = True
        elif s[i] == 'I_LOCATE':
            opcode = 2
            microcode = 0
            found = True
        elif s[i] == 'I_KEEPSHELIFT':
            opcode = 3
            microcode = 0
            found = True
        elif s[i] == 'I_OVERBURN':
            opcode = 4
            microcode = 0
            found = True
        elif s[i] == 'I_ID':
            opcode = 5
            microcode = 0
            found = True
        elif s[i] == 'I_TIMER':
            opcode = 6
            microcode = 0
            found = True
        elif s[i] == 'I_ANGLE':
            opcode = 7
            microcode = 0
            found = True
        elif s[i] == 'I_TID':
            opcode = 8
            microcode = 0
            found = True
        elif s[i] == 'I_TARGETID':
            opcode = 8
            microcode = 0
            found = True
        elif s[i] == 'I_TINFO':
            opcode = 9
            microcode = 0
            found = True
        elif s[i] == 'I_TARGETINFO':
            opcode = 9
            microcode = 0
            found = True
        
        elif s[i] == 'I_GINFO':
            opcode = 10
            microcode = 0
            found = True
        elif s[i] == 'I_GAMEINFO':
            opcode = 10
            microcode = 0
            found = True
        elif s[i] == 'I_RINFO':
            opcode = 11
            microcode = 0
            found = True
        elif s[i] == 'I_ROBOTINFO':
            opcode = 11
            microcode = 0
            found = True
        elif s[i] == 'I_COLLISIONS':
            opcode = 13
            microcode = 0
            found = True
        elif s[i] == 'I_RESETCOLCNT':
            opcode = 13
            microcode = 0
            found = True
        
        elif s[i] == 'I_TRANSMIT':
            opcode = 14
            microcode = 0
            found = True
        
        elif s[i] == 'I_RECEIVE':
            opcode = 15
            microcode = 0
            found = True
        elif s[i] == 'I_DATAREADY':
            opcode = 16
            microcode = 0
            found = True
        elif s[i] == 'I_CLEARCOM':
            opcode = 17
            microcode = 0
            found = True
        elif s[i] == 'I_KILLS':
            opcode = 18
            microcode = 0
            found = True
        elif s[i] == 'I_DEATHS':
            opcode = 18
            microcode = 0
            found = True
        elif s[i] == 'I_CLEARMETERS':
            opcode = 19
            microcode = 0
            found = True
        # memory addresses
        if (not found) and \
           (s[i][1] == '@') and \
           s[i][2].isdigit():
            opcode = str2int(rstr(s[i], len(s[i])-1))
            if(opcode < 0) or (opcode > (max_ram + 1) + ((max_code + 1) << 3) - 1):
                prog_error(3,s[i])
                microcode = 1
                found = True
                
                if (not found) and s[i][1].isdigit():
                    opcode = str2int(s[i])
                    found = True
                    
                if found:
                    robot[n].code[p].op[i] = opcode
                    if indirect:
                        microcode = microcode | 8
                        robot[n].code[p].op[max_op] = robot[n].code[p].op[max_op] or (microcode << (i*4)) # check
                elif s[i] !='':
                    prog_error(2,s[i])
    
    if show_code:
        print_code(n,p)
    if compile_by_line:
        readkey()

def check_plen(plen):
    if plen > maxcode:
        prog_error(16,'\t\nMaximum program length exceeded, (Limit: ' + cstr(maxcode+1) + ' compiled lines)')

def _compile(n, filename):
    global numvars
    global numlabels
    lc = ''
    lock_code = ''
    lock_pos = 0
    locktype = 0
    lock_dat = 0
    pp = [''] * max_op
    if not os.path.isfile(filename):
        prog_error(8, filename)
    # textcolor(robot_color(n))
    print('Compiling robot #' + str(n + 1) + ': ' + filename)
    robot[n].is_locked = False
    # textcolor(robot_color(n))
    numvars = 0
    numlabels = 0
    for k in range(max_code):
        for i in range(max_op):
            robot[n].code[k].op[i] = 0
    robot[n].plen = 0
    f = open(filename, 'r')
    s = ''
    linecount = 0
    for line in f:
        if s == '#END': # and plen <= maxcode
            break
        s = line
        linecount += 1
        if locktype < 3:
            lock_pos = 0
        if lock_code != '':
            for i in s:
                lock_pos += 1
                if lock_pos > len(lock_code):
                    lock_pos = 0
                if locktype == 3:
                    s[i] = chr((ord(s[i]) - 1) ^ (ord(lock_code[lock_pos]) ^ lock_dat))
                elif locktype == 2:
                    s[i] = chr(ord(s[i]) ^ (ord(lock_code[lock_pos]) ^ 1))
                else:
                    s[i] = chr(ord(s[i]) ^ ord(lock_code[lock_pos]))
                lock_dat = ord(s[i]) & 15
        s = btrim(s)
        orig_s = s
        t = ''
        for i in s:
            if ord(i) in range(0,33) or ord(i) in range(128,256) or i == ',':
                t += ' '
            else:
                t += i
        s = t
        if show_source and ((lock_code == '') or debugging_compiler):
            print(zero_pad(linecount, 3) + ':' + zero_pad(robot[n].plen, 3) + ' ' + s)
        if debugging_compiler:
            if pygame.key.get_pressed() == chr(27):
                sys.exit()
        k = -1
        for i in range(len(t) - 1, -1, -1):
            if s[i] == ';':
                k = i
        if k == 0:
            s = ''
        elif k > 0:
            s = s[0:k - 1]
            s = s[k:]
        s = btrim(s.upper())
        # for i in range(max_op):
        #    pp.append('') # This is already at length max_op?!
        if (len(s) > 0) and (s[0] != ';'):
            if s[0] == '#': # Compiler Directives
                s1 = btrim(rstr(s,len(s)-1)).upper()
                msg = btrim(rstr(orig_s, len(orig_s) - 5))
                k = 0
                for i in range(0, len(s1)):
                    if (k == 0) and (s1[i] == ' '):
                        k = i
                k -= 1
                if k > 1:
                    s2 = lstr(s1, k + 1)
                    s3 = btrim(rstr(s1, len(s1) - k)).upper()
                    k = 0
                    if numvars > 0:
                        for i in range(0, numvars):
                            if s3 == varname[i]:
                                k = i
                    if (s2 == 'DEF') and (numvars < max_vars):
                        if len(s3) > max_var_len:
                            prog_error(12, s3)
                        elif k > 0:
                            prog_error(11, s3)
                        else:
                            numvars += 1
                            if numvars > max_vars:
                                prog_error(14, '')
                            else:
                                varname[numvars - 1] = s3
                                varloc[numvars - 1] = 127 + numvars
                    elif (lstr(s2, 4) == 'LOCK'):
                        is_locked = True
                        if len(s2) > 4:
                            locktype = value(rstr(s2, len(s2) - 4))
                            lock_code = btrim(s3.upper())
                            print('Robot is of LOCKed format from this point forward. [' + locktype + ']')
                                # print('Using key: "', lock_code, '"')
                            for i in range(len(lock_code)):
                                lock_code[i] = chr(ord(lock_code[i]) - 65)
                    elif s2 == 'MSG':
                        name = msg
                    elif s2 == 'TIME':
                        robot_time_limit = value(s3)
                        if robot_time_limit < 0:
                            robot_time_limit = 0
                    elif s2 == 'CONFIG':
                        if lstr(s3, 8) == 'SCANNER=':
                            robot[n].config.scanner = value(rstr(s3, len(s3) - 8))
                        elif lstr(s3, 7) == 'SHIELD=':
                            robot[n].config.shield == value(rstr(s3, len(s3) - 7))
                        elif lstr(s3, 7) == 'WEAPON=':
                            robot[n].config.weapon = value(rstr(s3, len(s3) - 7))
                        elif lstr(s3, 6) == 'ARMOR=':
                            robot[n].config.armor = value(rstr(s3, len(s3) - 6))
                        elif lstr(s3, 7) == 'ENGINE=':
                            robot[n].config.engine = value(rstr(s3, len(s3) - 7))
                        elif lstr(s3, 10) == 'HEATSINKS=':
                            robot[n].config.heatsinks = value(rstr(s3,len(s3) - 10))
                        elif lstr(s3, 6) == 'MINES=':
                            robot[n].config.mines = value(rstr(s3, len(s3) - 6))
                        else:
                            prog_error(20, s3)
                        if robot[n].config.scanner < 0:
                            robot[n].config.scanner = 0
                        if robot[n].config.scanner > 5:
                            robot[n].config.scanner = 5
                        if robot[n].config.weapon < 0:
                            robot[n].config.weapon = 0
                        if robot[n].config.weapon > 5:
                            robot[n].config.weapon = 5
                        if robot[n].config.armor < 0:
                            robot[n].config.armor = 0
                        if robot[n].config.armor > 5:
                            robot[n].config.armor = 5
                        if robot[n].config.engine < 0:
                            robot[n].config.engine = 0
                        if robot[n].config.engine > 5:
                            robot[n].config.engine = 5
                        if robot[n].config.heatsinks < 0:
                            robot[n].config.heatsinks = 0
                        if robot[n].config.heatsinks > 5:
                            robot[n].config.heatsinks = 0
                        if robot[n].config.mines < 0:
                            robot[n].config.mines = 0
                        if robot[n].config.mines > 5:
                            robot[n].config.mines = 5
                    else:
                        print('Warning: unknown directive "' + s2 + '"')
            if s[0] == '*': # Inline Pre-Compiled Machine Code
                print('Inline Machine Code')
                check_plen(robot[n].plen)
                for i in range(max_op):
                    pp[i] = ''
                for i in range(1,len(s)):
                    if s[i] == '*':
                        prog_error(23, s)
                k = 0
                i = 1
                s1 = ''
                if len(s) <= 2:
                    prog_error(22, s)
                while (i < len(s)) and (k <= max_op):
                    i += 1
                    if ord(s[i]) in [x in range(33,42), x in range(43,128)]:
                        pp[k] = pp[k] + s[i]
                    elif ord(s[i]) in [x in range(0,33), x in range(128, 256)] and ord(s[i-1]) in [x in range(33, 42), x in range(43, 128)]:
                        k += 1
                for i in range(max_op):
                    robot[n].code[robot[n].plen].op[i] = str2int(pp[i])
                robot[n].plen += 1
            if s[0] == ':': # :labels
                check_plen(robot[n].plen)
                s1 = rstr(s, len(s) - 1)
                for i in range(1, len(s1)):
                    if not int(s1[i]) in range(10):
                        print(i)
                        prog_error(1, s)
                robot[n].code[robot[n].plen].op[0] = str2int(s1)
                robot[n].code[robot[n].plen].op[max_op] = 2
                if show_code:
                    print_code(n, robot[n].plen)
                robot[n].plen += 1
            if s[0] == '!': # !labels
                check_plen(robot[n].plen)
                s1 = btrim(rstr(s, len(s) - 1))
                k = 0
                for i in range(len(s1) - 1,0,-1):
                    if s1[i] in [';', chr(8), chr(9), chr(10), ' ', ',']:
                        k = i
                if k > 0:
                    s1 = lstr(s1, k - 1)
                    k = 0
                    for i in range(numlabels):
                        if labelname[i] == s1:
                            if labelnum[i] >= 0:
                                prog_error(13, '"!' + s1 + '" (' + cstr(labelnum[i]) + ')')
                                k = i
                    if k == 0:
                        numlabels += 1
                        if numlabels > max_labels:
                            prog_error(15, '')
                        k = numlabels
                    labelname[k] = s1
                    labelnum[k] = robot[n].plen
            else: # Instructions/Numbers
                check_plen(robot[n].plen)
                # Parse instructions
                # Remove comments
                k = 0
                for i in range(len(s)-1, 0, -1):
                    if s[i] == ';':
                        k = i
                if k >= 0:
                    s = lstr(s, k - 1)
                # Setup variables for parsing
                k = 0
                for j in range(max_op):
                    pp[j] = ''
                for j in range(len(s)):
                    c = s[j]
                    if not c in [' ', chr(8), chr(9), chr(10), ','] and k <= max_op:
                        pp[k] = pp[k] + c
                    elif not lc in [' ', chr(8), chr(9), chr(10), ',']:
                        k = k + 1
                lc = c
                parse1(n, robot[n].plen, pp)
                robot[n].plen += 1
    f.close()
    # Add our implied NOP if there's room. This was originally to make sure
    # no one tries using an empty robot program, kinda pointless otherwise
    if robot[n].plen <= maxcode:
        for i in range(max_op):
            pp[i] = ''
        pp[0] = 'NOP'
        parse1(n, robot[n].plen, pp)
    else:
        robot[n].plen -= 1

    # second pass, resolving !labels
    if numlabels > 0:
        for i in range(robot[n].plen):
            for j in range(max_op - 1):
                if robot[n].code[i].op[max_op] >> (j * 4) == 3: # unresolved !label
                    k = robot[n].code[i].op[j]
                    if k > 0 and k <= numlabels:
                        l = labelnum[k]
                        if l < 0:
                            prog_error(19, '"!' + labelname[k] + '" (' + cstr(l) + ')')
                        if l < 0 or l > maxcode:
                            prog_error(18, '"!' + labelname[k] + '" (' + cstr(l) + ')')
                        else:
                            robot[n].code[i].op[j] = l
                            mask = not (0xF << (j * 4))
                            robot[n].code[i].op[max_op] = (robot[n].code[i].op[max_op] and mask) or (4 << (j * 4))
                    else:
                        prog_error(17, cstr(k))
    # textcolor(7)
                                
def robot_config(n):
    if robot[n].config.scanner == 5:
        robot[n].scanrange = 1500
    elif robot[n].config.scanner == 4:
        robot[n].scanrange = 1000
    elif robot[n].config.scanner == 3:
        robot[n].scanrange = 700
    elif robot[n].config.scanner == 2:
        robot[n].scanrange = 500
    elif robot[n].config.scanner == 1:
        robot[n].scanrange = 350
    else:
        robot[n].scanrange = 250
        
    if robot[n].config.weapon == 5:
        robot[n].shotstrength = 1.5
    elif robot[n].config.weapon == 4:
        robot[n].shotstrength = 1.35
    elif robot[n].config.weapon == 3:
        robot[n].shotstrength = 1.2
    elif robot[n].config.weapon == 2:
        robot[n].shotstrength = 1
    elif robot[n].config.weapon == 1:
        robot[n].shotstrength = 0.8
    else:
        robot[n].shotstrength = .5
        
    if robot[n].config.armor == 5:
        robot[n].damageadj = 0.66
        robot[n].speedadj = 0.66
    elif robot[n].config.armor == 4:
        robot[n].damageadj = 0.77
        robot[n].speedadj = 0.75
    elif robot[n].config.armor == 3:
        robot[n].damageadj = 0.83
        robot[n].speedadj = 0.85
    elif robot[n].config.armor == 2:
        robot[n].damageadj = 1
        robot[n].speedadj = 1
    elif robot[n].config.armor == 1:
        robot[n].damageadj = 1.5
        robot[n].speedadj = 1.2
    else:
        robot[n].damageadj = 2
        robot[n].speedadj = 1.33
        
    if robot[n].config.engine == 5:
        robot[n].speedadj = robot[n].speedadj * 1.5
    elif robot[n].config.engine == 4:
        robot[n].speedadj = robot[n].speedadj * 1.35
    elif robot[n].config.engine == 3:
        robot[n].speedadj = robot[n].speedadj * 1.2
    elif robot[n].config.engine == 2:
        robot[n].speedadj = robot[n].speedadj * 1
    elif robot[n].config.engine == 1:
        robot[n].speedadj = robot[n].speedadj * 0.8
    else:
        robot[n].speedadj = robot[n].speedadj * 0.5
            
        # heatsinks are handled seperately
        if robot[n].config.mines == 5:
            robot[n].mines = 24
        elif robot[n].config.mines == 4:
            robot[n].mines = 16
        elif robot[n].config.mines == 3:
            robot[n].mines = 10
        elif robot[n].config.mines == 2:
            robot[n].mines = 6
        elif robot[n].config.mines == 1:
            robot[n].mines = 4
        else:
            robot[n].mines = 2
            robot[n].config.mines = 0
            
        robot[n].shields_up = False
        if (robot[n].config.shield < 3) or (robot[n].config.shield > 5):
            robot[n].config.shield = 0
        if (robot[n].config.heatsinks < 0) or (robot[n].config.heatsinks > 5):
            robot[n].config.heatsinks = 0
        
def reset_software(n):
    for i in range(0, max_ram):
        robot[n].ram[i] = 0
        robot[n].ram[71] = 768
        robot[n].thd = robot[n].hd
        robot[n].tspd = 0
        robot[n].scanarc = 8
        robot[n].shift = 0
        robot[n].err = 0
        robot[n].overburn = False
        robot[n].keepshift = False
        robot[n].ip = 0
        robot[n].accuracy = 0
        robot[n].meters = 0
        robot[n].delay_left = 0
        robot[n].time_left = 0
        robot[n].shields_up = False
            
def reset_hardware(n):
    for i in range(max_robot_lines):
        robot[n].ltx[i] = 0
        robot[n].tx[i] = 0
        robot[n].lty[i] = 0
        robot[n].ty[i] = 0
        while True:
            robot[n].x = random.randint(0, 999)
            robot[n].y = random.randint(0, 999)
            dd = 1000
            for i in range(0, num_robots + 1):
                if robot[i].x < 0:
                    robot[i].x = 0
                if robot[i].x > 1000:
                    robot[i].x = 1000
                if robot[i].y < 0:
                    robot[i].y = 0
                if robot[i].y > 1000:
                    robot[i].y = 1000
                d = distance(robot[n].x, robot[n].y, robot[i].x, robot[i].y) 
                if((robot[i].armor > 0) and (i != n) and (d < dd)):
                    dd = d
            if dd > 32:
                break
        for i in range(0, max_mines + 1):
            robot[n].mine[i].x = -1 
            robot[n].mine[i].y = -1
            robot[n].mine[i]._yield = 0
            robot[n].mine[i].detonate = False
            robot[n].mine[i].detect = 0
        robot[n].lx = -1
        robot[n].ly = -1
        robot[n].hd = random.randint(0, 255)
        robot[n].shift = 0
        robot[n].lhd = robot[n].hd + 1
        robot[n].lshift = robot[n].shift + 1
        robot[n].spd = 0
        robot[n].speed = 0
        robot[n].cooling = False
        robot[n].armor = 100
        robot[n].larmor = 0
        robot[n].heat = 0
        robot[n].lheat = 1
        robot[n].match_shots = 0
        robot[n].won = False
        robot[n].last_damage = 0
        robot[n].last_hit = 0
        robot[n].transponder = n + 1
        robot[n].meters = 0
        robot[n].shutdown = 400 
        robot[n].shields_up = False
        robot[n].channel = robot[n].transponder
        robot[n].startkills = robot[n].kills
        robot_config(n) 

def init_robot(n):
    robot[n].wins = 0
    robot[n].trials = 0
    robot[n].kills = 0
    robot[n].deaths = 0
    robot[n].shots_fired = 0
    robot[n].match_shots = 0
    robot[n].hits = 0
    robot[n].damage_total = 0
    robot[n].cycles_lived = 0
    robot[n].error_count = 0
    robot[n].plen = 0
    robot[n].max_time = 0
    robot[n].name = ''
    robot[n].fn = ''
    robot[n].speed = 0
    robot[n].arc_count = 0
    robot[n].robot_time_limit = 0
    robot[n].scanrange = 1500
    robot[n].shotstrength = 1
    robot[n].damageadj = 1
    robot[n].speedadj = 1
    robot[n].mines = 0
    robot[n].config.scanner = 5
    robot[n].config.weapon = 2
    robot[n].config.armor = 2
    robot[n].config.engine = 2
    robot[n].config.heatsinks = 1
    robot[n].config.shield = 0
    robot[n].config.mines = 0
    for i in range(0, max_ram + 1):
        robot[n].ram[i] = 0
    robot[n].ram[71] = 768
    for i in range(0, max_code + 1):
        for k in range(0, max_op + 1):
            robot[n].code[i].op[k] = 0
    reset_hardware(n) 
    reset_software(n)
    
def create_robot(n, filename):
    #if maxavail < sizeof(robot_rec): # commented out since this will not be a problem on today's computers
        #prog_error(9, base_name(no_path(filename))) 
    robot[n] 
    filename = ucase(btrim(filename))
    if filename == filename.split('.')[0]: # base_name(filename) originally
        if filename[0] == '?':
            filename = filename + locked_ext
        else:
            filename = filename + robot_ext
    if filename[0] == '?':
        filename = rstr(filename, len(filename) - 1)
    robot[n].fn = filename.split('/')[-1].split('.')[0] # no_path takes "dksjl/ kdsjlf/dlj" and gives you all after the last slash
    _compile(n, filename)
    robot_config(n) 
    k = robot[n].config.scanner + robot[n].config.armor + robot[n].config.weapon + robot[n].config.engine + robot[n].config.heatsinks + robot[n].config.shield + robot[n].config.mines
    if k > max_config_points:
        prog_error(21, cstr(k) + '/' + cstr(max_config_points))

def shutdown():
    #graph_mode(False) # graphics
    if show_cnotice:
        #textcolor(3) # graphics
        print(progname, '', version, '')
        print(cnotice1)
        print(cnotice2)
        print(cnotice3)
    #textcolor(7) # graphics
    if not registered: # from ATR2FUNC
        #textcolor(4) # graphics
        print('Unregistered version')
    else:
        print('Registered to: ', reg_name) # reg_name defined in ATR2FUNC
    #textolor(7) # graphics
    print()
    if logging_errors:
        for i in range(0, num_robots + 1):
            print('Robot error-log created: ' + robot[i].fn + '.ERR')
            robot[i].errorlog = open(robot[i].errorlog, 'a').close()  
    quit()
    
def delete_compile_report():
    if os.path.isfile(main_filename + compile_ext):
        os.remove(main_filename + compile_ext)
        
def write_compile_report():
    f = open(main_filename + compile_ext, 'w') 
    f.write(str(num_robots + 1)) 
    for i in range(0, num_robots + 1):
        f.write(str(robot[i].fn))
    f.close()
    #textcolor(15) # graphics
    print()
    print("All compiles successful!")
    print()
    shutdown()

def parse_param(s):
    global step_mode
    global game_delay
    global time_slice
    global game_limit
    global matches
    global show_source
    global no_gfx
    global report
    global report_type
    global compile_only
    global show_cnotice
    global show_arcs
    global windoze
    global debug_info
    global maxcode
    global insane_missiles
    global old_shields
    global logging_errors
    global insanity
    global num_robots
    s1 = ''
    found = False
    s = btrim(ucase(s))
    if s == '':
        return
    if s[0] == '#':
        fn = rstr(s, len(s) - 1)
        if fn == fn.split('.')[0]:  
            fn = fn + config_ext
        if not os.path.isfile(fn):
            prog_error(6, fn)
        f = open(fn, 'r')
        for line in f:
            s1 = ucase(btrim(s1))
            if s1[0] == '#':
                prog_error(7, s1)
            else:
                parse_param(s1)
        f.close()
        found = True
    elif s[0] in ['/', '-', '=']:
        s1 = rstr(s, len(s) - 1)
        if s1[0] == 'X':
            step_mode = value(rstr(s1, len(s1) - 1))
            found = True
            if step_mode == 0:
                step_mode = 1
            if (step_mode < 1) or (step_mode > 9):
                prog_error(24, rstr(s1, len(s1) - 1))
        if s1[0] == 'D':
            game_delay = value(rstr(s1, len(s1) - 1)) 
            found = True
        if s1[0] == 'T':
            time_slice = value(rstr(s1, len(s1) - 1))
            found = True
        if s1[0] == 'L':
            game_limit = value(rstr(s1, len(s1) - 1)) * 1000
            found = True
        if s1[0] == 'Q':
            sound_on = False # sound_on defined in ATR2FUNC
            found = True
        if s1[0] == 'M': 
            matches = value(rstr(s1, len(s1) - 1))
            found = True
        if s1[0] == 'S':
            show_source = False
            found = True
        if s1[0] == 'G':
            no_gfx = True
            found = True
        if s1[0] == 'R':
            report = True
            found = True
            if (len(s1) > 1):
                report_type = value(rstr(s1, len(s1) - 1))
        if s1[0] == 'C':
            compile_only = True
            found = True
        if s1[0] == '^':
            show_cnotice = False
            found = True
        if s1[0] == 'A':
            show_arcs = True
            found = True
        if s1[0] == 'W':
            windoze = False 
            found = True
        if s1[0] == '$':
            debug_info = True
            found = True
        if s1[0] == '#':
            maxcode = value(rstr(s1, len(s1) - 1)) - 1
            found = True
        if s1[0] == '!':
            insane_missiles = True
            if (len(s1) > 1):
                insanity = value(rstr(s1, len(s1) - 1))
                found = True
        if s1[0] == '@':
            old_shields = True
            found = True
        if s1[0] == 'E':
            logging_errors = True
            found = True
        if insanity < 0:
            insanity = 0
        if insanity > 15:
            insanity = 15
    elif s[0] == ';':
        found = True
    elif(num_robots < max_robots) and (s != ''):
        num_robots += 1
        create_robot(num_robots, s) 
        found = True
        if num_robots == max_robots:
            print("Maximum number of robots reached.")
    else:
        prog_error(10, '')
    if not found:
        prog_error(8, s)

def init(): 
    global step_mode
    global logging_errors
    global stats_mode
    global insane_missiles
    global insanity
    global windoze
    global no_gfx
    global timing
    global matches
    global played
    global old_shields
    global _quit
    global compile_only
    global show_arcs
    global debug_info
    global show_cnotice
    global show_source
    global report
    global kill_count
    global maxcode
    global max_code
    global num_robots
    global game_limit
    global game_cycle
    global game_delay
    global default_delay
    global time_slice
    global default_slice
    global temp_mode
    global delay_per_sec
    global sound_on
    if debugging_compiler or compile_by_line or show_code:
        print("!!! Warning !!! Compiler Debugging enabled !!!\n")
    step_mode = 0 # {stepping disabled}
    logging_errors = False
    stats_mode = 0
    insane_missiles = False
    insanity = 0
    delay_per_sec = 0 # initialized in ATR2FUNC
    windoze = True
    graphix = False # initialized in ATR2FUNC
    no_gfx = True
    sound_on = True # initialized in ATR2FUNC
    timing = True
    matches = 1
    played = 0
    old_shields = False
    _quit = False
    compile_only = False
    show_arcs = False
    debug_info = False
    show_cnotice = True
    show_source = True
    report = False
    kill_count = 0
    maxcode = max_code 
    make_tables() # in ATR2FUNC
    random.seed(time.time()) # "randomize" in original code
    num_robots = -1
    game_cycle = 0 
    game_delay = default_delay
    time_slice = default_slice
    for i in range(0, max_missiles + 1):
        missile[i].a = 0 
        missile[i].source = -1
        missile[i].x = 0
        missile[i].y = 0
        missile[i].lx = 0
        missile[i].ly = 0
        missile[i].mult = 1
    registered = False # initialized in ATR2FUNC
    reg_name = "Unregistered" # initialized in ATR2FUNC
    reg_num = 0xFFFF # initialized in ATR2FUNC
    check_registration() # in ATR2FUNC
    print()
    #textcolor(3) # graphical
    print(progname, '', version, '')
    print(cnotice1)
    print(cnotice2)
    #textcolor(7) # graphical 
    if not registered:
        #textcolor(4) # graphical
        print("Unregistered version")
    else:
        print("Registered to: ", reg_name)
    #textcolor(7) # graphical 
    print()
    # {create_robot(0,'SDUCK');}
    delete_compile_report()
    if len(sys.argv) > 1:
        for i in range(1, len(sys.argv)):
            parse_param(btrim(sys.argv[i].upper())) # uses ATR2FUNC
    else:
        prog_error(5, '')
    temp_mode = step_mode # {store initial step_mode}
    if logging_errors:
        for i in range (0, num_robots + 1):
            robot[i].errorlog = open(robot[i].fn.split('.')[0] + '.ERR', 'w')
            if os.path.isfile(robot[i].errorlog):
                os.remove(robot[i].errorlog)
            robot[i].errorlog = open(robot[i].fn.split('.')[0] + '.ERR', 'w')
            robot[i].errorlog.close()
    if compile_only:
        write_compile_report() 
    if num_robots < 1:
        prog_error(4, '')
    '''if not no_gfx: #commeting out since graphics-related
        graph_mode(True) # func on bool line 552 '''
    # {--fix ups--}
    if matches > 100000: matches = 100000
    if matches < 1: matches = 1
    if game_delay > 1000: game_delay = 1000
    if game_delay < 0: game_delay = 0 
    if time_slice > 100: time_slice = 100;
    if time_slice < 1: time_slice = 1
    if game_limit < 0: game_limit = 0
    if game_limit > 100000: game_limit = 100000
    if maxcode < 1: maxcode = 1 # {0 based, so actually 2 lines}
    if maxcode > max_code: maxcode = max_code
    # {--Just to avoid floating pointers--}
    for i in range(num_robots + 1, max_robots + 3):
        robot[i] = robot[0]
        robot[-1] = robot[0]
        robot[-2] = robot[0]
    if not graphix:
        #print("Freemem: ", memavail) # don't have to do since we have much memavail
        print()


# def draw_robot(n): GRAPHICAL

def get_from_ram(n,i,j):
    if (i < 0) or (i > (max_ram + 1) + (((max_code + 1) << 3) - 1)):
        k = 0
        robot[n].robot_error(n,4,cstr(i))
    else:
        if i <= max_ram:
            k = robot[n].ram[i]
        else:
            l = i - max_ram - 1
            k = code[l >> 2].op[l & 3]
    return k

def get_val(n,c,o):
    k = 0
    j = (robot[n].code[c].op[max_op] >> (4*o)) & 15
    i = robot[n].code[c].op[o]
    if (j & 7) == 1:
        k = get_from_ram(n,i,j)
    else:
        k = i
    if (j & 8) > 0:
        k = get_from_ram(n,k,j)
    return k

def put_val(n,c,o,v):
    k = 0
    i = 0
    j = 0
    j = (robot[n].code[c].op[max_op] >> (4 * o)) & 15
    i = robot[n].code[c].op[o]
    if (j and 7) == 1:
        if (i<0) or (i>max_ram):
            robot_error(n,4,cstr(i))
        else:
            if (j and 8) > 0:
                i = robot[n].ram[i]
                if (i < 0) or (i > max_ram):
                    robot_error(n,4,cstr(i))
                else:
                    robot[n].ram[i] = v
            else:
                robot[n].ram[i] = v
    else:
        robot_error(n,3,'')

def push(n,v):
    if (robot[n].ram[71] >= stack_base) and (robot[n].ram[71] < (stack_base + stack_size)):
        robot[n].ram[robot[n].ram[71]] = v
        robot[n].ram[71] = robot[n].ram[71] + 1
    else:
        robot_error(n,1,cstr(robot[n].ram[71]))
            
def pop(n):
    if (robot[n].ram[71] > stack_base) and (robot[n].ram[71] <= (stack_base + stack_size)):
        robot[n].ram[71] = robot[n].ram[71] - 1
        k = robot[n].ram[robot[n].ram[71]]
    else:
        robot_error(n,5,cstr(robot[n].ram[71]))
    return k

def find_label(n,l,m):
    k = -1
    if m == 3:
        robot_error(n,9,'')
    elif m == 4:
        k = l
    else:
        for i in range(plen,0,-1):
            j = code[i].op[max_op] & 15
            if (j == 2) and (code[i].op[0] == l):
                k = i
    return k

def init_mine(n,detectrange,size):
    k = -1
    for i in range(0,max_mines):
        if ((robot[n].mine[i].x < 0) or (robot[n].mine[i].x > 1000) or (robot[n].mine[i].y < 0) or (robot[n].mine[i].y > 1000) or (robot[n].mine[i]._yield <= 0)) and (k < 0):
            k = i
        if k >= 0:
            robot[n].mine[k].x = x
            robot[n].mine[k].y = y
            robot[n].mine[k].detect = detectrange
            robot[n].mine[k]._yield = size
            robot[n].mine[k].detonate = False
            click()

def count_missiles():
    k = 0
    for i in range(0,max_missiles):
        if missile[i].a > 0:
            k = k + 1
    return k

def init_missile(xx,yy,xxv,yyv,dir,s,blast,ob):
    k = -1
    click()
    for i in range(max_missiles,0,-1):
        if missile[i].a == 0:
            k = i
        if k >= 0:
            missile[k].source = s
            missile[k].x = xx
            missile[k].lx = missile.x
            missile[k].y = yy
            missile[k].ly = missile.y
            missile[k].rad = 0
            missile[k].lrad = 0
            if missile[k].ob:
                missile[k].mult = 1.25
            else:
                missile[k].mult = 1
            if missile[k].blast > 0:
                missile[k].max_rad = missile.blast
                a = 2
            else:
                if (s >= 0) and (s <= num_robots):
                    missile[k].mult = missile[k].mult * (robot[s].shotstrength)
                m = missile[k].mult
                if ob:
                    m = m + 0.25
                missile[k].mspd = missile[k].missile_spd * missile[k].mult
                if insane_missiles:
                    missile[k].mspd = 100 + (50 * insanity) * mult
                if (s >= 0) and (s <= num_robots):
                    robot[s].heat += round(20*m)
                    robot[s].shots_fired += 1
                    robot[s].match_shots += 1
                a = 1
                hd = dir
                max_rad = mis_radius
                if debug_info:
                    print('\v' + ATR2FUNC.zero_pad(game_cycle,5) + ' F ' + s + ': hd=' + '           ')
                    ### repeat until keypressed; flushkey; end; DOES NOTHING IN PYTHON     
            
def damage(n,d,physical):
    global debug_info
    if (n < 0) or (n > num_robots) or (robot[n].armor <= 0):
        sys.exit()
    if robot[n].config.shield < 3:
        robot[n].shields_up = False
        h = 0
    if (shields_up) and (not physical):
        dd = robot[n].d
    if (robot[n].old_shields) and (robot[n].config.shield >= 3):
        robot[n].d = 0
        h = 0
    else:
        if robot[n].config.shield == 3:
            robot[n].d = round(dd * 2 / 3.0)
            if robot[n].d < 1:
                robot[n].d = 1
                h = round(dd * 2 / 3.0)
            if robot[n].config.shield == 4:
                h = int(dd / 2.0)
                robot[n].d = dd - h
            if robot[n].config.shield == 5:
                robot[n].d = round(dd * 1 / 3.0)
                if robot[n].d < 1:
                    robot[n].d = 1
                h = round(dd * 1 / 3.0)
                if h < 1:
                    h = 1
    if robot[n].d < 0:
        robot[n].d = 0
    if debug_info:
        print('\r' + zero_pad(game_cycle,5) + ' D ' + n + ': ' + robot[n].armor + '-' + robot[n].d + '=' + str(robot[n].armor - robot[n].d) + '           ')
       # repeat until keypressed; flushkey; end;
    if robot[n].d > 0:
        robot[n].d = round(robot[n].d * damageadj)
    if d < 1:
        d = 1
    robot[n].armor -= robot[n].d
    robot[n].heat -= h
    robot[n].last_damage = 0
    if armor <= 0:
        armor = 0
        update_armor(n)
        heat = 500
        update_heat(n)
        armor = 0
        kill_count += 1
        deaths += 1
        update_lives(n)
    if graphix and timing:
        time_delay(10)
     # draw_robot(n) GRAPHICAL
    robot[n].heat = 0
    update_heat(n)
    init_missile(x,y,0,0,0,n,blast_circle,False)
    if overburn:
        m = 1.3
    else: m = 1
    for i in range(0,num_robots):
        if (i != n) and (robot[i].armor > 0):
            k = round(distance(x, y, robot[i].x, robot[i].y))
            if k < blast_radius:
                damage(i, round(abs(blast_radius - k) * m), False)

def scan(n):
    nn = -1
    _range = maxint
    if not (0 <= n <= num_robots):
        return
    if robot[n].scanarc < 0:
        robot[n].scanarc = 0
    robot[n].accuracy = 0
    nn = -1
    _dir = (robot[n].shift + robot[n].hd) & 255 
    if debug_info:
        print('<SCAN Arc=', robot[n].scanarc, ', Dir=', _dir, '>')
    for i in range(0, num_robots):
        if (i != n) and (robot[i].armor > 0):
            j = find_anglei(robot[n].x, robot[n].y, robot[i].x, robot[i].y)
            d = distance(robot[n].x, robot[n].y, robot[i].x, robot[i].y)
            k = round(d)
            if (k < _range) and (k <= robot[n].scanrange) and ((abs(j - _dir) <= abs(robot[n].scanarc)) or (abs(j - _dir) >= 256 - abs(robot[n].scanarc))):
                _dir = (dir + 1024) & 255 
                xx = round(sint[_dir] * d + robot[n].x)
                yy = round(-cost[_dir] * d + robot[n].y)
                r = distance(xx, yy, robot[i].x, robot[i].y)
                if debug_window:
                    print('SCAN HIT! Scan X,Y: ' + round(xx) + ',' + round(yy) + '  Robot X,Y: ' + round(robot[i].x) + ',' + round(robot[i].y) + '  Dist=' + round(r))
                    while True:
                        if keypressed:
                            break
                if (robot[n].scanarc > 0) or (r < hit_range - 2):
                    _range = k
                    robot[n].accuracy = 0
                    if robot[n].scanarc > 0:
                        j = (j + 1024) & 255 
                        _dir = (_dir + 1024) & 255
                        if (j < _dir):
                            sign = -1
                        if (j > _dir):
                            sign = 1
                        if (j > 190) and (_dir < 66):
                            _dir = _dir + 256
                            sign = -1 
                        if (_dir > 190) and (j < 66):
                            j = j + 256
                            sign = 1
                        acc = abs(j - _dir) / robot[n].scanarc * 2
                        if sign < 0:
                            robot[n].accuracy = -abs(round(acc))
                        else:
                            robot[n].accuracy = abs(round(acc))
                    nn = i
                    if debug_info:
                        print('\r' + zero_pad(game_cycle, 5) + ' S ' + robot[n].n + ': nn=' + nn + ', range=' + _range + ', acc=' + accuracy + '           ')
                        while True:
                            if keypressed:
                                break
    if 0 <= nn <= num_robots:
        robot[n].ram[5] = robot[nn].transponder
        robot[n].ram[6] = (robot[nn].hd - (robot[n].hd + robot[n].shift) + 1024) & 255 
        robot[n].ram[7] = robot[nn].spd
        robot[n].ram[13] = round(robot[nn].speed * 100)
    return _range

def com_transmit(n, chan, data):
    for i in range(0, num_robots + 1):
        if (robot[i].armor > 0) and (i != n) and (robot[i].channel == chan):
            if (robot[i].ram[10] < 0) or (robot[i].ram[10] > max_queue):
                robot[i].ram[10] = 0
            if (robot[i].ram[11] < 0) or (robot[i].ram[11] > max_queue):
                robot[i].ram[11] = 0
            robot[i].ram[robot[i].ram[11] + com_queue] = data
            robot[i].ram[11] += 1
            if (robot[i].ram[11] > max_queue):
                robot[i].ram[11] = 0
            if (robot[i].ram[11] == robot[i].ram[10]):
                robot[i].ram[10] += 1
            if (robot[i].ram[10] > max_queue):
                robot[i].ram[10] = 0
                
def com_receive(n):
    k = 0
    if (robot[n].ram[10] != robot[n].ram[11]):
        if (robot[n].ram[10] < 0) or (robot[n].ram[10] > max_queue):
            robot[n].ram[10] = 0
        if (robot[n].ram[11] < 0) or (robot[n].ram[11] > max_queue):
            robot[n].ram[11] = 0
        k = robot[n].ram[robot[n].ram[10] + com_queue]
        robot[n].ram[10] += 1
        if (robot[n].ram[10] > max_queue):
            robot[n].ram[10] = 0
    else:
        robot_error(n, 12, '')
    return k

def in_port(n,p,time_used):
    global minint
    v = 0
    if p == 1:
        v = robot[n].spd
    if p == 2:
        v = robot[n].heat
    if p == 3:
        v = robot[n].hd
    if p == 4:
        v = robot[n].shift
    if p == 5:
        v = (robot[n].shift + robot[n].hd) & 255
    if p == 6:
        v = robot[n].armor
    if p == 7:
        v = scan(n)
        time_used += 1
        if show_arcs:
            arc_count = 2
    if p == 8:
        v = robot[n].accuracy
        time_used += 1
    if p == 9:
        robot[n].nn = -1
        time_used += 3
        robot[n].k = 65535
        robot[n].nn = -1
        for i in range(0,num_robots):
            j = round(distance(x,y,robot[i].x,robot[i].y))
            if (n != i) and (j < k) and (robot[i].armor > 0):
                k = j
                nn = i
            v = k
            if nn in range(0,num_robots):
                robot[n].ram[5] = robot[robot[n].nn].transponder
    if p == 10:
        v = random.randint(0,65535) + random.randint(0,2)
    if p == 16:
        nn = -1
        if show_arcs:
            sonar_count = 2
        time_used += 40
        l = -1
        k = 65535
        random[n].nn = -1
        for i in range(0, num_robots):
            j = round(distance(x, y, robot[i].x, robot[i].y))
            if (n != i) and (j < k) and (j < max_sonar) and (robot[i].armor > 0):
                k = j
                l = i
                robot[n].nn = i
        if l >= 0:
            v = (round(find_angle(x, y, robot[l].x, robot[l].y) / math.pi*128 + 1024 + random(65) - 32) & 255)
        else:
            v = minint
        if robot[n].nn in range(0,num_robots):
            robot[n].ram[5] = robot[robot[n].nn].transponder
    if p == 17:
        v = scanarc
    if p == 18:
        if overburn:
            v = 1
        else:
            v = 0
    if p == 19:
        v = transponder
    if p == 20:
        v = shutdown
    if p == 21:
        v = channel
    if p == 22:
        v = mines
    if p == 23:
        if robot[n].config.mines >= 0:
            k = 0
            for i in range(0, max_mines):
                if (mine[i].x >= 0) and (mine[i].x <= 1000) and (mine[i].y >= 0) and (mine[i].y <= 1000) and (mine[i]._yield > 0):
                    k += 1
                    v = k
                else:
                    v = 0
    if p == 24:
        if robot[n].config.shield > 0:
            if shields_up:
                v = 1
            else:
                v = 0
        else:
            v = 0
            robot[n].shields_up = False
    else:
        robot_error(n,11,cstr(p))
    return v

def out_port(n,p,v,time_used):
    if p == 11:
        robot[n].tspd = v
    if p == 12:
        robot[n].shift = (robot[n].shift + v + 1024) & 255
    if p == 13:
        robot[n].shift = (v + 1024) & 255
    if p == 14:
        robot[n].thd = (robot[n].thd + v + 1024) & 255
    if p == 15:
        time_used += 3
        if v > 4:
            v = 4
        if v < -4:
            v = -4
        init_missile(x, y, xv, yv, (robot[n].hd + robot[n].shift + v) & 255, n, 0, robot[n].overburn)
    if p == 17:
        robot[n].scanarc = v
    if p == 18:
        if v == 0:
            robot[n].overburn = False
        else:
            robot[n].overburn = True
    if p == 19:
        robot[n].transponder = v
    if p == 20:
        robot[n].shutdown = v
    if p == 21:
        robot[n].channel = v
    if p == 22:
        if robot[n].config.mines >= 0:
            if robot[n].mines > 0:
                init_mine(n,v,robot[n].mine_blast)
                robot[n].mines -= 1
            else:
                robot_error(n, 14, '')
        else:
            robot_error(n, 13, '')
    if p == 23:
        if robot[n].config.mines >= 0:
            for i in range(0, max_mines):
                mine[i].detonate = True
        else:
             robot_error(n, 13, '')   
    if p == 24:
        if robot[n].config.shield >= 3:
            if v == 0:
                robot[n].shields_up = False
            else:
                robot[n].shields_up = True
        else:
            robot[n].shields_up = False
            robot_error(n, 15, '')
    else:
        robot_error(n, 11, cstr(p))
    if robot[n].scanarc > 64:
        robot[n].scanarc = 64
    if robot[n].scanarc < 0:
        robot[n].scanarc = 0
        
def call_int(n,int_num,time_used):
    if int_num == 0:
        damage(n,1000,True)
    if int_num == 1:
        reset_software(n)
        time_used = 10
    if int_num == 2:
        time_used = 5
        robot[n].ram[69] = round(robot[n].x)
        robot[n].ram[70] = round(robot[n].y)
    if int_num == 3:
        time_used = 2
        if robot[n].ram[65] == 0:
            robot[n].keepshift = False
        else:
            robot[n].keepshift = True
        robot[n].ram[70] = robot[n].shift & 255
    if int_num == 4:
        if robot[n].ram[65] == 0:
            robot[n].overburn = False
        else:
            robot[n].overburn = True
    if int_num == 5:
        time_used = 2
        robot[n].ram[70] = robot[n].transponder
    if int_num == 6:
        time_used = 2
        robot[n].ram[69] = game_cycle >> 16
        robot[n].ram[70] = game_cycle & 65535
    if int_num == 7:
        j = robot[n].ram[69]
        k = robot[n].ram[70]
        if j < 0:
            j = 0
        if j > 1000:
            j = 1000
        if k < 0:
            k = 0
        if k > 1000:
            k = 1000
        robot[n].ram[65] = round(find_angle(round(robot[n].x), round(robot[n].y),j,k) / math.pi * 128 + 256) & 255
        time_used = 32
    if int_num == 8:
        robot[n].ram[70] = robot[n].ram[5]
        time_used = 1
    if int_num == 9:
        robot[n].ram[69] = robot[n].ram[6]
        robot[n].ram[70] = robot[n].ram[7]
        time_used = 2
    if int_num == 10:
        k = 0
        for i in range(0,num_robots):
            if robot[i].armor > 0:
                k += 1
        robot[n].ram[68] = k
        robot[n].ram[69] = played
        robot[n].ram[70] = matches
        time_used = 4
    if int_num == 11:
        robot[n].ram[68] = round(robot[n].speed * 100)
        robot[n].ram[69] = robot[n].last_damage
        robot[n].ram[70] = robot[n].last_hit
        time_used = 5
    if int_num == 12:
        robot[n].ram[70] = robot[n].ram[8]
        time_used = 1
    if int_num == 13:
        robot[n].ram[8] = 0
        time_used = 1
    if int_num == 14:
        com_transmit(n, Robot[n].channel, robot[n].ram[65])
        time_used = 1
    if int_num == 15:
        if robot[n].ram[10] != robot[n].ram[11]:
            robot[n].ram[70] = com_receive(n)
        else:
            robot_error(n,12,'')
        time_used = 1
    if int_num == 16:
        if (ram[11] >= robot[n].ram[10]):
            robot[n].ram[70] = robot[n].ram[11]-ram[10]
        else:
            robot[n].ram[70] = max_queue + 1 - robot[n].ram[10] + robot[n].ram[11]
        time_used = 1
    if int_num == 17:
        robot[n].ram[10] = 0
        robot[n].ram[11] = 0
        time_used = 1
    if int_num == 18:
        robot[n].ram[68] = robot[n].kills
        robot[n].ram[69] = robot[n].kills - robot[n].startkills
        robot[n].ram[70] = robot[n].deaths
        time_used = 3
    if int_num == 19:
        robot[n].ram[9] = 0
        robot[n].meters = 0
    else:
        robot_error(n,10,cstr(int_num))

def jump(n, o, inc_ip):
    loc = find_label(n, get_val(n, robot[n].ip, 0), robot[n].code[robot[n].ip].op[max_op] >> (o * 4))
    if (loc >= 0) and (loc <= robot[n].plen):
        inc_ip = False
        robot[n].ip = loc
    else:
        robot_error(n, 2, cstr(loc))

# def update_debug_bars():
# def update_debug_system():
# def update_debug_registers():
# def update_debug_flags():
# def update_debug_memory():
# def update_debug_code():
# def update_debug_window():

def update_debug_window(): # lines 2404-2428
    if graphix and (step_mode > 0):
        update_debug_bars # {armour + heat}
        update_debug_system # {system variables}
        update_debug_registers # {registers}
        update_debug_flags # {flag register}
        update_debug_memory # {memory}
        update_debug_code # {code}
        
# def init_debug_window():
# def close_debug_window():

def gameover():
    global game_cycle
    global game_limit
    global num_robots
    if (game_cycle >= game_limit) and (game_limit > 0):
        return True
    if game_cycle & 31 == 0:
        k = 0
        for n in range(num_robots + 1):
            if robot[n].armor > 0:
                k += 1
            if k <= 0:
                return True
            else:
                return False
    else:
        return False
    
def toggle_graphix():
    graph_mode(not graphix)
    if not graphix:
        #textcolor(7) # graphics-related
        print('Match ' + played + '/' + matches + ', Battle in progress...')
        print()
    else:
        setscreen
        
def invalid_microcode(n, ip):
    invalid = False
    for i in range(3):
        k = (robot[n].code[ip].op[max_op] >> (i << 2)) & 7 
        if not (k in [0, 1, 2, 4]):
            invalid = True
    return invalid

def process_keypress(c):
    global timing
    global show_arcs
    global debug_info
    global windoze
    global bout_over
    global _quit
    global step_loop
    if c == 'C':
        calibrate_timing
    elif c == 'T':
        timing = not timing
    elif c == 'A':
        show_arcs = not show_arcs
    elif (c == 'S') or (c == 'Q'):
        if sound_on:
            chirp
        sound_on = not sound_on
        if sound_on:
            chirp
    elif c == '$':
        debug_info = not debug_info
    elif c == 'W':
        windoze = not windoze
    elif c == '\b':
        bout_over = True
    elif c == '\e':
        _quit = True
        step_loop = False  

def execute_instruction(n):
    global step_count
    global step_loop
    global executed
    
    # update system variables
    robot[n].ram[0] = robot[n].tspd
    robot[n].ram[1] = robot[n].thd
    robot[n].ram[2] = robot[n].shift
    robot[n].ram[3] = robot[n].accuracy
    
    time_used = 1
    inc_ip = True
    loc = 0
    if (robot[n].ip > robot[n].plen) or \
       (robot[n].ip < 0):
        robot[n].ip = 0
    if invalid_microcode(n, robot[n].ip):
        time_used = 1 
        robot_error(n, 16, hex(robot[n].code[robot[n].ip].op[max_op]))
        
    # the following is graphics-related
    '''elif graphix and (step_mode>0) and (n=0) then  {if stepping enabled...}
        begin
        inc(step_count);
        update_cycle_window;
        update_debug_window;
        if (step_count mod step_mode)=0 then step_loop:=true else step_loop:=false;
        while step_loop and (not(quit or gameover or bout_over)) do
        if keypressed then with robot[0]^ do
        begin
        c:=upcase(readkey);
        case c of
        'X':begin
             temp_mode:=step_mode;
             step_mode:=0;
             step_loop:=false;
             close_debug_window;
            end;
        ' ':begin step_count:=0; step_loop:=false; end;
        '1'..'9':begin step_mode:=value(c); step_count:=0; step_loop:=false; end;
        '0':begin step_mode:=10; step_count:=0; step_loop:=false; end;
        '-','_':if mem_watch>0 then
                 begin
                  setcolor(0);
                  for i:=0 to 9 do
                   outtextxy(035,212+(10*i),decimal((mem_watch+i),4) + ' :');
                  dec(mem_watch);
                  update_debug_memory;
                 end;
        '+','=':if mem_watch<1014 then
                 begin
                  setcolor(0);
                  for i:=0 to 9 do
                   outtextxy(035,212+(10*i),decimal((mem_watch+i),4) + ' :');
                  inc(mem_watch);
                  update_debug_memory;
                 end;
        '[','{':if mem_watch>0 then
                 begin
                  setcolor(0);
                  for i:=0 to 9 do
                   outtextxy(035,212+(10*i),decimal((mem_watch+i),4) + ' :');
                  dec(mem_watch,10);
                  if mem_watch<0 then mem_watch:=0;
                  update_debug_memory;
                 end;
        ']','}':if mem_watch<1014 then
                 begin
                  setcolor(0);
                  for i:=0 to 9 do
                   outtextxy(035,212+(10*i),decimal((mem_watch+i),4) + ' :');
                  inc(mem_watch,10);
                  if mem_watch>1014 then mem_watch:=1014;
                  update_debug_memory;
                 end;
        'G':begin toggle_graphix; temp_mode:=step_mode; step_mode:=0; step_loop:=false; end;
        else process_keypress(c);
        end;
        end;
        end;'''
    if ((robot[n].code[robot[n].ip].op[max_op] & 7) in [0, 1]):
        time_used = 0
    else:
        if get_val(n, robot[n].ip, 0) == 0: # NOP
            executed += 1
        elif get_val(n, robot[n].ip, 0) == 1: # ADD
            put_val(n, robot[n].ip, 1, get_val(n, robot[n].ip, 1) + get_val(n, robot[n].ip, 2))
            executed += 1
        elif get_val(n, robot[n].ip, 0) == 2: # SUB
            put_val(n, robot[n].ip, 1, get_val(n, robot[n].ip, 1) - get_val(n, robot[n].ip, 2))
            executed += 1
        elif get_val(n, robot[n].ip, 0) == 3: # OR
            put_val(n, robot[n].ip, 1, get_val(n, robot[n].ip, 1) | get_val(n, robot[n].ip, 2))
            executed += 1
        elif get_val(n, robot[n].ip, 0) == 4: # AND
            put_val(n, robot[n].ip, 1, get_val(n, robot[n].ip, 1) & get_val(n, robot[n].ip, 2))
            executed += 1
        elif get_val(n, robot[n].ip, 0) == 5: # XOR
            put_val(n, robot[n].ip, 1, get_val(n, robot[n].ip, 1) ^ get_val(n, robot[n].ip, 2))
            executed += 1
        elif get_val(n, robot[n].ip, 0) == 6: # NOT
            put_val(n, robot[n].ip, 1, not(get_val(n, robot[n].ip, 1)))
            executed += 1
        elif get_val(n, robot[n].ip, 0) == 7: # MPY
            put_val(n, robot[n].ip, 1, get_val(n, robot[n].ip, 1) * get_val(n, robot[n].ip, 2))
            time_used = 10
            executed += 1
        elif get_val(n, robot[n].ip, 0) == 8: # DIV
            j = get_val(n, robot[n].ip, 2)
            if j != 0:
                put_val(n, robot[n].ip, 1, get_val(n, robot[n].ip, 1) // j)
            time_used = 10
            executed += 1
        elif get_val(n, robot[n].ip, 0) == 9: # MOD
            j = get_val(n, robot[n].ip, 2)
            if j != 0:
                put_val(n, robot[n].ip, 1, get_val(n, robot[n].ip, 1) % j)
            else:
                robot_error(n, 8, '')
            time_used = 10
            executed += 1
        elif get_val(n, robot[n].ip, 0) == 10: # RET
            robot[n].ip = pop(n)
            if (robot[n].ip < 0) or (robot[n].ip > robot[n].plen):
                robot_error(n, 7, cstr(robot[n].ip))
            executed += 1
        elif get_val(n, robot[n].ip, 0) == 11: # GSB
            loc = find_label(n, get_val(n, robot[n].ip, 1), code[robot[n].ip].op[max_op] >> (1 * 4)) # local variable
            if loc >= 0:
                push(n, robot[n].ip)
                inc_ip = False # local variable
                robot[n].ip = loc
            else:
                robot_error(n, 2, cstr(get_val(n, robot[n].ip, 1)))
            executed += 1
        elif get_val(n, robot[n].ip, 0) == 12: # JMP
            jump(n, 1, inc_ip)
            executed += 1
        elif get_val(n, robot[n].ip, 0) == 13: # JLS, JB
            if robot[n].ram[64] & 2 > 0:
                jump(n, 1, inc_ip)
            time_used = 0
            executed += 1
        elif get_val(n, robot[n].ip, 0) == 14: # JGR, JA
            if robot[n].ram[64] & 4 > 0:
                jump(n, 1, inc_ip)
            time_used = 0
            executed += 1
        elif get_val(n, robot[n].ip, 0) == 15: # JNE
            if robot[n].ram[64] & 1 == 0:
                jump(n, 1, inc_ip)
            time_used = 0
            executed += 1
        elif get_val(n, robot[n].ip, 0) == 16: # JEQ, JE
            if robot[n].ram[64] & 1 > 0:
                jump(n, 1, inc_ip)
            time_used = 0
            executed += 1
        elif get_val(n, robot[n].ip, 0) == 17: # SWAP, XCHG
            robot[n].ram[4] = get_val(n, robot[n].ip, 1)
            put_val(n, robot[n].ip, 1, get_val(n, robot[n].ip, 2))
            put_val(n, robot[n].ip, 2, robot[n].ram[4])
            time_used = 3
            executed += 1
        elif get_val(n, robot[n].ip, 0) == 18: # DO
            robot[n].ram[67] = get_val(n, robot[n].ip, 1)
            executed += 1
        elif get_val(n, robot[n].ip, 0) == 19: # LOOP
            robot[n].ram[67] -= 1
            if robot[n].ram[67] > 0:
                jump(n, 1, inc_ip)
            executed += 1
        elif get_val(n, robot[n].ip, 0) == 20: # CMP
            k = get_val(n, robot[n].ip, 1) - get_val(n, robot[n].ip, 2)
            robot[n].ram[64] = robot[n].ram[64] & 0xFFF0
            if k == 0:
                robot[n].ram[64] = robot[n].ram[64] | 1
            if k < 0:
                robot[n].ram[64] = robot[n].ram[64] | 2
            if k > 0:
                robot[n].ram[64] = robot[n].ram[64] | 4
            if (get_val(n, robot[n].ip, 2) == 0) and (k == 0):
                robot[n].ram[64] = robot[n].ram[64] | 8
            executed += 1
        elif get_val(n, robot[n].ip, 0) == 21: # TEST
            k = get_val(n, robot[n].ip, 1) & get_val(n, robot[n].ip, 2)
            robot[n].ram[64] = robot[n].ram[64] & 0xFFF0
            if k == get_val(n, robot[n].ip, 2):
                robot[n].ram[64] = robot[n].ram[64] | 1
            if k == 0:
                robot[n].ram[64] = robot[n].ram[64] | 8
            executed += 1
        elif get_val(n, robot[n].ip, 0) == 22: # MOV, SET
            put_val(n, robot[n].ip, 1, get_val(n, robot[n].ip, 2))
            executed += 1
        elif get_val(n, robot[n].ip, 0) == 23: # LOC
            put_val(n, robot[n].ip, 1, robot[n].code[robot[n].ip].op[2])
            time_used = 2
            executed += 1
        elif get_val(n, robot[n].ip, 0) == 24: # GET
            k = get_val(n, robot[n].ip, 2)
            if (k >= 0) and (k <= max_ram):
                put_val(n, robot[n].ip, 1, robot[n].ram[k])
            elif (k > max_ram) and (k <= (max_ram + 1) + (((max_code + 1) << 3) - 1)):
                j = k - max_ram - 1
                put_val(n, robot[n].ip, 1, robot[n].code[j >> 2].op[j & 3])
            else:
                robot_error(n, 4, cstr(k))
            time_used = 2
            executed += 1
        elif get_val(n, robot[n].ip, 0) == 25: # PUT
            k = get_val(n, robot[n].ip, 2)
            if (k >= 0) and (k <= max_ram):
                robot[n].ram[k] = get_val(n, robot[n].ip, 1)
            else:
                robot_error(n, 4, cstr(k))
            time_used = 2
            executed += 1
        elif get_val(n, robot[n].ip, 0) == 26: # INT
            call_int(n, get_val(n, robot[n].ip, 1), time_used)
            executed += 1
        elif get_val(n, robot[n].ip, 0) == 27: # IPO, IN
            time_used = 4
            put_val(n, robot[n].ip, 2, in_port(n, get_val(n, robot[n].ip, 1), time_used))
            executed += 1
        elif get_val(n, robot[n].ip, 0) == 28: # OPO, OUT
            time_used = 4
            out_port(n, get_val(n, robot[n].ip, 1), get_val(n, robot[n].ip, 2), time_used)
            executed += 1
        elif get_val(n, robot[n].ip, 0) == 29: # DEL, DELAY
            time_used = get_val(n, robot[n].ip, 1)
            executed += 1
        elif get_val(n, robot[n].ip, 0) == 30: # PUSH
            push(n, get_val(n, robot[n].ip, 1))
            executed += 1
        elif get_val(n, robot[n].ip, 0) == 31: # POP
            put_val(n, robot[n].ip, 1, pop(n))
            executed += 1
        elif get_val(n, robot[n].ip, 0) == 32: # ERR
            robot_error(n, get_val(n, robot[n].ip, 1), '')
            time_used = 0
            executed += 1
        elif get_val(n, robot[n].ip, 0) == 33: # INC
            put_val(n, robot[n].ip, 1, get_val(n, robot[n].ip, 1) + 1)
            executed += 1
        elif get_val(n, robot[n].ip, 0) == 34: # DEC
            put_val(n, robot[n].ip, 1, get_val(n, robot[n].ip, 1) - 1)
            executed += 1
        elif get_val(n, robot[n].ip, 0) == 35: # SHL
            put_val(n, robot[n].ip, 1, get_val(n, robot[n].ip, 1) << get_val(n, robot[n].ip, 2))
            executed += 1
        elif get_val(n, robot[n].ip, 0) == 36: # SHR
            put_val(n, robot[n].ip, 1, get_val(n, robot[n].ip, 1) >> get_val(n, robot[n].ip, 2))
            executed += 1
        elif get_val(n, robot[n].ip, 0) == 37: # ROL
            put_val(n, robot[n].ip, 1, rol(get_val(n, robot[n].ip, 1), get_val(n, robot[n].ip, 2)))
            executed += 1
        elif get_val(n, robot[n].ip, 0) == 38: # ROR
            put_val(n, robot[n].ip, 1, ror(get_val(n, robot[n].ip, 1), get_val(n, robot[n].ip, 2)))
            executed += 1
        elif get_val(n, robot[n].ip, 0) == 39: # JZ
            time_used = 0
            if robot[n].ram[64] & 8 > 0:
                jump(n, 1, inc_ip)
            executed += 1
        elif get_val(n, robot[n].ip, 0) == 40: # JNZ
            time_used = 0
            if robot[n].ram[64] & 8 == 0:
                jump(n, 1, inc_ip)
            executed += 1
        elif get_val(n, robot[n].ip, 0) == 41: # JAE, JGE
            if (robot[n].ram[64] & 1 > 0) or (robot[n].ram[64] & 4 > 0):
                jump(n, 1, inc_ip)
            time_used = 0
            executed += 1
        elif get_val(n, robot[n].ip, 0) == 42: # JBE, JLE
            if (robot[n].ram[64] & 1 > 0) or (robot[n].ram[64] & 2 > 0):
                jump(n, 1, inc_ip)
            time_used = 0
            executed += 1
        elif get_val(n, robot[n].ip, 0) == 43: # SA
            put_val(n, robot[n].ip, 1, sal(get_val(n, robot[n].ip, 1), get_val(n, robot[n].ip, 2)))
            executed += 1
        elif get_val(n, robot[n].ip, 0) == 44: # SAR
            put_val(n, robot[n].ip, 1, sar(get_val(n, robot[n].ip, 1), get_val(n, robot[n].ip, 2)))
            executed += 1
        elif get_val(n, robot[n].ip, 0) == 45: # NEG
            put_val(n, robot[n].ip, 1, 0 - get_val(n, robot[n].ip, 1))
            executed += 1
        elif get_val(n, robot[n].ip, 0) == 46: # JTL
            loc = get_val(n, robot[n].ip, 1)
            if (loc >= 0) and (loc <= robot[n].plen):
                inc_ip = False
                robot[n].ip = loc
            else:
                robot_error(n, 2, cstr(loc))
        else:
            robot_error(n, 6, '')
    robot[n].delay_left += time_used
    if inc_ip:
        robot[n].ip += 1
    if graphix and (n == 0) and (step_mode > 0):
        update_debug_window()

def do_robot(n):
    global executed
    if (n < 0) or (n > num_robots):
        return
    if robot[n].armor <= 0:
        return

    # Time slice
    robot[n].time_left = time_slice
    if (robot[n].time_left > robot[n].robot_time_limit) and \
       (robot[n].robot_time_limit > 0):
        robot[n].time_left = robot[n].robot_time_limit
    if (robot[n].time_left > robot[n].max_time) and \
       (robot[n].max_time > 0):
        robot[n].time_left = robot[n].max_time
    executed = 0

    # Execute timeslice
    while (robot[n].time_left > 0) and (not robot[n].cooling) and (executed < 20 + time_slice) and (robot[n].armor > 0):
        if robot[n].delay_left < 0:
            robot[n].delay_left = 0
        if (robot[n].delay_left > 0):
            robot[n].delay_left -= 1
            robot[n].time_left -= 1
        if (robot[n].time_left >= 0) and (robot[n].delay_left == 0):
            execute_instruction(n)
        if robot[n].heat >= robot[n].shutdown:
            robot[n].cooling = True
            robot[n].shields_up = False
        if robot[n].heat >= 500:
            damage(n, 1000, True)

    # Fix up variables
    robot[n].thd = (robot[n].thd + 1024) & 255
    robot[n].hd = (robot[n].hd + 1024) & 255
    robot[n].shift = (robot[n].shift + 1024) & 255
    if robot[n].tspd < -75:
        robot[n].tspd = -75
    if robot[n].tspd > 100:
        robot[n].tspd = 100
    if robot[n].spd < -75:
        robot[n].spd = -75
    if robot[n].spd > 100:
        robot[n].spd = 100
    if robot[n].heat < 0:
        robot[n].heat = 0
    if robot[n].last_damage < maxint:
        robot[n].last_damage += 1
    if robot[n].last_hit < maxint:
        robot[n].last_hit += 1 
    if robot[n].shields_up and (game_cycle & 3 == 0):
        robot[n].heat += 1
    if not robot[n].shields_up:
        if robot[n].heat > 0:
            if robot[n].config.heatsinks == 5:
                if game_cycle & 1 == 0:
                    robot[n].heat -= 1
            elif robot[n].config.heatsinks == 4:
                if game_cycle % 3 == 0:
                    robot[n].heat -= 1
            elif robot[n].config.heatsinks == 3:
                if game_cycle & 3 == 0:
                    robot[n].heat -= 1
            elif robot[n].config.heatsinks == 2:
                if game_cycle & 7 == 0:
                    robot[n].heat -= 1
            elif game_cycle & 3 == 0:
                robot[n].heat += 1
            if robot[n].overburn and (game_cycle % 3 == 0):
                robot[n].heat += 1
            if (robot[n].heat > 0):
                robot[n].heat -= 1
            if (robot[n].heat > 0) and (game_cycle and 7 == 0) and (abs(robot[n].tspd) <= 25):
                robot[n].heat -= 1
            if (robot[n].heat <= robot[n].shutdown - 50) or (robot[n].heat <= 0):
                robot[n].cooling = False
    if robot[n].cooling:
        robot[n].tspd = 0
    heat_mult = 1
    if 80 <= robot[n].heat <= 99:
        heat_mult = 0.98
    elif 100 <= robot[n].heat <= 149:
        heat_mult = 0.95
    elif 150 <= robot[n].heat <= 199:
        heat_mult = 0.85
    elif 200 <= robot[n].heat <= 249:
        heat_mult = 0.75
    elif 250 <= robot[n].heat <= maxint:
        heat_mult = 0.50
    if robot[n].overburn:
        heat_mult = heat_mult * 1.30
    if (robot[n].heat >= 475) and (game_cycle & 3 == 0):
        damage(n, 1, True)
    elif (robot[n].heat >= 450) and (game_cycle & 7 == 0):
        damage(n, 1, True)
    elif (robot[n].heat >= 400) and (game_cycle & 15 == 0):
        damage(n, 1, True)
    elif (robot[n].heat >= 350) and (game_cycle & 31 == 0):
        damage(n, 1, True)
    elif (robot[n].heat >= 300) and (game_cycle & 63 == 0):
        damage(n, 1, True)
    if (abs(robot[n].spd - robot[n].tspd) <= acceleration):
        robot[n].spd = robot[n].tspd
    else:
        if robot[n].tspd > robot[n].spd:
            robot[n].spd += acceleration
        else:
            robot[n].spd -= acceleration
    tthd = robot[n].hd + robot[n].shift
    if (abs(robot[n].hd - robot[n].thd) <= turn_rate) or (abs(robot[n].hd - robot[n].thd) >= 256 - turn_rate):
        robot[n].hd = robot[n].thd
    elif robot[n].hd != robot[n].thd:
        k = 0
        if ((robot[n].thd > robot[n].hd) and (abs(robot[n].hd - robot[n].thd) <= 128)) or ((robot[n].thd < robot[n].hd) and (abs(robot[n].hd - robot[n].thd) >= 128)):
            k = 1
        if k == 1:
            robot[n].hd = (robot[n].hd + turn_rate) & 255
        else:
            robot[n].hd = (robot[n].hd + 256 - turn_rate) & 255
    robot[n].hd = robot[n].hd & 255
    if robot[n].keepshift:
        robot[n].shift = (tthd - robot[n].hd + 1024) & 255
    robot[n].speed = robot[n].spd / 100 * (max_vel * heat_mult * robot[n].speedadj)
    robot[n].xv = sint[robot[n].hd] * robot[n].speed
    robot[n].yv = -cost[robot[n].hd] * robot[n].speed
    if (robot[n].hd == 0) or (robot[n].hd == 128):
        robot[n].xv = 0
    if (robot[n].hd == 64) or (robot[n].hd == 192):
        robot[n].yv = 0
    if robot[n].xv != 0:
        ttx = robot[n].x + robot[n].xv
    else:
        ttx = robot[n].x
    if robot[n].yv != 0:
        tty = robot[n].y + robot[n].yv
    else:
        tty = robot[n].y
    if (ttx < 0) or (tty < 0) or (ttx > 1000) or (tty > 1000):
        robot[n].ram[8] += 1
        robot[n].tspd = 0
        if abs(robot[n].speed) >= max_vel / 2:
            damage(n, 1, True)
        robot[n].spd = 0
    for i in range (0, num_robots + 1):
        if (i != n) and (robot[i].armor > 0) and (distance(ttx, tty, robot[i].x, robot[i].y) < crash_range):
            robot[n].tspd = 0
            robot[n].spd = 0
            ttx = robot[n].x
            tty = robot[n].y
            robot[i].tspd = 0
            robot[i].spd = 0
            robot[n].ram[8] += 1
            robot[i].ram[8] += 1
            if abs(robot[n].speed) >= max_vel / 2:
                damage(n, 1, True)
                damage(i, 1, True)
    if ttx < 0:
        ttx = 0
    if tty < 0:
        tty = 0
    if ttx > 1000:
        ttx = 1000
    if tty > 0:
        tty = 1000
    robot[n].meters = robot[n].meters + distance(robot[n].x, robot[n].y, ttx, tty)
    if robot[n].meters >= maxint:
        robot[n].meters = robot[n].meters - maxint
    robot[n].ram[9] = int(robot[n].meters)
    robot[n].x = ttx
    robot[n].y = tty
    if robot[n].armor < 0:
        robot[n].armor = 0
    if robot[n].heat < 0:
        robot[n].heat = 0
    if graphix:
        if robot[n].armor != robot[n].larmor:
            update_armor(n)
        if robot[n].heat // 5 != robot[n].lheat // 5:
            update_heat(n)
        draw_robot(n)
    robot[n].lheat = robot[n].heat
    robot[n].larmor = robot[n].armor
    robot[n].cycles_lived += 1

def do_mine(n, m):
    global kill_count
    if ((robot[n].mine[m].x >= 0) and (robot[n].mine[m].x <= 1000) and (robot[n].mine[m].y >= 0) and (robot[n].mine[m].y <= 1000) and (robot[n].mine[m]._yield > 0)):
        for i in range(0, num_robots + 1):
            if (robot[i].armor > 0) and (i != n):
                d = distance(robot[n].mine[m].x, robot[n].mine[m].y, robot[i].x, robot[i].y)
                if (d <= robot[n].mine[m].detect):
                    robot[n].mine[m].detonate = True
        if (robot[n].mine[m].detonate):
            init_missile(robot[n].mine[m].x, robot[n].mine[m].y, 0, 0, 0, n, mine_circle, False)
            kill_count = 0
            if (robot[n].armor > 0):
                source_alive = True
            else:
                source_alive = False
            for i in range(0, num_robots + 1):
                if (robot[i].armor > 0):
                    k = round(distance(robot[n].mine[m].x, robot[n].mine[m].y, robot[i].x, robot[i].y))
                    if k < robot[n].mine[m]._yield:
                        damage(i, round(abs(_yield - k)), False)
                        if (0 <= n <= num_robots) and (i != n):
                            robot[n].damage_total += round(abs(_yield - k))
            if (kill_count > 0) and (source_alive) and (robot[n].armor <= 0):
                kill_count -= 1
            if kill_count > 0:
                robot[n].kills += kill_count
                update_lives(n)
            if graphix:
                pass
                #putpixel(round(x*screen_scale)+screen_x,round(y*screen_scale)+screen_y,0); # graphics
            robot[n].mine[m]._yield = 0
            robot[n].mine[m].x = -1
            robot[n].mine[m].y = -1
        else:
            if graphix and (game_cycle & 1 == 0):
                '''main_viewport;
                setcolor(robot_color(n));
                line(round(x*screen_scale)+screen_x,round(y*screen_scale)+screen_y-1,
                round(x*screen_scale)+screen_x,round(y*screen_scale)+screen_y+1);
                line(round(x*screen_scale)+screen_x+1,round(y*screen_scale)+screen_y,
                round(x*screen_scale)+screen_x-1,round(y*screen_scale)+screen_y);'''

def do_missile(n):
    global kill_count
    missile[n]
    if a == 0:
        pass
    else:
        if a ==1:
            if (x<-20) | (x>1020) | (y<-20) | (y>1020):
                a = 0
                
                llx = lx
                lly = ly
                lx = x
                ly = y
                
                if a > 0:
                    hd = (hd+256) and 255
                    xv = sint[hd] * mspd
                    yv = -cost[hd]*mspd
                    x = x+xv
                    y = y +yv
                                        
                #look for hit on a robot
                k =1
                l = mixint
                for i in len(num_robots):
                    if(i.armor>0) and (i !=source):
                        d = distance(lx,ly,robot[i].x,robot[i].y)
                        if (d<=mspd) and (r<hit_range) and (round(d)<=1):
                            k= i
                            l = round(d)
                            dd = round(r)
                            tx = xx
                            ty = y
                if k >= 0:
                    x = tx
                    y = ty
                    a = 2
                    rad = 0
                    lrad = 0
                    if source in range(0,num_robots):
                        robot[source].last_hit = 0
                        (robot[source].hits) + 1
                    for i in range(0,num_robots):
                        dd = round(distance(x,y,robot[i].x,robot[i].y))
                        if dd <=hit_range:
                            dam = round(abs(hit_range-dd)*mult)
                            if dam <= 0:
                                dam = 1
                                kill_count = 0
                            if robot[source].armor>0:
                                source_alive = True
                            else:
                                source_alive = False
                                damage(i,dam,False)
                            if source in range(0,num_robots) and (i!= source):
                                (robot[source].damage_tota,dam)+1
                            if kill_count > 0 and source_alive and robot[source].armor <=0:
                                kill_count -=1
                            if kill_count > 0:
                                robot[source].kills +=1
                                kill_count +=1
                                update_lives(source)
    #draw missile

def victor_string(k, n):
    s = ''
    if k == 1:
        s = 'Robot #' + cstr(n + 1) + ' (' + robot[n].fn + ') wins!'
    if k == 0:
        s = 'Simultaneous destruction, match is a tie.'
    if k > 1:
        s = 'No clear victor, match is a tie.'
    return s

def show_statistics():
    i = 0
    j = 0
    k = 0
    n = 0
    sx = 0
    sy = 0
    
    sx = 24
    sy = 93 - num_robots * 3
        
    # viewport(0,0,639,479)
    # box(sx+0,sy,sx+591,sy+102+num_robots*12)
    # hole(sx + 4, sy + 4, sx + 587, sy + 98 + num_robots * 12)
    # setfillpattern(gray50,1)
    # bar(sx+5,sy+5,sx+586,sy+97+num_robots*12)
    # setcolor(15)
    
    # outtextxy(sx+16,sy+20, 'Robot        Scored wins Matches Armor kills death shots')
    
    # outtextxy(sx+16,sy+30)
    
    n = -1
    k =0
    
    for i in range(num_robots + 1):
        armor = robot[i].armor
        if robot[i].armor > 0 | robot[i].armor == robot[i].won:
            k += 1
        for i in range(num_robots + 1):
            robot[i].armor = robot[i].armor
            # setcolor(robot_color(i))
            if k == 1 and n == i:
                j = 1
            else:
                j = 0
                
                
                '''
                  outtextxy(sx+016,sy+042+i*12,addfront(cstr(i+1),2)+' - '+addrear(fn,15)+cstr(j)
               +addfront(cstr(wins),8)+addfront(cstr(trials),8)
               +addfront(cstr(armor)+'%',9)+addfront(cstr(kills),7)
               +addfront(cstr(deaths),8)+addfront(cstr(match_shots),9));
                '''
            # outtextxy(sx+16,sy+42+i*12,addfront(str(i+1),2) +'- '+ addrear(fn,15) + str(j))
        # setcolor(15)
        
        # outtextxy(sx+16,sy+64,num_robots*12,victor_string(k,n))
        
    if windoze:
        pass
            # outtextxy(sx+16,sy+76+num_robots*12, 'Press any key to continue...')
            # flushkey
            # readkey
        
        # textcolor(15)
    print(chr(13) + ' ' + chr(13))
    print('\n Match', played, '/', matches, 's')        
    print('Robot            Scored   Wins  Matches  Armor  Kills  Deaths    Shots')
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    n = -1
    k = 0
    for i in range(num_robots + 1):
        if robot[i].armor > 0 or robot[i].won:
            k += 1
            n = i
    for i in range(num_robots + 1):
    # textcolor(robot_color[i])
        if k == 1 and n == i:
            j = 1
        else:
            j = 0                
            print(addfront(cstr(i + 1), 2) + ' - ' + \
                  addrear(robot[i].fn, 15)+cstr(j) + \
                  addfront(cstr(robot[i].wins), 8) + \
                  addfront(cstr(robot[i].trials), 8) + \
                  addfront(cstr(robot[i].armor) + '%', 9) + \
                  addfront(cstr(robot[i].kills), 7) + \
                  addfront(cstr(robot[i].deaths), 8) + \
                  addfront(cstr(robot[i].match_shots), 9))
    # textcolor(15)
    # print('\n')
    print(victor_string(k,n))
    print('\n')

def score_robots():
    k = 0
    n = -1
    for i in range(0, num_robots + 1):
        robot[i].trials += 1
        if robot[i].armor > 0:
            k += 1
            n = i
    if (k == 1) and (n >= 0):
        robot[n].wins += 1
        robot[n].won = True
        
def init_bout():
    global game_cycle
    game_cycle = 0
    for i in range(max_missiles):
        missile[i].a = 0
        missile[i].source = -1
        missile[i].x = 0
        missile[i].y = 0
        missile[i].lx = 0
        missile[i].ly = 0
        missile[i].mult = 1
    for i in range(num_robots + 1):
        robot[i].mem_watch = 128
        reset_hardware(i)
        reset_software(i)
    if graphix:
        setscreen
    if graphix and (step_mode > 0):
        init_debug_window
    if not graphix:
        pass
        # textcolor(7)

def bout():
    global game_cycle
    global game_delay
    global played
    global step_loop
    global step_mode
    global _quit
    global graphix
    if _quit:
        sys.exit()
    played += 1
    init_bout()
    bout_over = False
    if step_mode == 0:
        step_loop = False
    else:
        step_loop = True
    step_count = -1
    if graphix and (step_mode > 0):
        for i in range(num_robots + 1):
            draw_robot(i)
    while not _quit and not gameover() and not bout_over:
        game_cycle += 1
        for i in range(num_robots + 1):
            if robot[i].armor > 0:
                do_robot(i)
        for i in range(max_missiles):
            if missile[i].a > 0:
                do_missile(i)
        for i in range(num_robots + 1):
            for k in range(max_mines):
                if robot[i].mine[k]._yield > 0:
                    do_mine(i,k)
                    
        if graphix and timing:
            time_delay(game_delay)

        if keypressed:
            c = str(pygame.key.get_pressed()).upper()
        else:
            c = chr(255)

        if c == 'X':
            if not robot[0].is_locked:
                if not graphix:
                    toggle_graphix()
                if robot[0].armor > 0:
                    if temp_mode > 0:
                        step_mode = temp_mode
                    else:
                        step_mode = 1
                    step_count += 1
                    init_debug_window()
        if c == '+' or c == '=':
            if game_delay < 100:
                if game_delay in range(0,5):
                    game_delay = 5
                elif game_delay in range(5,10):
                    game_delay = 10
                elif game_delay in range(10,15):
                    game_delay = 15
                elif game_delay in range(15,20):
                    game_delay = 30
                elif game_delay in range(20,30):
                    game_delay = 40
                elif game_delay in range(30,40):
                    game_delay = 50
                elif game_delay in range(50,60):
                    game_delay = 60
                elif game_delay in range(60,75):
                    game_delay = 75
                else:
                    game_delay = 100
        if c == '-' or c == '_':
            if game_delay > 0:
                if game_delay in range(0,6):
                    game_delay = 0
                elif game_delay in range(6,11):
                    game_delay = 5
                elif game_delay in range(11,16):
                    game_delay = 10
                elif game_delay in range(16,21):
                    game_delay = 15
                elif game_delay in range(21,31):
                    game_delay = 20
                elif game_delay in range(31,41):
                    game_delay = 30
                elif game_delay in range(41,51):
                    game_delay = 40
                elif game_delay in range(51,61):
                    game_delay = 50
                elif game_delay in range(61,75):
                    game_delay = 60
                else:
                    game_delay = 75
        if c == 'G':
            toggle_graphix()
        else:
            process_keypress(c)

        if game_delay < 0:
            game_delay = 0
        if game_delay > 100:
            game_delay = 100
        if game_delay in range(0,2):
            k = 100
        elif game_delay in range(2,6):
            k = 50
        elif game_delay in range(6,11):
            k = 25
        elif game_delay in range(11,26):
            k = 20
        elif game_delay in range(26,41):
            k = 10
        elif game_delay in range(41,71):
            k = 5
        elif game_delay in range(71,maxint + 1):
            k = 1
        else:
            k = 10
        if not graphix:
            k = 100
        if graphix:
            if ((game_cycle % k) == 0) or (game_cycle == 10):
                update_cycle_window()
            else:
                if (update_timer != mem[0:0x46C] >> 1):
                    update_cycle_window()
            update_timer = mem[0:0x46C] >> 1
            
    update_cycle_window()
    # Commented out in the original: {if (not graphix) then print;}
    score_robots()
    show_statistics()
    
def write_report():
    f = open(main_filename + report_ext, 'w')
    f.write(str(num_robots + 1)) 
    for i in range(0, num_robots + 2):
        if report_type == 2:
            f.write(str(robot[i].wins) + ' ' + str(robot[i].trials) + ' ' + str(robot[i].kills) + ' ' + str(robot[i].deaths) + ' ' + str(robot[i].fn) + ' ')
        elif report_type == 3:
            f.write(str(robot[i].wins) + ' ' + str(robot[i].trials) + ' ' + str(robot[i].kills) + ' ' + str(robot[i].deaths) + ' ' + str(robot[i].armor) + ' ' + str(robot[i].heat) + ' ' + str(robot[i].shots_fired) + ' ' + str(robot[i].fn) + ' ')
        elif report_type == 4:
            f.write(str(robot[i].wins) + ' ' + str(robot[i].trials) + ' ' + str(robot[i].kills) + ' ' + str(robot[i].deaths) + ' ' + str(robot[i].armor) + ' ' + str(robot[i].heat) + ' ' + str(robot[i].shots_fired) + ' ' + str(robot[i].hits) + ' ' + str(robot[i].damage_total) + ' ' + str(robot[i].cycles_lived) + ' ' + str(robot[i].error_count) + ' ' + str(robot[i].fn) + ' ')
        else:
            f.write(str(robot[i].wins) + ' ' + str(robot[i].trials) + ' ' + str(robot[i].fn) + ' ')
    f.close()
    
def begin_window():
    if (not graphix) or (not windoze):
        pass # May need to be a sys.exit()
    setscreen
    viewport(0,639,479)
    box(100,150,539,200)
    hole(105,155,534,195)
    setfillpattern(gray50,1)
    bar(105,155,534,195)
    setcolor(15)
    s = 'Press any to begin!'
    outtextxy(320-((len(s) << 3) >> 1), 172,s)
    flushkey
    readkey
    setscreen

def main():
    if graphix:
        begin_window 
    if matches > 0:
        for i in range(1, matches + 1):
            bout()
    if not graphix:
        print()
    if _quit:
        return
    if matches > 1:
        print()
        print()
        graph_mode(False)
        # textcolor(15)
        print('Bout complete! (', matches, ' matches)')
        print()
        k = 0
        w = 0
        for i in range(0, num_robots + 1):
            if robot[i].wins == w:
                k = k + 1
            if robot[i].wins > w:
                k = 1
                n = i
                w = robot[i].wins
        print('Robot           Wins  Matches  Kills  Deaths    Shots')
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        for i in range(0, num_robots + 1):
            # textcolor(robot_color(i))
            print(addfront(cstr(i + 1), 2) + ' - ' + addrear(robot[i].fn, 8) + addfront(cstr(robot[i].wins), 7) + addfront(cstr(robot[i].trials), 8) + addfront(cstr(robot[i].kills), 8) + addfront(cstr(robot[i].deaths), 8) + addfront(cstr(robot[i].shots_fired), 9))
        # textcolor(15)
        print()
        if k == 1:
            print('Robot #', n + 1, ' (', robot[n].fn, ') wins the bout! (score: ', w, '/', matches, ')')
        else:
            print('There is no clear victor!')
        print()
    elif graphix:
        graph_mode(False)
        show_statistics()
    if report:
        write_report()

if __name__ == "__main__":
    pygame.init()
    init()
    main()
    shutdown()
    pygame.quit()
else:
    print("Being Imported")
