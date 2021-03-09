
sum = [1,5]
print_data = []
for i in range(10,1000):
    num = str(i)
    if len(num) == 2:
        gewei = int(num)%10
        shiwei = int(num)//10
        if gewei in sum or shiwei in sum:
            print_data.append(i)
    elif len(num) ==3:
        gewei = int(num) % 10
        shiwei = int(num) // 10 % 10
        baiwei = int(num) // 100
        if gewei in sum or shiwei in sum or baiwei in sum:
            print_data.append(i)
num = 0
for i in print_data:
    if num == 20:
        print()
        print(i,end='\t')
        num = 0
    else:
        print(i,end='\t')
    num+=1
