#===========================================================================
#License
#===========================================================================

#Copyright (C) 2016 Alexander Blaessle
#This software is distributed under the terms of the GNU General Public License.

#This file is part of PyRW.

#PyRW is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.

#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.

#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>.

#===========================================================================
#Importing necessary modules
#===========================================================================

#Numpy
import numpy as np

#Matplotlib
import matplotlib.pyplot as plt

#===========================================================================
#Module description
#===========================================================================

#Module with essential functions for pyrw, including the following functions:

#(1) angle_from_vertices
#(2) dist
#(3) norm
#(4) compute_angle
#(5) create_arc_curve
#(6) cross2d
#(7) perp
#(8) outwPerp
#(9) cross2d
#(11) unit_vector
#(12) direc_angle
#(13) checkInsidePoly
#(14) checkInsideCircle
#(15) combinations

#===========================================================================
#Module functions
#===========================================================================


def angle_from_vertices(vcenter,vstart,vend,samedist=False):
	

	"""Returns angle between two vertices around vcenter.

	:param vcenter:  Vertex object.
	:type vcenter: pyrw.geometry.vertex
	:param vstart:  Vertex object.
	:type vstart: pyrw.geometry.vertex
	:param vend:  Vertex object.
	:type vend: pyrw.geometry.vertex
	:param samedist:  Flag if vectors need to have same length.
	:type samedist: bool
	:returns: float -- angle
	"""

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


def dist(p1,p2):
	
	"""Returns euclidean distance between two points.

	:param p1:  Point 1.
	:type p1: array
	:param p2:  Point 2.
	:type p2: array
	
	:returns: float -- distance
	"""
	
	return  norm(p1-p2)


def norm(vec):
	
	"""Returns L2-norm of vector.

	:param vec:  Vector.
	:type vec: array
	:returns: float -- length of vector
	"""
	
	return np.linalg.norm(vec)

		
def compute_angle(vec1,vec2):
		
	"""Returns angle between two vectors.

	:param vec1:  Vector.
	:type vec1: array
	:param vec2:  Vector.
	:type vec2: array
	:returns: float -- angle
	"""	
		
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
	
	"""Creates array with points describing the curve of an arc.

	:param vcenter:  Vertex object.
	:type vcenter: pyrw.geometry.vertex
	:param angle:  Angle of arc.
	:type angle: float
	:param angle_offset:  Offset angle of arc.
	:type angle_offset: float
	:param radius:  radius of arc.
	:type radius: float
	:param steps:  number of steps for arc.
	:type steps: int
	
	:returns: (array,array) -- vectors describing x/y-coordinates
	"""
	
	anglevec=np.linspace(angle_offset,angle_offset+angle,steps)
	
	xvec=vcenter.x[0]+radius*np.cos(anglevec)
	yvec=vcenter.x[1]+radius*np.sin(anglevec)
	
	return xvec, yvec

def cross2d(x1,x2):
	
	"""Returns reduced 2D cross product.

	:param x1:  Coordinate 1.
	:type x1: array
	:param x2:  Coordinate 2.
	:type x2: array
	
	:returns: float -- cross product
	"""
	
	return float(x1[0]*x2[1]-x1[1]*x2[0])	

def perp(x):
	
	"""Returns perpendicular vector.

	:param x:  Vector.
	:type x: array
	
	:returns: array -- perpendicular vector
	"""
	
	xp = np.empty_like(x)
	xp[0] = -x[1]
	xp[1] = x[0]
	return xp

def outwPerp(x,c):
       
	"""Returns outward perpendicular vector.

	:param x:  Vector.
	:type x: array
	:param c:  Center coordinate.
	:type c: array
	
	:returns: array -- perpendicular vector
	"""
	
	xp = np.empty_like(x)
	xp[0] = -x[1]
	xp[1] = x[0]
	
	if np.dot(xp,c)>0:
                return xp
        else:
                return -xp


def unit_vector(vector):
	
	"""Returns unit vector.

	:param vector:  Vector.
	:type vector: array
	
	:returns: array -- unit vector
	"""
	
	return vector / np.linalg.norm(vector)


def direc_angle(v1,v2):
	
	"""Returns directional angle.

	:param v1:  Vector.
	:type v1: array
	:param v2:  Vector.
	:type v2: array
	
	:returns: array -- directional angle
	"""
	
	v1_u = unit_vector(v1)
	v2_u = unit_vector(v2)
	angle = np.arccos(np.dot(v1_u, v2_u))
	if np.isnan(angle):
		if (v1_u == v2_u).all():
			return 0.0
		else:
			return np.pi
	return angle

def checkInsidePoly(coord,poly):
	
	"""Returns True if coord is inside poly.
	
	Taken from http://www.ariel.com.au/a/python-point-int-poly.html
	
	:param coord:  Coordinate.
	:type coord: array
	:param poly:  Polygon corners.
	:type poly: list
	
	:returns: bool -- True if inside
	"""
	
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
	
	"""Returns True if x is inside circle.
	
	:param x:  Coordinate.
	:type x: array
	:param center:  Coordinate of center.
	:type center: array
	:param radius:  Radius of circle.
	:type radius: float
	:param center:  Tolerance added to check to avoid rounding errors.
	:type center: float
	:param debug:  Debugging flag.
	:type debug: bool
	
	
	:returns: bool -- True if inside
	"""
	
        val=np.linalg.norm(x-center)-radius
	if abs(val)<tol:
		return 0
	else:
                val=np.sign(val)
		return val

def combinations(arrays,out=None):
        
        """Returns cartesian product of arrays.
	
	:param arrays:  List of arrays.
	:type arrays: list
	:param out: Result vector.
	:type out: array
	
	:returns: array -- Cartesian product
	"""
        
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
	
	
