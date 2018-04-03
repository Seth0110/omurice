# ATR2 Test functions
# Date: 1-13-2018

import ATR2.py as A

'''
#CONSTANTS
progname       = 'AT-Robots'
version        = '2.11'
cnotice1       = 'Copyright 1997 ''99, Ed T. Toton III'
cnotice2       = 'All Rights Reserved.'
cnotice3       = 'Copyright 2014, William "Amos" Confer'
main_filename  = 'ATR2'
robot_ext      = '.AT2'
locked_ext     = '.ATL'
config_ext     = '.ATS'
compile_ext    = '.CMP'
report_ext     = '.REP'

_T             = True
_F             = False
minint         = -32768  # maxint=32787 is alrady defined by turbo pascal


# robots
max_robots     = 31    # starts at 0, so total is max_robots+1
max_code       = 1023  # same here
max_op         = 3     # etc...
stack_size     = 256
stack_base     = 768
max_ram        = 1023  # but this does start at 0 (odd #, 2^n-1)
max_vars       = 256
max_labels     = 256
acceleration   = 4
turn_rate      = 8
max_vel        = 4
max_missiles   = 1023
missile_spd    = 32
hit_range      = 14
blast_radius   = 25
crash_range    = 8
max_sonar      = 250
com_queue      = 512
max_queue      = 255
max_config_points= 12
max_mines      = 63
mine_blast     = 35

# simulator & graphics
screen_scale   = 0.46
screen_x       = 5
screen_y       = 5
robot_scale    = 06 # What is this?????? //ASK
default_delay  = 20
default_slice  = 05 # What is this?????? //ASK
mine_circle    = trunc(mine_blast*screen_scale)+1
blast_circle   = trunc(blast_radius*screen_scale)+1
mis_radius     = trunc(hit_range/2)+1
max_robot_lines = 8
#Gray50 : FillPatternType = ($AA, $55, $AA, $55, $AA, $55, $AA, $55) # //ASK

'''

# FUNCTIONS START!!!!!!

'''
def init_function_test():

    # Calls init()
    A.init()

    # Tests variables
    print("step_mode: " + step_mode)
    print("logging_errors: " + logging_errors)
    print("stats_mode: " + stats_mode)
    print("insane_missiles: " + insane_missiles)
    print("insanity: " + insanity)
    print("windoze: " + windoze)
    print("graphix: " + graphix)
    print("no_gfx: " + no_gfx)
    print("sound_on: " + sound_on)
    print("timing: " + timing)
    print("matches: " + matches)
    print("played: " + played)
    print("old_shields: " + old_shields)
    # print("quit: " + quit)      # Problem?????
    print("compile_only: " + compile_only)
    print("show_arcs: " + show_arcs)
    print("debug_info: " + debug_info)
    print("show_cnotice: " + show_cnotice)
    print("show_source: " + show_source)
    print("report: " + report)
    print("kill_count: " + kill_count)
    print("maxcode: " + maxcode)

    # Function calls
    
    #make_tables() # IS IN ATR2FUNC, CREATES the arrays that contain Sint and Cost values
    #randomize()  # NOt in any of the files for the game, must be in a library somewhere
    

    print("num_robots: " + num_robots)
    print("game_limit:" + game_limit)
    print("game_cycle: " + game_cycle)
    print("game_delay: " + game_delay)
    print("time_slice: " + time_slice)

    print("registered: " + registered)
    print("reg_name: " + reg_name)
    print("reg_num: " + reg_num)




def test_operand():



def test_mnemonic(n, m):
    a = A.mnemonic(n, m)
    print(a)
    print('alph')

    # b = A.mnemonic(1, 1)
    # print(b)

    if (a == 'NOP'):
        print('Pass')

    else:
        print('Fail')


test_mnemonic(00, 0)
'''


def test_max_shown():
    a = A.max_shown(1)
    b = A.max_shown(3)

    if a == 12 and b == 6:
        print('Pass')
    else:
        print('Fail')


test_max_shown()

'''


def test_log_error():   #Procedure



def test_graph_check():

def test_robot_graph():

def test_update_armor():

def test_update_heat():

def test_robot_error():

def test_update_lives():

def test_update_cycle_window():

def test_setscreen():

def test_graph_mode():

def test_prog_error():

def test_print_code():

def test_parse1():

def test_check_plen():

def test_compile():

def test_robot_config():

def test_reset_software():

def test_reset_hardware():

def test_init_robot():

def test_create_robot():

def test_shutdown():

def test_delete_compile_report():

def test_write_compile_report():

def test_parse_param():

def test_init():

def test_draw_robot():

def test_get_from_ram():

def test_get_val():

def test_put_val():

def test_push():

def test_pop():

def test_find_label():

def test_init_mine():

def test_count_missiles():

def test_init_missile():

def test_damage():

def test_scan():

def test_com_transmit():

def test_com_receive():

def test_in_port():

def test_out_port():

def test_call_int():

def test_jump():

def test_update_debug_bars():

def test_update_debug_system():

def test_update_debug_registers():

def test_update_debug_flags():

def test_update_debug_memory():

def test_update_debug_code():

def test_update_debug_window():

def test_init_debug_window():

def test_close_debug_window():

def test_gameover():

def test_toggle_graphix():

def test_invalid_microcode():

def test_process_keypress():

def test_execute_instruction():

def test_do_robot():

def test_do_mine():

def test_do_missile():

def test_victor_string():

def test_show_statistics():

def test_score_robots():

def test_init_bout():

def test_bout():

def test_write_report():

def test_begin_window():

def test_main():

'''
