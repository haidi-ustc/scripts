import numpy as np
from monty.serialization import loadfn
ret=loadfn('input.json')
s=ret["training"]['systems']

def get_batch_size(line):
   _tmp=int(line.split('u')[-1])
   return int(np.ceil(32/_tmp))

#select system  need  change !!!
t=[i for i in s if 'f3.0' in i] 
print(list(map(get_batch_size,t)),)
t=[i for i in s if 'equi' in i]
print(list(map(get_batch_size,t)),)
