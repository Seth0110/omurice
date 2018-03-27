# with the ATR2FUNC import, will we need to ATR2FUNC.function() for all of them?

import ATR2FUNC
import random # for random.seed()
import time # for random
import os # for checking files

# globals: line 69- (skipping simulator/graphics variables)

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
_T = true
_F = false
minint = -32768 # {maxint=32787 is alrady defined by turbo pascal}

# {debugging/compiler}
show_code = _F
compile_by_line = _F
max_var_len = 16
debugging_compiler = _F

# {robots}
max_robots = 31  # {starts at 0, so total is max_robots+1}
max_code = 1023  # {same here}
max_op = 3  # {etc...}
stack_size = 256
stack_base = 768
max_ram = 1023  # {but this does start at 0 (odd #, 2^n-1)}
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

# general settings
_quit = False
report = False
show_cnotice = False
kill_count = 0
report_type = 0 


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
    _yield = 0 # yield is a special expression, subbing _yield
    detonate = False

class robot_rec: # line 144-166 - originally a "record"
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

class missile_rec: # line 169-172 - originally a "record"
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

missile = [] # line 179 - array or missiles, max_missiles = 1023
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

# # def max_shown():
    
def graph_check(n):
    ok = True
    if (not graphix) or (n < 0) or (n > num_robots) or (n >= max_shown):
        ok = False
    return ok

# def robot_graph(n): GRAPHICAL

# def update_armor(n):
# def update_heat(n):
# def robot_error(n,i,ov):        
# def update_lives(n):
def update_cycle_window():
    if not graphix:
        print('\t' + 'Match ' + played +  '/' + matches + ', Cycle: ' + ATR2FUNC.zero_pad(game_cycle,9))
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
    
# def graph_mode(on):
# # def prog_error(n,ss):

# def print_code(n,p):  
def check_plen(plen):
    if plen > maxcode:
        prog_error(16,'\t\nMaximum program length exceeded, (Limit: ' + cstr(maxcode+1) + ' compiled lines)')

def _compile(n,filename):
    lock_code = ''
    lock_pos = 0
    locktype = 0
    lock_dat = 0
    if not exist(filename):
        prog_error(8,filename)
    textcolor(robot_color(n))
    print('Compiling robot #' + str(n + 1) + ': ' + filename)
    is_locked = False
    textcolor(robot_color(n))
    numvars = 0
    numlabels = 0
    for k in range(0, max_code):
        for i in range(0, max_op):
            code[k].op[i] = 0
    plen = 0
    f = open(filename,'r') # DOES THIS NEED TO HAVE WRITE PERMISSIONS
    s = ''
    linecount = 0
    for line in f: # This whole loop is probably bugged...
        if s == '#END' or plen > maxcode:
            break
        linecount += 1
        if lock_code != '':
            for i in s:
                lock_pos += 1
                if lock_pos > len(lock_code):
                    lock_pos = 0
                if lock_code != '':
                    lock_pos += 1
                    if lock_pos > len(lock_code):
                        lock_pos = 0
                    if locktype == 3: # THIS MUST MATCH ATRLOCK FILE ALGORITHM
                        s[i] = chr((ord(s[i]) - 1) ^ (ord(lock_code[lock_pos]) ^ lock_dat))
                    if locktype == 2:
                        s[i] = chr(ord(s[i]) ^ (ord(lock_code[lock_pos]) ^ 1))
                    else:
                        s[i] = chr(ord(s[i]) ^ ord(lock_code[lock_pos]))
                lock_dat = ord(s[i]) & 15
            # s = btrim(s)
            orig_s = s
            t = '' # strings in Python are immutable
            for i in s-list:
                if int(i) in range(0,33) or int(i) in range(128,256):
                   t += ' '
                else:
                    t = i
            if show_source and ((lock_code == '') or debugging_compiler):
                print(zero_pad(linecount, 3) + ':' + zero_pad(plen, 3) + ' ' + s)
            if debugging_compiler:
                if readkey == chr(27):
                    sys.exit()
            k = 0
            for i in range(len(t),0,-1):
                if i == ';':
                    k = i
            if k > 0:
                s = lstr(t, k - 1)
            # s = btrim(t.upper())
            for i in range(0,max_op):
                pp[i] = ''
            if (len(s) > 0) and (s[0] != ';'):
                if s[0] == '#': # Compiler Directives
                    s1 = rstr(s, length(s) - 1).upper() # had a btrim
                    msg = rstr(orig_s, len(orig_s) - 5) # had a btrim
                    k = 0
                    for i in range(0, s1):
                        if (k == 0) and (s1[i] == ' '):
                            k = i
                    k -= 1
                    if k > 1:
                        s2 = lstr(s1, k)
                        s3 = rstr(s1, len(s1) - k).upper() # had a btrim
                        k = 0
                        if numvars > 0:
                            for i in range(0, numvars):
                                if s3 = varname[i]:
                                    k = i
                        if (s2 = 'DEF') and (numvars < max_vars):
                            if len(s3) > max_var_len:
                                prog_error(12, s3)
                            elif k > 0: # This had an obscure if-else structure
                                prog_error(11, s3)
                            else:
                                numvars += 1
                                if numvars > max_vars:
                                    prog_error(11, s3)
                                else:
                                    numvars += 1
                                    if numvars > max_vars:
                                        prog_error(14, '')
                                    else:
                                        varname[numvars] = s3
                                        varloc[numvars] = 127 + numvars
                        elif (lstr(s2, 4) = 'LOCK'):
                            is_locked = True
                            if len(s2) > 4:
                                locktype = value(rstr(s2, len(s2) - 4))
                                lock_code = btrim(s3.upper())
                                print('Robot is of LOCKed format from this point forward. [' + locktype + ']')
                                
                                
                        
       
#    while (not eof(f)) and (s != '#END') (and (plen<=maxcode)):
#     begin
#      readln(f,s);
#      inc(linecount);
#      if locktype<3 then lock_pos:=0;
#      if lock_code<>'' then
#       for i:=1 to length(s) do
#        begin
#         inc(lock_pos); if lock_pos>length (lock_code) then lock_pos:=1;
#         case locktype of
#          3:s[i]:=char((ord(s[i])-1) xor (ord(lock_code[lock_pos]) xor lock_dat));
#          2:s[i]:=char(ord(s[i]) xor (ord(lock_code[lock_pos]) xor 1));
#          else s[i]:=char(ord(s[i]) xor ord(lock_code[lock_pos]));
#         end;
#         lock_dat:=ord(s[i]) and 15;
#        end;
#      s:=btrim(s);
#      orig_s:=s;
#      for i:=1 to length(s) do
#       if s[i] in [#0..#32,',',#128..#255] then s[i]:=' ';
#      if show_source and ((lock_code='') or debugging_compiler) then
#         writeln(zero_pad(linecount,3)+':'+zero_pad(plen,3)+' ',s);
#      if debugging_compiler then
#         begin if readkey=#27 then halt; end;
#      {-remove comments-}
#      k:=0;
#      for i:=length(s) downto 1 do
#          if s[i]=';' then k:=i;
#      if k>0 then s:=lstr(s,k-1);
#      s:=btrim(ucase(s));
#      for i:=0 to max_op do pp[i]:='';
#      if (length(s)>0) and (s[1]<>';') then
#       begin
#        case s[1] of
#         '#':begin (*  Compiler Directives  *)
#              s1:=ucase(btrim(rstr(s,length(s)-1)));
#              msg:=btrim(rstr(orig_s,length(orig_s)-5));
#              k:=0;
#              for i:=1 to length(s1) do
#               if (k=0) and (s1[i]=' ') then k:=i;
#              dec(k);
#              if k>1 then
#               begin
#                s2:=lstr(s1,k);
#                s3:=ucase(btrim(rstr(s1,length(s1)-k)));
#                k:=0;
#                if numvars>0 then
#                 for i:=1 to numvars do
#                  if s3=varname[i] then k:=i;
#                if (s2='DEF') and (numvars<max_vars) then
#                 begin
#                  if length(s3)>max_var_len then prog_error(12,s3)
#                   else
#                  if k>0 then prog_error(11,s3)
#                   else
#                    begin
#                     inc(numvars);
#                     if numvars>max_vars then prog_error(14,'')
#                      else begin
#                            varname[numvars]:=s3;
#                            varloc [numvars]:=127+numvars;
#                           end;
#                    end;
#                 end
#                else if (lstr(s2,4)='LOCK') then
#                 begin
#                  {FIFI}
#                  is_locked:=true; {this robot is locked}
#                  {/FIFI}
#                  if length(s2)>4 then locktype:=value(rstr(s2,length(s2)-4));
#                  lock_code:=btrim(ucase(s3));
#                  writeln('Robot is of LOCKed format from this point forward. [',locktype,']');
#                  {writeln('Using key: "',lock_code,'"');}
#                  for i:=1 to length(lock_code) do
#                   lock_code[i]:=char(ord(lock_code[i])-65);
#                 end
#                else if (s2='MSG') then name:=msg
#                else if (s2='TIME') then
#                 begin
#                  robot_time_limit:=value(s3);
#                  if robot_time_limit<0 then robot_time_limit:=0;
#                 end
#                else if (s2='CONFIG') then
#                 begin
#                  if (lstr(s3,8)='SCANNER=') then config.scanner:=
#                      value(rstr(s3,length(s3)-8))
#                  else if (lstr(s3,7)='SHIELD=') then config.shield:=
#                          value(rstr(s3,length(s3)-7))
#                  else if (lstr(s3,7)='WEAPON=') then config.weapon:=
#                          value(rstr(s3,length(s3)-7))
#                  else if (lstr(s3,6)='ARMOR=') then config.armor:=
#                          value(rstr(s3,length(s3)-6))
#                  else if (lstr(s3,7)='ENGINE=') then config.engine:=
#                          value(rstr(s3,length(s3)-7))
#                  else if (lstr(s3,10)='HEATSINKS=') then config.heatsinks:=
#                          value(rstr(s3,length(s3)-10))
#                  else if (lstr(s3,6)='MINES=') then config.mines:=
#                          value(rstr(s3,length(s3)-6))
#                  else prog_error(20,s3);
#                  with config do
#                    begin
#                      if scanner<0 then scanner:=0; if scanner>5 then scanner:=5;
#                      if shield<0 then shield:=0;   if shield>5 then shield:=5;
#                      if weapon<0 then weapon:=0;   if weapon>5 then weapon:=5;
#                      if armor<0 then armor:=0;     if armor>5 then armor:=5;
#                      if engine<0 then engine:=0;   if engine>5 then engine:=5;
#                      if heatsinks<0 then heatsinks:=0; if heatsinks>5 then heatsinks:=5;
#                      if mines<0 then mines:=0;     if mines>5 then mines:=5;
#                    end;
#                 end
#                else writeln('Warning: unknown directive "'+s2+'"');
#               end;
#             end;
#         '*':begin  (*  Inline Pre-Compiled Machine Code  *)
#              check_plen(plen);
#              for i:=0 to max_op do pp[i]:='';
#              for i:=2 to length(s) do
#               if s[i]='*' then prog_error(23,s);
#              k:=0; i:=1; s1:='';
#              if length(s)<=2 then prog_error(22,s);
#              while (i<length(s)) and (k<=max_op) do
#               begin
#                inc(i);
#                if ord(s[i]) in [33..41,43..127] then pp[k]:=pp[k]+s[i]
#                  else if (ord(s[i]) in [0..32,128..255]) and
#                          (ord(s[i-1]) in [33..41,43..127]) then inc(k);
#               end;
#              for i:=0 to max_op do
#               code[plen].op[i]:=str2int(pp[i]);
#              inc(plen);
#             end;
#         ':':begin  (*  :labels  *)
#              check_plen(plen);
#              s1:=rstr(s,length(s)-1);
#              for i:=1 to length(s1) do
#               if not (s1[i] in ['0'..'9']) then
#                  prog_error(1,s);
#              code[plen].op[0]:=str2int(s1);
#              code[plen].op[max_op]:=2;
#              if show_code then print_code(n,plen);
#              inc(plen);
#             end;
#         '!':begin (*  !labels  *)
#              check_plen(plen);
#              s1:=btrim(rstr(s,length(s)-1));
#              k:=0;
#              for i:=length(s1) downto 1 do
#                  if s1[i] in [';',#8,#9,#10,' ',','] then k:=i;
#              if k>0 then s1:=lstr(s1,k-1);
#              k:=0;
#              for i:=1 to numlabels do
#               if (labelname[i]=s1) then
#                begin
#                 if (labelnum[i]>=0) then prog_error(13,'"!'+s1+'" ('+cstr(labelnum[i])+')');
#                 k:=i;
#                end;
#              if (k=0) then
#               begin
#                inc(numlabels);
#                if numlabels>max_labels then prog_error(15,'');
#                k:=numlabels;
#               end;
#              labelname[k]:=s1;
#              labelnum [k]:=plen;
#             end;
#         else begin  (*  Instructions/Numbers  *)
#               check_plen(plen);
#               {-parse instruction-}
#               {-remove comments-}
#               k:=0;
#               for i:=length(s) downto 1 do
#                   if s[i]=';' then k:=i;
#               if k>0 then s:=lstr(s,k-1);
#               {-setup variables for parsing-}
#               k:=0; for j:=0 to max_op do pp[j]:='';
#               for j:=1 to length(s) do
#                begin
#                 c:=s[j];
#                 if (not (c in [' ',#8,#9,#10,','])) and (k<=max_op) then pp[k]:=pp[k]+c
#                    else if not (lc in [' ',#8,#9,#10,',']) then k:=k+1;
#                 lc:=c;
#                end;
#               parse1(n,plen,pp);
#               inc(plen);
#              end;
#        end;
#       end;
#     end;
#    close(f);
#    {-Add our implied NOP if theres room. This was originally to make sure
#      no one tries using an empty robot program, kinda pointless otherwise-}
#    if plen<=maxcode then
#     begin
#      for i:=0 to max_op do pp[i]:='';
#      pp[0]:='NOP';
#      parse1(n,plen,pp);
#     end
#    else
#     dec(plen); 


#    {--second pass, resolving !labels--}
#    if numlabels>0 then
#     for i:=0 to plen do
#      for j:=0 to max_op-1 do
#       if code[i].op[max_op] shr (j*4)=3 {unresolved !label} then
#        begin
#         k:=code[i].op[j];
#         if (k>0) and (k<=numlabels) then
#          begin
#           l:=labelnum[k];
#           if (l<0) then prog_error(19,'"!'+labelname[k]+'" ('+cstr(l)+')');
#           if (l<0) or (l>maxcode) then prog_error(18,'"!'+labelname[k]+'" ('+cstr(l)+')')
#            else
#             begin
#              code[i].op[j]:=l;
#              mask:=not($F shl (j*4));
#              code[i].op[max_op]:=(code[i].op[max_op] and mask) or (4 shl (j*4));
#                                   {resolved !label}
#             end;
#          end
#         else prog_error(17,cstr(k));
#        end;
#   end;
#  textcolor(7);
# end;


# needs review: how does this function actually access config.attribute?
def robot_config(n):
    if config.scanner == 5:
        robot[n].scanrange = 1500
    elif config.scanner == 4:
        robot[n].scanrange = 1000
    elif config.scanner == 3:
        robot[n].scanrange = 700
    elif config.scanner == 2:
        robot[n].scanrange = 500
    elif config.scanner == 1:
        robot[n].scanrange = 350
    else:
        robot[n].scanrange = 250
        
    if config.weapon == 5:
        robot[n].shotstrength = 1.5
    elif config.weapon == 4:
        robot[n].shotstrength = 1.35
    elif config.weapon == 3:
        robot[n].shotstrength = 1.2
    elif config.weapon == 2:
        robot[n].shotstrength = 1
    elif config.weapon == 1:
        robot[n].shotstrength = 0.8
    else:
        shotstrength = .5
        
    if config.armor == 5:
        robot[n].damageadj = 0.66
        robot[n].speedadj = 0.66
    elif config.armor == 4:
        robot[n].damageadj = 0.77
        robot[n].speedadj = 0.75
    elif config.armor == 3:
        robot[n].damageadj = 0.83
        robot[n].speedadj = 0.85
    elif config.armor == 2:
        robot[n].damageadj = 1
        robot[n].speedadj = 1
    elif config.armor == 1:
        robot[n].damageadj = 1.5
        robot[n].speedadj = 1.2
    else:
        robot[n].damageadj = 2
        robot[n].speedadj = 1.33
        
    if config.engine == 5:
        robot[n].speedadj = speedadj * 1.5
    elif config.engine == 4:
        robot[n].speedadj = speedadj * 1.35
    elif config.engine == 3:
        robot[n].speedadj = speedadj * 1.2
    elif config.engine == 2:
        robot[n].speedadj = speedadj * 1
    elif config.engine == 1:
        robot[n].speedadj = speedadj * 0.8
    else:
        robot[n].speedadj = speedadj * 0.5
            
        # heatsinks are handled seperately
        if config.mines == 5:
            robot[n].mines = 24
        elif config.mines == 4:
            robot[n].mines = 16
        elif config.mines == 3:
            robot[n].mines = 10
        elif config.mines == 2:
            robot[n].mines = 6
        elif config.mines == 1:
            robot[n].mines = 4
        else:
            mines = 2
            config.mines = 0
            
        robot[n].shields_up = False
        if (config.shield < 3) or (config.shield > 5):
            config.shield = 0
        if (config.heatsinks < 0) or (config.heatsinks > 5):
            config.heatsinks = 0
        
def reset_software(n):
    for r in robot:
        for i in range(0,max_ram):
            ram[i] = 0
            ram[71] = 768
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
            
# def reset_hardware(n):
# # def create_robot(n, filename):
# # def shutdown():
# # def delete_compile_report():
# # def write_compile_report():
# # def parse_param(s):
# # def init():

# def draw_robot(n): GRAPHICAL

# what on earth is ram[]?!?
def get_from_ram(n,i,j):
    for r in robot:
        if (i < 0) or (i > (max_ram + 1) + (((max_code + 1) << 3) - 1)):
            k = 0
            robot[n].robot_error(n,4,cstr(i))
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
        j = (robot[n].code[c].op[max_op] >> (4*o)) & 15
        i = robot[n].code[c].op[o]
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
        j = (robot[n].code[c].op[max_op] >> (4 * o)) & 15
        i = robot[n].code[c].op[o]
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

def init_missile(xx,yy,xxv,yyv,dir,s,blast,ob):
    k = -1
    # click() # global?
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
    if (n < 0) or (n > num_robots) or (robot[n].armor <= 0):
        sys.exit()
    if robot[n].config.shield < 3:
        robot[n].shields_up = false
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
                h = trunc(dd / 2.0)
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
   if debug_info: # is this a global?
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
     update_heat(n);
     init_missile(x,y,0,0,0,n,blast_circle,false)
     if overburn:
         m = 1.3
     else: m = 1
     for i in range(0,num_robots):
         if (i !> n) and (robot[i].armor > 0):
             k = round(distance(x, y, robot[i].x, robot[i].y))
             if k < blast_radius:
                 damage(i, round(abs(blast_radius - k) * m), False)

# def scan(n):
# def com_transmit(n,chan,data):
# def com_receive(n):
def in_port(n,p,time_used)
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
            j = round(distance(x,y,robot[i]^.x,robot[i]^.y))
            if (n != i) and (j < k) and (robot[i].armor > 0):
                k = j
                nn = i
            v = k
            if nn in range(0,num_robots):
                ram[5] = robot[robot[n].nn].transponder
    if p == 10:
        v = random.randint(0,65535) + random.randint(0,2)
    if p == 16:
        nn = -1
        if show_arcs:
            sonar_count = 2 # what is this??
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
                    v = minint # ?!?
        if robot[n].nn in range(0,num_robots):
            ram[5] = robot[robot[n].nn].transponder
    if p == 17:
        v = scanarc # what is this??
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
        if config.mines >= 0:
            k = 0
            for i in range(0, max_mines):
                if (mine[i].x >= 0) and (mine[i].x <= 1000) and (mine[i].y >= 0) and (mine[i].y <= 1000) and (mine[i].yield > 0):
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
            robot[n].shields_up = false
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
        if v = 0:
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
            if v = 0:
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
        ram[69] = round(robot[n].x)
        ram[70] = round(robot[n].y)
    if int_num == 3:
        time_used = 2
        if ram[65] == 0:
            robot[n].keepshift = False
        else:
            robot[n].keepshift = True
        ram[70] = robot[n].shift & 255
    if int_num == 4
        if ram[65] == 0:
            robot[n].overburn = False
        else:
            robot[n].overburn = True
    if int_num == 5:
        time_used = 2
        ram[70] = robot[n].transponder
    if int_num == 6:
        time_used = 2
        ram[69] = game_cycle >> 16
        ram[70] = game_cycle & 65535
    if int_num == 7:
        j = ram[69]
        k = ram[70]
        if j < 0:
            j = 0
        if j > 1000:
            j = 1000
        if k < 0:
            k = 0
        if k > 1000:
            k = 1000
        ram[65] = round(find_angle(round(robot[n].x), round(robot[n].y),j,k) / math.pi * 128 + 256) & 255
        time_used = 32
    if int_num == 8:
        ram[70] = ram[5]
        time_used = 1
    if int_num == 9:
        ram[69] = ram[6]
        ram[70] = ram[7]
        time_used = 2
    if int_num == 10
        k = 0
        for i in range(0,num_robots):
            if robot[i].armor > 0:
                k += 1
        ram[68] = k
        ram[69] = played
        ram[70] = matches
        time_used = 4
    if int_num == 11
        ram[68] = round(robot[n].speed * 100)
        ram[69] = robot[n].last_damage
        ram[70] = robot[n].last_hit
        time_used = 5
    if int_num == 12:
        ram[70] = ram[8]
        time_used = 1
    if int_num == 13:
        ram[8] = 0
        time_used = 1
    if int_num == 14:
        com_transmit(n, Robot[n].channel, ram[65])
        time_used = 1
    if int_num == 15:
        if ram[10] != ram[11]:
            ram[70] = com_receive(n)
        else:
            robot_error(n,12,'')
        time_used = 1
    if int_num == 16:
        if (ram[11] >= ram[10]):
            ram[70]:=ram[11]-ram[10]
        else:
            ram[70] = max_queue + 1 - ram[10] + ram[11]
        time_used = 1
    if int_num == 17:
        ram[10] = 0
        ram[11] = 0
        time_used = 1
    if int_num == 18:
        ram[68] = robot[n].kills
        ram[69] = robot[n].kills - robot[n].startkills
        ram[70] = robot[n].deaths
        time_used = 3
    if int_num == 19:
        ram[9] = 0
        robot[n].meters = 0
    else:
        robot_error(n,10,cstr(int_num))

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
def bout():
    # if quit then exit;
    played += 1
    init_bout()
    bout_over = False
    if step_mode = 0:
        then step_loop = False
    else:
        step_loop = True
    step_count = -1
    if graphix and (step_mode > 0):
        for i in range(0,num_robots):
            draw_robot(i)
    while not _quit and not gameover and not bout_over:
        game_cycle += 1
        for i in range(0,num_robots):
            if robot[i].armor > 0:
                do_robot(i)
        for i in range(0,max_missiles):
            if missile[i].a > 0:
                do_missile(i)
        for i in range(0,num_robots):
            for k in range(0,max_mines):
                if robot[i].mine[k]._yield > 0:
                    do_mine(i,k)
                
        if graphix and timing:
            time_delay(game_delay)

        if keypressed:
            c = readkey.upper()
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
                    game_delay = 05
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
            process_keypress(c);

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
            if ((game_cycle % k) = 0) or (game_cycle = 10):
                update_cycle_window()
            else:
                if (update_timer != mem[0:$46C] >> 1):
                    update_cycle_window()
            update_timer = mem[0:$46C] >> 1
            
    update_cycle_window()
    # Commented out in the original: {if (not graphix) then print;}
    score_robots()
    show_statistics()
    
# def write_report():
# def begin_window():
# def main():
