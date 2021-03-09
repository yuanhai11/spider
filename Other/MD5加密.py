import hashlib
'''
update时 如果不定义新的hash对象，被加密的字符串，默认会进行字符串拼接，从而得到错误数据
'''

def main(str):
    for st in str:
        m = hashlib.md5()
        m.update(st.encode(encoding='utf-8'))
        result = m.hexdigest()
        print(result)
        print(len(result))

from Other.post_es import get_company_id
Id = get_company_id('杭州古北智能制造有限公司')
print(Id)

if __name__ == '__main__':
    str = ['a','b','c']
    main(str)