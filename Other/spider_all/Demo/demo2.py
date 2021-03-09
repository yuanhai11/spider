
def loop():
    '''
    :param：wxt
    :keyword：none
    :return: 等腰三角形
    '''
    for i in range(1,11):
        for j in range(i-1):
            print(j,end='\t')
        print(i)


if __name__ == '__main__':
    loop()
