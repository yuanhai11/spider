import random

def redpacket(cash, person):
    for i in range(1,person+1):
        if i == person:
            print('A' * i, round(cash,2))
        else:
            num = round(cash * random.random(),2)
            print('A'*i,num)
            cash-=num

redpacket(10,5)

