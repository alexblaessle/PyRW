import numpy as np
import time

center=np.array([0,0])

radius=35.

tol=0.000001

def bla(x):
        return np.sqrt(x[0]**2+x[1]**2)

def bla2(x):
        return np.sign(val)

def bla3(x):
        if x<0:
                return -1
        if x>0: 
                return 1
        if x==0:
                return 0

        
for i in range(100000):
        
        x=np.random.random(2)
        print type(x-center)
        raw_input()
        
        val=np.linalg.norm()-radius
       
        val2=bla(x-center)-radius
        
        val=bla2(val)
        
        val=bla3(val)
        
        
                