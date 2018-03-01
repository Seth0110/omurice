# with the ATR2FUNC import, will we need to ATR2FUNC.function() for all of them?

import ATR2FUNC
import random#for random.seed()
import time#for random
import os#for checking files

###globals: line 69- (skipping simulator/graphics variables)

#Constant - Python has no equivalent of const
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
_T = true
_F = false
minint = -32768 #{maxint=32787 is alrady defined by turbo pascal}

#{debugging/compiler}
show_code = _F
compile_by_line = _F
max_var_len = 16
debugging_compiler = _F

#{robots}
max_robots = 31  #{starts at 0, so total is max_robots+1}
max_code = 1023  #{same here}
max_op = 3  #{etc...}
stack_size = 256
stack_base = 768
max_ram = 1023  #{but this does start at 0 (odd #, 2^n-1)}
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

#general settings
_quit = False
report = False
show_cnotice = False
kill_count = 0
report_type = 0 


class op_rec: #line 132-134
    op = [0 for i in range(0, max_op + 1)]
    
prog_type = [op_rec() for i in range(0, max_code + 1)] #line 135
#note: must be careful when accessing values of prog_type if we need attribute of class

class config_rec: #line 136-138
    scanner = 0 
    weapon = 0
    armor = 0
    engine = 0
    heatsinks = 0
    shield = 0
    mines = 0

class mine_rec: #line 139-143
    x = 0
    y = 0
    detect = 0
    _yield = 0 #yield is a special expression, subbing _yield
    detonate = False

class robot_rec: #line 144-166 - originally a "record"
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
    config = config_rec() 
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
    errorlog = open(errorlog, 'a').close() 

class missile_rec: #line 169-172 - originally a "record"
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

missile = []#line 179 - array or missiles, max_missiles = 1023
missile = [missile_rec() for i in range(0, max_missiles + 1)]

robot = []
robot = [robot_rec() for i in range(-2, max_robots + 3)]


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

# errorlog has not been declared yet
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

            print(errorlog + '<' + i + '> ' + s + ' (Line #' + ip + ') [Cycle: ' + game_cycle + ', Match: ' + played + '/' + matches + ']\n');
            print(errorlog + ' ' + mnemonic(code[ip].op[0] + code[ip].op[3] and 15) + '  ' + 
                  operand(code[ip].op[1] + (code[ip].op[3] >> 4) & 15) + ' +  ' + 
                  operand(code[ip].op[2] + (code[ip].op[3] >> 8) & 15))
            if ov != '':
                print(errorlog + '    (Values: ' + ov + ')') # was writeln
            else:
                print(errorlog); # was writeln
                
            print(errorlog + ' AX=' + addrear(chr(ram[65])+',',7))
            print(errorlog + ' BX=' + addrear(chr(ram[66])+',',7))
            print(errorlog + ' CX=' + addrear(chr(ram[67])+',',7))
            print(errorlog + ' DX=' + addrear(chr(ram[68])+',',7))
            print(errorlog + ' EX=' + addrear(chr(ram[69])+',',7))
            print(errorlog + ' FX=' + addrear(chr(ram[70])+',',7))
            print(errorlog + ' Flags=' + ram[64] + '\n') # was writeln
            print(errorlog + ' AX=' + addrear(hex(ram[65])+',',7))
            print(errorlog + ' BX=' + addrear(hex(ram[66])+',',7))
            print(errorlog + ' CX=' + addrear(hex(ram[67])+',',7))
            print(errorlog + ' DX=' + addrear(hex(ram[68])+',',7))
            print(errorlog + ' EX=' + addrear(hex(ram[69])+',',7))
            print(errorlog + ' FX=' + addrear(hex(ram[70])+',',7))
            print(errorlog + ' Flags=' + hex(ram[64]))
            print(errorlog)

def max_shown(): # line 347
    if stats_mode == 1:
        return 12
    elif stats_mode == 2:
        return 32
    else:
        return 6
            
def graph_check(n):
    ok = True
    if (not graphix) or (n<0) or (n>num_robots) or (n>=max_shown):
        ok:=false;
    return ok

# def robot_graph(n): GRAPHICAL

# def update_armor(n):
# def update_heat(n):
# def robot_error(n,i,ov):        
# def update_lives(n):
def update_cycle_window():
    if not graphix:
        print('\t' + 'Match ' + played +  '/' + matches + ', Cycle: ' + ATR2FUNC.zero_pad(game_cycle,9))
    else:
        # viewport(480,440,635,475)
        # setfillstyle(1,0)
        # bar(59,2,154,10)
        # setcolor(7)
        # outtextxy(75,03,zero_pad(game_cycle,9))
        
def setscreen():
    if not graphix:
        quit()
    # BIG GRAPHICAL PART GOES HERE
    
# def graph_mode(on):
def prog_error(n, ss): # line 569 in original code
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

# def print_code(n,p):  
def check_plen(plen):
    if plen > maxcode:
        prog_error(16,'\t\nMaximum program length exceeded, (Limit: ' + cstr(maxcode+1) + ' compiled lines)')

# def compile(n,filename):

# needs review: how does this function actually access config.attribute?
def robot_config(n):
    for r in robot:
        if config.scanner == 5:
            r.scanrange = 1500
        elif config.scanner == 4:
            r.scanrange = 1000
        elif config.scanner == 3:
            r.scanrange = 700
        elif config.scanner == 2:
            r.scanrange = 500
        elif config.scanner == 1:
            r.scanrange = 350
        else:
            r.scanrange = 250
            
        if config.weapon == 5:
            r.shotstrength = 1.5
        elif config.weapon == 4:
            r.shotstrength = 1.35
        elif config.weapon == 3:
            r.shotstrength = 1.2
        elif config.weapon == 2:
            r.shotstrength = 1
        elif config.weapon == 1:
            r.shotstrength = 0.8
        else:
            shotstrength = .5
            
        if config.armor == 5:
            r.damageadj = 0.66
            r.speedadj = 0.66
        elif config.armor == 4:
            r.damageadj = 0.77
            r.speedadj = 0.75
        elif config.armor == 3:
            r.damageadj = 0.83
            r.speedadj = 0.85
        elif config.armor == 2:
            r.damageadj = 1
            r.speedadj = 1
        elif config.armor == 1:
            r.damageadj = 1.5
            r.speedadj = 1.2
        else:
            r.damageadj = 2
            r.speedadj = 1.33
            
        if config.engine == 5:
            r.speedadj = speedadj * 1.5
        elif config.engine == 4:
            r.speedadj = speedadj * 1.35
        elif config.engine == 3:
            r.speedadj = speedadj * 1.2
        elif config.engine == 2:
            r.speedadj = speedadj * 1
        elif config.engine == 1:
            r.speedadj = speedadj * 0.8
        else:
            r.speedadj = speedadj * 0.5
            
        # heatsinks are handled seperately
        if config.mines == 5:
            r.mines = 24
        elif config.mines == 4:
            r.mines = 16
        elif config.mines == 3:
            r.mines = 10
        elif config.mines == 2:
            r.mines = 6
        elif config.mines == 1:
            r.mines = 4
        else:
            mines = 2
            config.mines = 0
            
        r.shields_up = False
        if (config.shield < 3) or (config.shield > 5):
            config.shield = 0
        if (config.heatsinks < 0) or (config.heatsinks > 5):
            config.heatsinks = 0
        
def reset_software(n):
    for r in robot:
        for i in range(0,max_ram):
            ram[i] = 0
            ram[71] = 768
            r.thd = r.hd
            r.tspd = 0
            r.scanarc = 8
            r.shift = 0
            r.err = 0
            r.overburn = False
            r.keepshift = False
            r.ip = 0
            r.accuracy = 0
            r.meters = 0
            r.delay_left = 0
            r.time_left = 0
            r.shields_up = False
            
# def reset_hardware(n):
def reset_hardware(n): # lines 1212-1256
    for i in range(1, max_robot_lines + 1):
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
                d = distance(robot[n].x, robot[n].y, robot[i].x, robot[i].y) #ATR2FUNC
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
        robot_config(n) # line 1141
        
def create_robot(n, filename): # lines 1297-1323
    if maxavail < sizeof(robot_rec): 
    # sizeof gives number of bytes occupied by robot_rec
    # maxavail returns largest dynamic variable that can be allocated at the time, what is the Python equivalent?
        prog_error(9, base_name(no_path(filename))) # where is base_name defined?
    robot[n] # original code has with robot[n]^ do... is it different here?
    init_robot(n) # needs to be ported - line 1258
    filename = ucase(btrim(filename))
    if filename == base_name(filename):
        if filename[0] == '?':
            filename = filename + locked_ext
        else:
            filename = filename + robot_ext
    if filename[0] == '?':
        filename = rstr(filename, len(filename) - 1)
    robot[n].fn = base_name(no_path(filename))
    _compile(n, filename) # needs to be ported - line 881
    robot_config(n) # ported 
    k = robot[n].config.scanner + robot[n].config.armor + robot[n].config.weapon + robot[n].config.engine + robot[n].config.heatsinks + robot[n].config.shield + robot[n].config.mines
    if k > max_config_points:
        prog_error(21, cstr(k) + '/' + cstr(max_config_points))
    #end
    
def shutdown(): # lines 1325-1351
    #graph_mode(False) # graphics
    if show_cnotice:
        #textcolor(3) # graphics
        print(progname, '', version, '')
        print(cnotice1)
        print(cnotice2)
        print(cnotice3)
    #textcolor(7) # graphics
    if not registered: # registered defined in init - how to access here?
        #textcolor(4) # graphics
        print('Unregistered version')
    else:
        print('Registered to: ', reg_name) # reg_name defined in init - how to access here?
    #textolor(7) # graphics
    print()
    if logging_errors:
        for i in range(0, num_robots + 1):
            print('Robot error-log created: ' + robot[i].fn + '.ERR')
            robot[i].errorlog = open(robot[i].errorlog, 'a').close() # needs to be checked 
    quit()

# # def delete_compile_report():
def delete_compile_report(): # originally lines 1353-1357
    if os.path.isfile(main_filename + compile_ext):
        os.remove(main_filename + compile_ext)
        
# # def write_compile_report():
def write_compile_report(): # lines 1359-1376
    f = open(main_filename + compile_ext, 'w') # local variable
    f.write(str(num_robots + 1)) 
    for i in range(0, num_robots + 1):
        f.write(str(robot[i].fn))
    f.close()
    #textcolor(15) # graphics
    print()
    print("All compiles successful!")
    print()
    shutdown()
    
# # def parse_param(s):
def parse_param(s): # originally line 1379
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
    s1 = '' # local variable
    found = False # local variable
    s = btrim(ucase(s)) # ATR2FUNC functions
    if s == '':
        return
    if s[0] == '#':
        fn = rstr(s, len(s) - 1) # ATR2FUNC for rstr, fn is local
        if fn == base_name(fn): # where is base_name defined?
            fn = fn + config_ext
        if not os.path.isfile(fn):
            prog_error(6, fn)
        f = open(fn, 'r') # local variable f
        for line in f:
            s1 = ucase(btrim(s1)) # ATR2FUNC
            if s1[0] == '#':
                prog_error(7, s1)
            else:
                parse_param(s1)
        f.close()
        found = True
    elif s[0] in ['/', '-', '=']:
        s1 = rstr(s, len(s) - 1) # ATR2FUNC
        if s1[0] == 'X':
            step_mode = value(rstr(s1, len(s1) - 1)) # ATR2FUNC
            found = True
            if step_mode == 0:
                step_mode = 1
            if (step_mode < 1) or (step_mode > 9):
                prog_error(24, rstr(s1, len(s1) - 1)) # ATR2FUNC
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
            sound_on = False # sound_on defined in init() - how to access?
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
        create_robot(num_robots, s) # need to port create_robot on line 1297
        found = True
        if num_robots == max_robots:
            print("Maximum number of robots reached.")
    else:
        prog_error(10, '')
    if not found:
        prog_error(8, s)
    #end parse_param(s)

# # def init():
def init():#originally line 1452
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
    if debugging_compiler or compile_by_line or show_code:
        print("!!! Warning !!! Compiler Debugging enabled !!!")
        print() 
    step_mode = 0 # {stepping disabled}
    logging_errors = False
    stats_mode = 0
    insane_missiles = False
    insanity = 0
    delay_per_sec = 0 # not a global but not a local?
    windoze = True
    graphix = False # not a global but not a local?
    no_gfx = True
    sound_on = True # not a global but not a local?
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
    game_limit = 100000
    game_cycle = 0 
    game_delay = default_delay
    time_slice = default_slice
    for i in range(0, max_missiles + 1):  #line 1481-1483
        missile[i].a = 0 
        missile[i].source = -1
        missile[i].x = 0
        missile[i].y = 0
        missile[i].lx = 0
        missile[i].ly = 0
        missile[i].mult = 1
    registered = False # not a global but not a local?
    reg_name = "Unregistered" # not a global but not a local?
    reg_num = 0xFFFF # not a global but not a local?
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
    delete_compile_report() # from line 1353 - ported
    if paramcount > 0: # where is paramcount declared? 
        parse_param(btrim(ucase(paramstr(i)))) # uses ATR2FUNC
    else:
        prog_error(5, '') # ported
    temp_mode = step_mode # {store initial step_mode}
    if logging_errors:
        for i in range (0, num_robots + 1):
            robot[i].errorlog = open(base_name(robot[i].fn) + '.ERR', 'w') # where is base_name defined? 
            if os.path.isfile(robot[i].errorlog):
                os.remove(robot[i].errorlog)
            robot[i].errorlog = open(base_name(robot[i].fn) + '.ERR', 'w') # where is base_name defined, again?
            robot[i].errorlog.close()
    if compile_only:
        write_compile_report() # line 1359 ported
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
        print("Freemem: ", memavail) # where is memavail defined? 
        print()
# end init

# def draw_robot(n): GRAPHICAL

# what on earth is ram[]?!?
def get_from_ram(n,i,j):
    for r in robot:
        if (i < 0) or (i > (max_ram + 1) + (((max_code + 1) << 3) - 1)):
            k = 0
            r.robot_error(n,4,cstr(i))
        else:
            if i <= max_ram:
                k = ram[i]
            else:
                l = i - max_ram - 1
                k = code[l >> 2].op[l & 3]
    return k

def get_val(n,c,o):
    k = 0
    for r in robot:
        j = (r.code[c].op[max_op] >> (4*o)) & 15
        i = r.code[c].op[o]
        if (j & 7) == 1:
            k = get_from_ram(n,i,j)
        else:
            k = i
        if (j & 8) > 0:
            k = get_from_ram(n,k,j)
    get_val = k

def put_val(n,c,o,v):
    k:=0
    i:=0
    j:=0
    for r in robot:
        j = (r.code[c].op[max_op] >> (4 * o)) & 15
        i = r.code[c].op[o]
        if (j and 7) == 1:
            if (i<0) or (i>max_ram):
                robot_error(n,4,cstr(i))
            else:
                if (j and 8) > 0:
                    i:=ram[i];
                    if (i < 0) or (i > max_ram):
                        robot_error(n,4,cstr(i))
                    else:
                        ram[i] = v
                else:
                    ram[i] = v
        else:
            robot_error(n,3,'');

def push(n,v):
    for r in robot:
        if (ram[71] >= stack_base) and (ram[71] < (stack_base + stack_size)):
            ram[ram[71]] = v
            ram[71] = ram[71] + 1
        else:
            robot_error(n,1,cstr(ram[71]))
            
def pop(n):
    for r in robot:
        if (ram[71] > stack_base) and (ram[71] <= (stack_base + stack_size)):
            ram[71] = ram[71] - 1
            k = ram[ram[71]];
        else:
            robot_error(n,5,cstr(ram[71]));
    return k;

def find_label(n,l,m):
    k = -1;
    for r in robot:
        if m == 3:
            robot_error(n,9,'')
        elif m == 4:
            k:=l
        else:
            for i in range(plen,0,-1):
                j = code[i].op[max_op] & 15
                if (j=2) and (code[i].op[0]=l) then k:=i;
    return k

def init_mine(n,detectrange,size):
    for r in robot:
        k = -1
        for i in range(0,max_mines):
            if ((mine[i].x < 0) or (mine[i].x > 1000) or (mine[i].y < 0) or (mine[i].y > 1000) or (mine[i].yield <= 0)) and (k < 0):
                k = i
            if k >= 0:
                mine[k].x = x
                mine[k].y = y
                mine[k].detect = detectrange
                mine[k].yield = size
                mine[k].detonate = false
                click

def count_missiles():
    k = 0
    for i in range(0,max_missiles):
        if missile[i].a > 0:
            k = k + 1
    return k

# def init_missile(xx,yy,xxv,yyv,dir,s,blast,ob):
# def damage(n,d,physical):
# def scan(n):
# def com_transmit(n,chan,data):
# def com_receive(n):
# def in_port(n,p,time_used):
# def out_port(n,p,v,time_used):
# def call_int(n,int_num,time_used):
# def jump(n,o,inc_ip):
# def update_debug_bars():
# def update_debug_system():
# def update_debug_registers():
# def update_debug_flags():
# def update_debug_memory():
# def update_debug_code():
# def update_debug_window():
# def init_debug_window():
# def close_debug_window():
# def gameover():
# def toggle_graphix():
# def invalid_microcode(n,ip):
# def process_keypress(c):
# def execute_instruction(n):
# def do_robot(n):
# def do_mine(n,m):
# def do_missile(n):
# def victor_string(k,n):
# def show_statistics():
# def score_robots():
# def init_bout():
# def bout():
# def write_report():
# def begin_window():
# def main():
