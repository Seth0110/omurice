import ATR2

def test():
    for i in range(0, 1):
        for k in range(0, 10000):
            a = ATR2.operand(i, k)

            if a != ("["+str(i)+"]"):
                print("{"+str(i)+","+str(k)+"} = " + a)

test()
