import ATR2FUNC

'''

def func_test_hexnum():  #Pass
    pass_fail = "Fail"

    num_1 = ATR2FUNC.hexnum(0)
    num_2 = ATR2FUNC.hexnum(8)
    num_3 = ATR2FUNC.hexnum(15)

    #print('step_1')
    if (num_1 == '0') & (num_2 == '8') & (num_3 == 'F'):
        pass_fail = "Pass"

    #print('step_2')
    print(pass_fail)


func_test_hexnum()


def func_test_hexb(): #Pass
    #print('step_1')
    a = ATR2FUNC.hexb(11)
    #print(a)

    #print('step_2')
    if a == '0B':
        print('Pass')
    else:
        print('Fail')


func_test_hexb()

'''
def func_test_hex():  #Fail
    print('step_1')
    a = ATR2FUNC.hex(10)
    print(a)

    print('step_2')
    if a == '0FA':
        print('Pass')
    else:
        print('Fail')


func_test_hex()

'''

def func_test_valuer():  #Pass
    a = ATR2FUNC.valuer("100")
    #print(a)

    if type(a) is int and a == 100:
        print('Pass')
    else:
        print('Fail')

func_test_valuer()



def func_test_value():  #Pass
    a = ATR2FUNC.value(1)
    #print(a)

    if a == 1:
        print('Pass')
    else:
        print('Fail')

func_test_value()


def func_test_cstrr():  #Pass
    a = ATR2FUNC.cstrr(1.1)
    #print(a)

    if type(a) is str and a == "1.1":
        print('Pass')
    else:
        print('Fail')

func_test_cstrr()


def func_test_cstr():  #Pass
    a = ATR2FUNC.cstr(1.1)
    #print(a)

    if type(a) is str and a == "1.1":
        print('Pass')
    else:
        print('Fail')

func_test_cstr()



def func_test_zero_pad():  #Pass
    s = ATR2FUNC.zero_pad(5, 10)
    #print(s)

    if type(s) is str and len(s) == 10:
        print('Pass')
    else:
        print('Fail')

func_test_zero_pad()



def func_test_zero_pads():  #Pass
    s = ATR2FUNC.zero_pads(5, 10)
    #print(s)

    if type(s) is str and len(s) == 10:
        print('Pass')
    else:
        print('Fail')

func_test_zero_pads()


def func_test_addfront():  #Pass
    s = ATR2FUNC.addfront('5', 10)
    #print(s)

    if type(s) is str and len(s) == 10:
        print('Pass')
    else:
        print('Fail')

func_test_addfront()


def func_test_addrear():  #Pass
    s = ATR2FUNC.addrear('5', 10)
    #print(s)

    if type(s) is str and len(s) == 10:
        print('Pass')
    else:
        print('Fail')

func_test_addrear()


def func_test_ucase():  #Pass
    s = ATR2FUNC.ucase('a')
    #print(s)

    if type(s) is str and s.isupper():
        print('Pass')
    else:
        print('Fail')

func_test_ucase()


def func_test_lcase(): #Pass
    s = ATR2FUNC.lcase('a')
    #print(s)

    if type(s) is str and s.islower():
        print('Pass')
    else:
        print('Fail')

func_test_lcase()


def func_test_space():  #Pass
    s = ATR2FUNC.space(10)
    #print(s)

    if type(s) is str and len(s) == 10:
        print('Pass')
    else:
        print('Fail')

func_test_space()


def func_test_repchar(): #Pass
    s = ATR2FUNC.repchar('a', 5)
    #print(s)

    if type(s) is str and len(s) == 5:
        print('Pass')
    else:
        print('Fail')

func_test_repchar()


def func_test_ltrim():  #Pass
    s = ATR2FUNC.ltrim('12345')
    #print(s)

    if type(s) is str and s == '2345':
        print('Pass')
    else:
        print('Fail')

func_test_ltrim()


def func_test_rtrim():  #Pass
    s = ATR2FUNC.rtrim('12345')
    #print(s)

    if type(s) is str and s == '1234':
        print('Pass')
    else:
        print('Fail')

func_test_rtrim()


def func_test_btrim():  #Pass
    s = ATR2FUNC.btrim('12345')
    #print(s)

    if type(s) is str and s == '234':
        print('Pass')
    else:
        print('Fail')

func_test_btrim()


def func_test_lstr(): #Pass
    s = ATR2FUNC.lstr('12345', 3)
    #print(s)

    s1 = ATR2FUNC.lstr('1', 3)
    #print(s1)

    if type(s) is str and s == '123' and s1 == s1:
        print('Pass')
    else:
        print('Fail')

func_test_lstr()


def func_test_rstr():  #Pass
    s = ATR2FUNC.rstr('12345', 3)
    #print(s)

    s1 = ATR2FUNC.rstr('1', 3)
    #print(s1)

    if type(s) is str and s == '345' and s1 == s1:
        print('Pass')
    else:
        print('Fail')

func_test_rstr()


def func_test_check_registration(): #Not Finished
    a = ATR2FUNC.check_registration()

    #print(a)
    
func_test_check_registration()


def func_test_rol(): #Pass
    #print(ATR2FUNC._bin(10))

    a = ATR2FUNC.rol(10, 1)
    #print(a)
    #print(type(a))

    if a == '0000000000010100':
        print('Pass')
    else:
        print('Fail')

func_test_rol()


def func_test_ror():  #Pass
    #print(ATR2FUNC._bin(10))
    a = ATR2FUNC.ror(10, 1)

    #print(a)

    if type(a) == str and a == '0000000000000101':
        print('Pass')
    else:
        print('Fail')

func_test_ror()


def func_test_sal():  #Pass
    #print(ATR2FUNC._bin(10))
    a = ATR2FUNC.sal(10, 1)

    #print(a)

    if type(a) == str and a == '0000000000010100':
        print('Pass')
    else:
        print('Fail')

func_test_sal()


def func_test_sar():  #Pass
    #print(ATR2FUNC._bin(10))
    a = ATR2FUNC.sar(10, 1)

    #print(a)

    if type(a) == str and a == '0000000000000101':
        print('Pass')
    else:
        print('Fail')

func_test_sar()


def func_test_make_tables():  #Fail
    sint = ()
    cost = ()
    ATR2FUNC.make_tables()

    if sint[1] == math.sin(i/128*math.pi):
        print('Pass')
    else:
        print('Fail')

func_test_make_tables()


def func_test_robot_color():  #Pass
    a = ATR2FUNC.robot_color(27)
    #print(a)

    if a == 15:
        print('Pass')
    else:
        print('Fail')

func_test_robot_color()


def func_test_hex2int():
    a3 = ATR2FUNC.hex2int('5')
    #print(a3)

    a2 = ATR2FUNC.hex2int('C8')
    #print(a2)

    a1 = ATR2FUNC.hex2int('1')
    #print(a1)

    if a3 == 5 and a2 == 200 and a1 == 1:
        print('Pass')
    else:
        print('Fail')

func_test_hex2int()



def func_test_str2int():
    a = ATR2FUNC.str2int("")

'''