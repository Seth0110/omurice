# comments contained within {} are comments from the original code
# but not all comments from original code are included

# special Python expressions that are variables and functions in the original code are
# changed by adding an underscore in the front (ex: _yield, _quit, _compile)

# In python, global variables may be accessed from within a function,
# but to change those variables, the global keyword must be used

# Some local variables have the same name as global variables
# I commented them as I saw them but some may be left uncommented - careful!

import random # for random
import time # for random
import os # for checking files
import sys # for counting number of arguments on command line

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


def max_shown(): # lines 347-354
    if stats_mode == 1:
        return 12
    elif stats_mode == 2:
        return 32
    else:
        return 6
    

def prog_error(n, ss): # lines 569-610
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
        
    
def init_robot(n): # lines 1258-1295
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
    reset_software(n) # ported
    

def create_robot(n, filename): # lines 1297-1323
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

    
def shutdown(): # lines 1325-1351
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


def delete_compile_report(): # originally lines 1353-1357
    if os.path.isfile(main_filename + compile_ext):
        os.remove(main_filename + compile_ext)
      
        
def write_compile_report(): # lines 1359-1376
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

    
def parse_param(s): # lines 1379-1449
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
        if fn == fn.split('.')[0]:  
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
        
 
def init(): # lines 1452-1544
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
    game_limit = 100000
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
    if len(sys.argv - 1) > 0: # paramcount is # of args passed to command line which is len(sys.argv) 
        parse_param(btrim(ucase(paramstr(i)))) # uses ATR2FUNC
    else:
        prog_error(5, '') # ported
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


def scan(n): # lines 1915-1978
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


def com_transmit(n, chan, data): # lines 1980-1996
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


def com_receive(n): # lines 1998-2016
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
    

def update_debug_window(): # lines 2404-2428
    if graphix and (step_mode > 0):
        update_debug_bars # {armour + heat}
        update_debug_system # {system variables}
        update_debug_registers # {registers}
        update_debug_flags # {flag register}
        update_debug_memory # {memory}
        update_debug_code # {code}


def gameover(): # lines 2578-2592
    if (game_cycle >= game_limit) and (game_limit > 0):
        return True
    if game_cycle & 31 == 0:
        k = 0
        for n in range(0, num_robots + 1):
            if robot[n].armor > 0:
                k += 1
            if k <= 1:
                return True
            else:
                return False
    else:
        return False
        

def toggle_graphix(): # lines 2594-2604
    graph_mode(not graphix)
    if not graphix:
        #textcolor(7) # graphics-related
        print('Match ' + played + '/' + matches + ', Battle in progress...')
        print()
    else:
        setscreen


def invalid_microcode(n, ip): # lines 2606-2618
    invalid = False
    for i in range(0, 3):
        k = (robot[n].code[ip].op[max_op] >> (i << 2)) & 7 
        if not (k in [0, 1, 2, 4]):
            invalid = True
    return invalid
        
        
def process_keypress(c): # lines 2620-2636
    global timing
    global show_arcs
    global debug_info
    global windoze
    global bout_over
    global _quit
    global step_loop
    if c == 'C':
        calibrate_timing # ATR2FUNC
    elif c == 'T':
        timing = not timing
    elif c == 'A':
        show_arcs = not show_arcs
    elif (c == 'S') or (c == 'Q'):
        if sound_on:
            chirp # ATR2FUNC
        sound_on = not sound_on # initialized in ATR2FUNC
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
        
        
def execute_instruction(n): # lines 2638-2980
    global step_count
    global step_loop
    global executed
    robot[n].ram[0] = robot[n].tspd
    robot[n].ram[1] = robot[n].thd
    robot[n].ram[2] = robot[n].shift
    robot[n].ram[3] = robot[n].accuracy 
    time_used = 1 # local variable
    inc_ip = True # local variable
    loc = 0 # local variable
    if (robot[n].ip > robot[n].plen) or (robot[n].ip < 0):
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
    if (not((robot[n].code[robot[n].ip].op[max_op] & 7) in [0, 1])):
        time_used = 0
    else:
        if get_val(n, robot[n].ip, 0) == 0:
            executed += 1
        elif get_val(n, robot[n].ip, 0) == 1:
            put_val(n, robot[n].ip, 1, get_val(n, robot[n].ip, 1) + get_val(n, robot[n].ip, 2))
            executed += 1
        elif get_val(n, robot[n].ip, 0) == 2:
            put_val(n, robot[n].ip, 1, get_val(n, robot[n].ip, 1) - get_val(n, robot[n].ip, 2))
            executed += 1
        elif get_val(n, robot[n].ip, 0) == 3:
            put_val(n, robot[n].ip, 1, get_val(n, robot[n].ip, 1) | get_val(n, robot[n].ip, 2))
            executed += 1
        elif get_val(n, robot[n].ip, 0) == 4:
            put_val(n, robot[n].ip, 1, get_val(n, robot[n].ip, 1) & get_val(n, robot[n].ip, 2))
            executed += 1
        elif get_val(n, robot[n].ip, 0) == 5:
            put_val(n, robot[n].ip, 1, get_val(n, robot[n].ip, 1) ^ get_val(n, robot[n].ip, 2))
            executed += 1
        elif get_val(n, robot[n].ip, 0) == 6:
            put_val(n, robot[n].ip, 1, not(get_val(n, robot[n].ip, 1)))
            executed += 1
        elif get_val(n, robot[n].ip, 0) == 7:
            put_val(n, robot[n].ip, 1, get_val(n, robot[n].ip, 1) * get_val(n, robot[n].ip, 2))
            time_used = 10
            executed += 1
        elif get_val(n, robot[n].ip, 0) == 8:
            j = get_val(n, robot[n].ip, 2)
            if j != 0:
                put_val(n, robot[n].ip, 1, get_val(n, robot[n].ip, 1) // j)
            time_used = 10
            executed += 1
        elif get_val(n, robot[n].ip, 0) == 9:
            j = get_val(n, robot[n].ip, 2)
            if j != 0:
                put_val(n, robot[n].ip, 1, get_val(n, robot[n].ip, 1) % j)
            else:
                robot_error(n, 8, '')
            time_used = 10
            executed += 1
        elif get_val(n, robot[n].ip, 0) == 10:
            robot[n].ip = pop(n)
            if (robot[n].ip < 0) or (robot[n].ip > robot[n].plen):
                robot_error(n, 7, cstr(robot[n].ip))
            executed += 1
        elif get_val(n, robot[n].ip, 0) == 11:
            loc = find_label(n, get_val(n, robot[n].ip, 1), code[robot[n].ip].op[max_op] >> (1 * 4)) # local variable
            if loc >= 0:
                push(n, robot[n].ip)
                inc_ip = False # local variable
                robot[n].ip = loc
            else:
                robot_error(n, 2, cstr(get_val(n, robot[n].ip, 1)))
            executed += 1
        elif get_val(n, robot[n].ip, 0) == 12:
            jump(n, 1, inc_ip)
            executed += 1
        elif get_val(n, robot[n].ip, 0) == 13:
            if robot[n].ram[64] & 2 > 0:
                jump(n, 1, inc_ip)
            time_used = 0
            executed += 1
        elif get_val(n, robot[n].ip, 0) == 14:
            if robot[n].ram[64] & 4 > 0:
                jump(n, 1, inc_ip)
            time_used = 0
            executed += 1
        elif get_val(n, robot[n].ip, 0) == 15:
            if robot[n].ram[64] & 1 == 0:
                jump(n, 1, inc_ip)
            time_used = 0
            executed += 1
        elif get_val(n, robot[n].ip, 0) == 16:
            if robot[n].ram[64] & 1 > 0:
                jump(n, 1, inc_ip)
            time_used = 0
            executed += 1
        elif get_val(n, robot[n].ip, 0) == 17:
            robot[n].ram[4] = get_val(n, robot[n].ip, 1)
            put_val(n, robot[n].ip, 1, get_val(n, robot[n].ip, 2))
            put_val(n, robot[n].ip, 2, robot[n].ram[4])
            time_used = 3
            executed += 1
        elif get_val(n, robot[n].ip, 0) == 18:
            robot[n].ram[67] = get_val(n, robot[n].ip, 1)
            executed += 1
        elif get_val(n, robot[n].ip, 0) == 19:
            robot[n].ram[67] -= 1
            if robot[n].ram[67] > 0:
                jump(n, 1, inc_ip)
            executed += 1
        elif get_val(n, robot[n].ip, 0) == 20:
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
        elif get_val(n, robot[n].ip, 0) == 21:
            k = get_val(n, robot[n].ip, 1) & get_val(n, robot[n].ip, 2)
            robot[n].ram[64] = robot[n].ram[64] & 0xFFF0
            if k == get_val(n, robot[n].ip, 2):
                robot[n].ram[64] = robot[n].ram[64] | 1
            if k == 0:
                robot[n].ram[64] = robot[n].ram[64] | 8
            executed += 1
        elif get_val(n, robot[n].ip, 0) == 22:
            put_val(n, robot[n].ip, 1, get_val(n, robot[n].ip, 2))
            executed += 1
        elif get_val(n, robot[n].ip, 0) == 23:
            put_val(n, robot[n].ip, 1, robot[n].code[robot[n].ip].op[2])
            time_used = 2
            executed += 1
        elif get_val(n, robot[n].ip, 0) == 24:
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
        elif get_val(n, robot[n].ip, 0) == 25:
            k = get_val(n, robot[n].ip, 2)
            if (k >= 0) and (k <= max_ram):
                robot[n].ram[k] = get_val(n, robot[n].ip, 1)
            else:
                robot_error(n, 4, cstr(k))
            time_used = 2
            executed += 1
        elif get_val(n, robot[n].ip, 0) == 26:
            call_int(n, get_val(n, robot[n].ip, 1), time_used)
            executed += 1
        elif get_val(n, robot[n].ip, 0) == 27:
            time_used = 4
            put_val(n, robot[n].ip, 2, in_port(n, get_val(n, robot[n].ip, 1), time_used))
            executed += 1
        elif get_val(n, robot[n].ip, 0) == 28:
            time_used = 4
            out_port(n, get_val(n, robot[n].ip, 1), get_val(n, robot[n].ip, 2), time_used)
            executed += 1
        elif get_val(n, robot[n].ip, 0) == 29:
            time_used = get_val(n, robot[n].ip, 1)
            executed += 1
        elif get_val(n, robot[n].ip, 0) == 30:
            push(n, get_val(n, robot[n].ip, 1))
            executed += 1
        elif get_val(n, robot[n].ip, 0) == 31:
            put_val(n, robot[n].ip, 1, pop(n))
            executed += 1
        elif get_val(n, robot[n].ip, 0) == 32:
            robot_error(n, get_val(n, robot[n].ip, 1), '')
            time_used = 0
            executed += 1
        elif get_val(n, robot[n].ip, 0) == 33:
            put_val(n, robot[n].ip, 1, get_val(n, robot[n].ip, 1) + 1)
            executed += 1
        elif get_val(n, robot[n].ip, 0) == 34:
            put_val(n, robot[n].ip, 1, get_val(n, robot[n].ip, 1) - 1)
            executed += 1
        elif get_val(n, robot[n].ip, 0) == 35:
            put_val(n, robot[n].ip, 1, get_val(n, robot[n].ip, 1) << get_val(n, robot[n].ip, 2))
            executed += 1
        elif get_val(n, robot[n].ip, 0) == 36:
            put_val(n, robot[n].ip, 1, get_val(n, robot[n].ip, 1) >> get_val(n, robot[n].ip, 2))
            executed += 1
        elif get_val(n, robot[n].ip, 0) == 37:
            put_val(n, robot[n].ip, 1, rol(get_val(n, robot[n].ip, 1), get_val(n, robot[n].ip, 2)))
            executed += 1
        elif get_val(n, robot[n].ip, 0) == 38:
            put_val(n, robot[n].ip, 1, ror(get_val(n, robot[n].ip, 1), get_val(n, robot[n].ip, 2)))
            executed += 1
        elif get_val(n, robot[n].ip, 0) == 39:
            time_used = 0
            if robot[n].ram[64] & 8 > 0:
                jump(n, 1, inc_ip)
            executed += 1
        elif get_val(n, robot[n].ip, 0) == 40:
            time_used = 0
            if robot[n].ram[64] & 8 == 0:
                jump(n, 1, inc_ip)
            executed += 1
        elif get_val(n, robot[n].ip, 0) == 41:
            if (robot[n].ram[64] & 1 > 0) or (robot[n].ram[64] & 4 > 0):
                jump(n, 1, inc_ip)
            time_used = 0
            executed += 1
        elif get_val(n, robot[n].ip, 0) == 42:
            if (robot[n].ram[64] & 1 > 0) or (robot[n].ram[64] & 2 > 0):
                jump(n, 1, inc_ip)
            time_used = 0
            executed += 1
        elif get_val(n, robot[n].ip, 0) == 43:
            put_val(n, robot[n].ip, 1, sal(get_val(n, robot[n].ip, 1), get_val(n, robot[n].ip, 2)))
            executed += 1
        elif get_val(n, robot[n].ip, 0) == 44:
            put_val(n, robot[n].ip, 1, sar(get_val(n, robot[n].ip, 1), get_val(n, robot[n].ip, 2)))
            executed += 1
        elif get_val(n, robot[n].ip, 0) == 45:
            put_val(n, robot[n].ip, 1, 0 - get_val(n, robot[n].ip, 1))
            executed += 1
        elif get_val(n, robot[n].ip, 0) == 46:
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
        update_debug_window
        

def do_robot(n): # lines 2982-3119
    global executed
    if (n < 0) or (n > num_robots):
        return
    if robot[n].armor <= 0:
        return
    robot[n].time_left = time_slice
    if (robot[n].time_left > robot[n].robot_time_limit) and (robot[n].robot_time_limit > 0):
        robot[n].time_left = robot[n].robot_time_limit
    if (robot[n].time_left > robot[n].max_time) and (robot[n].max_time > 0):
        robot[n].time_left = robot[n].max_time
    executed = 0
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
    if robot[n].shields_up and (game_cycle and 3 == 0):
        robot[n].heat += 1
    if not robot[n].shields_up:
        if robot[n].heat > 0:
            if config.heatsinks == 5:
                if game_cycle & 1 == 0:
                    robot[n].heat -= 1
            elif config.heatsinks == 4:
                if game_cycle % 3 == 0:
                    robot[n].heat -= 1
            elif config.heatsinks == 3:
                if game_cycle & 3 == 0:
                    robot[n].heat -= 1
            elif config.heatsinks == 2:
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
    

def do_mine(n, m): # lines 3121-3176
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
        
        
def victor_string(k, n): # lines 3284-3293
    s = ''
    if k == 1:
        s = 'Robot #' + cstr(n + 1) + ' (' + robot[n].fn + ') wins!'
    if k == 0:
        s = 'Simultaneous destruction, match is a tie.'
    if k > 1:
        s = 'No clear victor, match is a tie.'
    return s


def score_robots(): # lines 3363-3376
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
        
        
def init_bout(): # lines 3378-3405
    global game_cycle
    game_cycle = 0
    for i in range(0, max_missiles + 1):
        missile[i].a = 0
        missile[i].source = -1
        missile[i].x = 0
        missile[i].y = 0
        missile[i].lx = 0
        missile[i].ly = 0
        missile[i].mult = 1
    for i in range(0, num_robots):
        robot[i].mem_watch = 128
        reset_hardware(i)
        reset_software(i)
    if graphix:
        setscreen
    if graphix and (step_mode > 0):
        init_debug_window
    #if not graphix:
        #textcolor(7)


def write_report(): # lines 3523-3543
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
    

def main(): # lines 3563-3610
    if graphix: # defined in ATR2FUNC 
        begin_window 
    if matches > 0:
        for i in range(1, matches + 1):
            bout 
    if not graphix:
        print()
    if _quit:
        return
    if matches > 1:
        print()
        print()
        graph_mode(False)
        #textcolor(15) # graphical
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
            #textcolor(robot_color(i)) # graphical
            print(addfront(cstr(i + 1), 2) + ' - ' + addrear(robot[i].fn, 8) + addfront(cstr(robot[i].wins), 7) + addfront(cstr(robot[i].trials), 8) + addfront(cstr(robot[i].kills), 8) + addfront(cstr(robot[i].deaths), 8) + addfront(cstr(robot[i].shots_fired), 9))
        #textcolor(15) # graphical
        print()
        if k == 1:
            print('Robot #', n + 1, ' (', robot[n].fn, ') wins the bout! (score: ', w, '/', matches, ')')
        else:
            print('There is no clear victor!')
        print()
    elif graphix:
        graph_mode(False)
        show_statistics 
    if report:
        write_report 
    
    