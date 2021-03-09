import pickle
import json
'''
1、通过pickle进行持久化存储的文件，
2、load进来时len（）可能会减少，但是不影响加载进来的数据。
'''
from pybloom_live import ScalableBloomFilter
bloom = ScalableBloomFilter()

old_data = ['a']
for i in range(1,10000):
    old_data.append('ww_{}'.format(i))
print(len(old_data))

for i in old_data:
    bloom.add(i)

f = open('pickle', 'wb')
pickle.dump(bloom,f)

f = open('pickle', 'rb')
pickle_data = pickle.load(f)
print(len(pickle_data))

print('b' not in pickle_data)
for i in range(1,1000):
    print('ww_{}'.format(i) not in pickle_data)

# filted_data = [i for i in updated_data if i not in bloom]
# print(filted_data)

class A():
    def __init__(self):
        self.f = open('pickle', 'rb')
        self.pickle_data = pickle.load(self.f)
        print(len(self.pickle_data))
        # exit()
    def updated(self):
        updated_data = ['ScalableBloomFilter object at 0x000001EA56F14C10>', 'wddwa',
                        'sefaf>a?F.?T.t33243./R.5435/754.?%74/.?v/./?w',
                        'sefaf>a?F.?T.t33243./R.5435/754.?%74/.?v/./?wwdwa','a','bbb','wwwwwdafaewr001']
        filted_data = [i for i in updated_data if i not in self.pickle_data]
        print(filted_data)
        self.pickle_updated(filted_data)

    def pickle_updated(self,data):
        f = open('pickle', 'wb')
        for i in data:
            self.pickle_data.add(i)
        pickle.dump(self.pickle_data, f)

if __name__ == '__main__':
    pass
    # a = A()
    # a.updated()