import numpy as np
import RWessentials as rwe



x1=np.array([4,1])
x2=np.array([1,1])

center=np.array([0,0])

radius=5.

xstart=np.array([5,0])
xend=np.array([0,5])
	
print arc_intersect(x1,x2,xstart,xend,center,radius)


