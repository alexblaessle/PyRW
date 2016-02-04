import numpy as np
import matplotlib.pyplot as plt

#Returns angle between two vertices around vcenter 
def angle_from_vertices(vcenter,vstart,vend,samedist=False):
	
	#Check if equal distant
	if samedist:
		if not dist(vend.x,vcenter.x)==dist(vstart.x,vcenter.x):
			print "Warning, |vcenter-vstart|!=|vcenter-vend|"
			return False
			
	#Compute vectors
	vec1=vstart.x-vcenter.x
	vec2=vend.x-vcenter.x
	
	#Compute angle
	angle=compute_angle(vec1,vec2)
	
	return angle

#Returns distance between two points
def dist(p1,p2):
	return  norm(p1-p2)

#Returns L2 norm of vector
def norm(vec):
	return np.linalg.norm(vec)

#Returns angle between two vectors		
def compute_angle(vec1,vec2):
		
	#Determine sign through atan2
	dv=vec1-vec2
	sign = np.arctan2(-dv[1],dv[0])

	if sign<0:
		sign=-1
	else:
		sign=1
	
	#Compute vector length
	l_vec1=norm(vec1)
	l_vec2=norm(vec2)
	
	#Compute dot product
	prod=np.dot(vec1,vec2)
	
	#Compute angle
	if l_vec1*l_vec2>0:
		if sign==1:
			angle=sign*np.arccos(prod/(l_vec1*l_vec2))
		elif sign==-1:	
			angle=2*np.pi+sign*np.arccos(prod/(l_vec1*l_vec2))
	else:
		#Make sure not to return NaN
		angle=0.
		
	return angle

def create_arc_curve(vcenter,angle,angle_offset,radius,steps=100):
	
	anglevec=np.linspace(angle_offset,angle_offset+angle,steps)
	
	xvec=vcenter.x[0]+radius*np.cos(anglevec)
	yvec=vcenter.x[1]+radius*np.sin(anglevec)
	
	return xvec, yvec

#Returns reduced 2D cross product
def cross2d(x1,x2):
	return float(x1[0]*x2[1]-x1[1]*x2[0])	

#Returns perpandicular vector
def perp(x):
	xp = np.empty_like(x)
	xp[0] = -x[1]
	xp[1] = x[0]
	return xp

#Returns outward perpandicular vector	
def outwPerp(x,c):
       
	xp = np.empty_like(x)
	xp[0] = -x[1]
	xp[1] = x[0]
	
	if np.dot(xp,c)>0:
                return xp
        else:
                return -xp

#Returns unit vector	
def unit_vector(vector):
	return vector / np.linalg.norm(vector)

#Returns directional vector
def direc_angle(v1,v2):
	v1_u = unit_vector(v1)
	v2_u = unit_vector(v2)
	angle = np.arccos(np.dot(v1_u, v2_u))
	if np.isnan(angle):
		if (v1_u == v2_u).all():
			return 0.0
		else:
			return np.pi
	return angle

#Returns true if coord is in poly
def checkInsidePoly(coord,poly):
	#Taken from http://www.ariel.com.au/a/python-point-int-poly.html
	n = len(poly)
	inside =False
	
	x=coord[0]
	y=coord[1]
	
	p1x,p1y = poly[0]
	for i in range(n+1):
		p2x,p2y = poly[i % n]
		if y > min(p1y,p2y):
			if y <= max(p1y,p2y):
				if x <= max(p1x,p2x):
					if p1y != p2y:
						xinters = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
					if p1x == p2x or x <= xinters:
						inside = not inside
		p1x,p1y = p2x,p2y
	
	return inside

def checkInsideCircle(x,center,radius,tol=1E-30,debug=False):
        val=np.linalg.norm(x-center)-radius
	if abs(val)<tol:
		return 0
	else:
                val=np.sign(val)
		return val

def combinations(arrays,out=None):
                
        #Convert all arrays to np arrays
        arrays = [np.asarray(x) for x in arrays]
        
        #Bring to same dtype
        dtype = arrays[0].dtype
        
        #Compute number of combinations
        n = np.prod([x.size for x in arrays])
        
        #Create output array if None is given
        if out is None:
                out = np.zeros([n, len(arrays)], dtype=dtype)
        
        #Compute size of repeats
        m = n / arrays[0].size
        out[:,0] = np.repeat(arrays[0], m)
        
        #Check if there is another array to go through
        if arrays[1:]:
                
                #Recursively call combinations again
                combinations(arrays[1:], out=out[0:m,1:])
                
                #Append results
                for j in xrange(1, arrays[0].size):
                        out[j*m:(j+1)*m,1:] = out[0:m,1:]
        
        return out
	
	
