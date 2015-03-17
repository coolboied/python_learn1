"""
from first_lesson import x

y = "kkkk"
print(x, y)

from imp import reload

k = "import first_lesson"
j = 'print("b")'
exec(k)
exec(j)

reload(first_lesson)

f = open('first_lesson.py')
print(f)
data = f.read()
print(data)
exec(data)

try :
	1/0
except Exception as ex:
	print(ex)
"""

"""
import math
a = str(3**3)
print(len(a))
print(math.sqrt(85),math.pi)

import random
print(random.random())
ran = [1,2,3,4,5,6,7]
rans = "mynameissquall"
print(random.choice(rans))
print(rans[2:5])
print(ran[2:5])
print(rans[:5])
print('he'+rans[2:])
b = rans.split('s')
print(rans,rans.upper(),b)
"""

"""
Squall={'name':'squall','age':26,'adress':'qingdao'}
print(Squall['name'])
Squall['job'] = 'dev'
Squall['job'] = ['dev','test']
Squall['job'].append('other')
Squall['job'].sort()
print(Squall)
Squall['job'].pop()
print(Squall)
for skey in Squall.keys():
	print(skey,Squall[skey])
"""

class human:
	def __init__(self,name, age):
		self.name = name
		self.age = age

gf = human('zwx',26)
print(gf.name)




