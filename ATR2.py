# comments contained within {} are comments from the original code
# but not all comments from original code are included

# special Python expressions that are variables in the original code are
# changed by adding an underscore in the front (ex: _yield, _quit)

# In python, global variables may be accessed from within a function,
# but to change those variables, the global keyword must be used

import random # for random
import time # for random
import os # for checking files

# globals: lines 69-128 (commenting out some simulator/graphics variables)

# Constant - Python has no equivalent of const
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
minint = -32768 # {maxint=32787 is alrady defined by turbo pascal}

# {debugging/compiler}
show_code = _F
compile_by_line = _F
max_var_len = 16
debugging_compiler = _F

# {robots}
max_robots = 31 # {starts at 0, so total is max_robots+1}
max_code = 1023 # {same here}
max_op = 3 # {etc...}
stack_size = 256
stack_base = 768
max_ram = 1023 # {but this does start at 0 (odd #, 2^n-1)}
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

# simulator and graphics
screen_scale = 0.46
screen_x = 5
screen_y = 5
robot_scale = 6
default_delay = 20
default_slice = 5
#mine_circle = trunc(mine_blast*screen_scale)+1;
#blast_circle = trunc(blast_radius*screen_scale)+1;
#mis_radius = trunc(hit_range/2)+1;
max_robot_lines = 8
#Gray50 : FillPatternType = ($AA, $55, $AA, $55, $AA, $55, $AA, $55);

# general settings
_quit = False
report = False
show_cnotice = False
kill_count = 0
report_type = 0 


# Classes - "records" in original code
class op_rec: # line 132-134
    op = [0 for i in range(0, max_op + 1)]
    
prog_type = [op_rec() for i in range(0, max_code + 1)] # line 135
# note: must be careful when accessing values of prog_type if we need attribute of class

class config_rec: # line 136-138
    scanner = 0 
    weapon = 0
    armor = 0
    engine = 0
    heatsinks = 0
    shield = 0
    mines = 0

class mine_rec: # line 139-143
    x = 0
    y = 0
    detect = 0
    _yield = 0 # yield is a special expression, substituting _yield
    detonate = False

class robot_rec: # line 144-166
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
    errorlog = open('errorlog', 'a').close() # each robot has an errorlog file

class missile_rec: # line 169-172
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

# {--robot variables--}
# lines 176-179
num_robots = 0
robot = [] # line 178 - array of robot_rec
robot = [robot_rec() for i in range(-2, max_robots + 3)]
missile = [] # line 179 - array of missile_rec
missile = [missile_rec() for i in range(0, max_missiles + 1)]

# {--compiler variables--}
# lines 181-189
f = open('f', 'a').close()
numvars = 0
numlabels = 0
maxcode = 0
lock_pos = 0
lock_dat = 0
varname = ['' for i in range(0, max_vars)]
varloc = [0 for i in range(0, max_vars)]
labelname = ['' for i in range(0, max_vars)]
labelnum = [0 for i in range(0, max_labels)]
show_source = False
compile_only = False
lock_code = ''

# {--simulator/graphics variables--}
# lines 191-204
bout_over = False
step_mode = 0
temp_mode = 0
step_count = 0
step_loop = False
old_shields = False
insane_missiles = False
debug_info = False
windoze = False
no_gfx = False
logging_errors = False
timing = False
show_arcs = False
game_delay = 0
time_slice = 0
insanity = 0
update_timer = 0
max_gx = 0
max_gy = 0
stats_mode = 0
game_limit = 0
game_cycle = 0
matches = 0
played = 0
executed = 0

# {--general settings--}
# lines 206-208
_quit = False
report = False
show_cnotice = False
kill_count = 0
report_type = 0


def max_shown(): # line 347
    if stats_mode == 1:
        return 12
    elif stats_mode == 2:
        return 32
    else:
        return 6
    

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


def delete_compile_report(): # originally lines 1353-1357
    if os.path.isfile(main_filename + compile_ext):
        os.remove(main_filename + compile_ext)
      
        
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
    #end parse_params()
                 
        
 
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