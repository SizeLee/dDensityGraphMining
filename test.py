import numpy as np
a = np.array([[1,2,3],[4,5,6],[7,8,9]])

b = a[:, [0, 2]][[0, 2], :]

b[0,0] = 100

print(b)
print(a)

b = list(range(0,8))
print(b[3])
del b[3]
print(b)
print(b[3])

def changeD(dic):
    dic['a'] = 0
    m = dic['M']
    m[0, :] = 1


d = dict()
d['a'] = 1
d['M'] = a

changeD(d)
print(d)
print(a)
# x = np.array([False])
# r = np.any([False, True, False, True])
# print(r)
# print(x)

b = dict()
b['a'] = 2
b['M'] = a.copy()

l = [b, d]
i=10
for each in l:
    each['M'][1,:] = i
    i +=1
print(b)
print(d)

l = list(range(10))
remainl = []
for i in l:
    if i<5:
        remainl.append(i)


print(l)
l = []
print(l==[])

l = [1,2,3]
lc = l.copy()
lc[0] = 100
print(l)
print(lc)

d = dict()
d[0] = 1
d[2] = 3
print(0 in d)

for i in range(1,2):
    print(i)
l.append(None)
print(l)
l.append(lc[-1])
print(l)
l[-1] = 3
print(set(lc))
print(set(l))
r = set(l).intersection(lc)
r = list(r)
print(r)

a = np.array([[1,2,3],[4,5,6],[7,8,9]])
b = np.array([[1,2,3],[4,5,6],[7,8,9]])
c = a*b
print(c)

a = list([1,2,3,4,5])
b = list([0,2,3])
print(b)
c = np.array(a)[b].tolist()
print(c)
d = list(c)
print(d)
d += c
print(d)
j = np.array([3,4,5])<np.array([1,5,4])
print(j)
print(np.any(j))
t = {}
if not t:
    print('a')

a = list([1,2,3,4,5])
b = list([1,2,3])
print(set(b).issubset(set(a)))

a = {1:{1:1},2:2}
b = a.copy()
b[1]=1
print(a)
print(b)
c = a.copy()
c[1][1]=2
print(a)
print(c)
del a[1]
print(a)
print(c)
print(a=={})
a = {1:{},2:{},3:{},4:{},5:{}}
print(len(a))
l = []
for eachkey in a:
    if a[eachkey] == {}:
        l.append(eachkey)

for eachkey in l:
    del a[eachkey]
print(a)

a = set()
a = a.union([1,2,3])
a = a.union([2,3,6,7])
print(a)
print(len(a))
b = list(a)
print(b)

for i in range(1,1):print(i)

a = [i for i in range(3,7)]
# a = a
for each in a:
    print(each)
# print(a)