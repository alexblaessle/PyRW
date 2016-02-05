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

from numpy import *
import RWessentials as rwe

class BC(object):
	
	#Init
	def __init__(self,w,typ,Id,edge,direcBehaviour):
		self.walker=w
		self.typ=typ
		self.Id=Id
		self.edge=edge
		self.direcBehaviour=direcBehaviour
		
	
	
	#Return intersection of last path with polgygon
	def findIntersectPoly(self,xold,xnew,poly):
		
		for i in range(len(poly)):
			p1 = poly[i]
			p2 = poly[mod(i+1,len(poly))]
			
			x_intersect=self.segIntersect(xold,xnew,p1.x,p2.x)
		
			if bool(len(shape(x_intersect))):
				return x_intersect
			
	#Returns perpandicular vector	
	def perp(self,x):
		xp = rwe.perp(x)
		return xp
	
	#Returns reduced 2D cross product
	def cross2d(self,x1,x2):
		return rwe.cross2d(x1,x2)
		
	#Checks if two line segments are intersecting, if they do, return intersection, else return false
	def segIntersect(self,x1,x2,y1,y2,debug=False):
		#Taken from http://stackoverflow.com/questions/563198/how-do-you-detect-where-two-line-segments-intersect
		#r=dx=x2-x1
		#s=dy=y2-y1
		#p=x1
		#q=y1
		
		#Compute slopes
		dx = x2-x1
		dy = y2-y1
		
		#Some debugging messages
		if debug:
			print "0<=", dot(y1-x1,dx), "<=", dot(dx,dx)
			print "0<=", dot(x1-y1,dy) , "<=",  dot(dy,dy)
			
			print "dot(y1-x1,dx)<0",dot(y1-x1,dx)<0
			print "dot(dx,dx)<dot(y1-x1,dx)", dot(dx,dx)<dot(y1-x1,dx)
			print "dot(x1-y1,dy)<0", dot(x1-y1,dy)<0
			print "dot(dy,dy)<dot(x1-y1,dy)", dot(dy,dy)<dot(x1-y1,dy)
		
		#Check for colinearity
		if self.cross2d(dx,dy)==0 and self.cross2d(x1-y1,dx)==0:
			#two lines are colinear
			if debug:
				print "colinear"
			
			if (dot(y1-x1,dx)>=0 and dot(dx,dx)>=dot(y1-x1,dx)) or (dot(x1-y1,dy)>=0 and dot(dy,dy)>=dot(x1-y1,dy)):
				#two lines are overlapping
				if debug:
					print "overlapping"
			
			if ((dot(y1-x1,dx)<0 or dot(dx,dx)<dot(y1-x1,dx)) and (dot(x1-y1,dy)<0 or dot(dy,dy)<dot(x1-y1,dy))):
				if debug:
					print "disjoint"
			# so RW moved along boundary. Return new x
			return x2
		
		#Check if parallel
		elif (self.cross2d(dx,dy)==0 and self.cross2d(x1-y1,dx)):
			if debug:
				print "parallel"
		
			#two lines are parallel, return False
			return False,False
		
		#Check if intersect possible
		elif self.cross2d(dx,dy)!=0:
			
			#Compute scaling factors
			u = self.cross2d(y1-x1,dx)/self.cross2d(dx,dy)
			t = self.cross2d(x1-y1,dy)/self.cross2d(dy,dx)
			
			#Check if intersect
			if (0<=t and t<=1) and (0<=u and u<=1):
			
				if debug:
					print "intersect"
				x2 = x1+t*dx
				return x2
			
			else:
				if debug:
					print "not parallel, not intersect"
				return False,False
	
	def circCheck(self,x,center,radius,tol=1E-30,debug=False):
                return rwe.checkInsideCircle(x,center,radius,tol=tol,debug=debug)
               
        def arcPreChecks(self,x1,x2,arc,tol=1E-30,breakAtProblem=False,debug=False):
		
		#Debugging message
		if debug:
			print "==========================="
			print "x1 = ", x1
			print "x2 = ", x2
				
		#Check if x1 or x2 is out of arc
		x1out=0
		x2out=0
		if self.circCheck(x1,arc.vcenter.x,arc.radius,tol=tol)==1:
			x1out=1	
		if self.circCheck(x2,arc.vcenter.x,arc.radius,tol=tol)==1:
			x2out=1
		
		#Debugging messages
		if debug:
			if x1out==1:
				print "x1 is out"
			if x2out==1:
				print "x2 is out"

		#Break if there is a problem
		if breakAtProblem:
			if x1out==1:
				raw_input()        
			
		#Need to check if xold is on arc, but trajectory is not passing through arc
		#(this is especially important for sticky BC)
		if self.circCheck(x1,arc.vcenter.x,arc.radius)==0:
			if self.circCheck(x2,arc.vcenter.x,arc.radius)<0:
				if debug:
					print "x1 on boundary, but x2 inside, returning False"
				return False
			
		return True
        
        def checkArcIntersect(self,x1,x2,arc,tol=1E-30,spacer=1E-5,breakAtProblem=False,preCheck=True,debug=False):
		
		#Do some prechecks
		if preCheck:
			pre=self.arcPreChecks(x1,x2,arc,tol=tol,breakAtProblem=breakAtProblem,debug=debug)
		else:
			pre=True
		
		#Compute vectors
		d=x2-x1
		f=x1-arc.vcenter.x
		
		#Compute polynomial coeffcients
		a = dot(d,d) 
		b = 2*dot(f,d) 
		c = dot(f,f) - arc.radius**2 
		
		#discriminant
		discriminant = b*b-4*a*c
		
		if not pre:
			return False,discriminant,a,b
		
		#Debugging message
		if debug:
                        print "discriminant coeffcients:"
                        print "a = ", a
                        print "b = ", b
                        print "c = ", c
                        print "discriminant = ",discriminant
		
		inter=False
		
		#Check discriminant
		if discriminant < 0:
			if debug:
                                print "discriminant < 0 => returning False"
			return False,discriminant,a,b
		else:
			return True,discriminant,a,b
	
	def arcIntersect(self,x1,x2,arc,tol=1E-30,spacer=1E-5,breakAtProblem=False,debug=False):
		
		#Check if there is an intersection
		inter,discriminant,a,b=self.checkArcIntersect(x1,x2,arc,tol=tol,breakAtProblem=breakAtProblem,debug=debug)
		
		if inter:
			xinterc=self.computeArcIntersect(x1,x2,arc,a,b,discriminant,spacer=spacer,debug=debug)
		else:
			return False,False
			
		return xinterc
		
	def computeArcIntersect(self,x1,x2,arc,a,b,discriminant,spacer=1E-5,debug=False):
		
		discriminant = sqrt(discriminant)
		
		#Compute interception scaling
		t1 = (-b - discriminant)/(2*a)
		t2 = (-b + discriminant)/(2*a)
		
		#Debugging message
		if debug:
			print "t1 = ", t1
			print "t2 = ", t2
		
		#Compute possible intersection points
		xinter1=x1+(t1-spacer)*(x2-x1)
		xinter2=x1+(t2-spacer)*(x2-x1)
		
		#Debugging message
		if debug:
			print "xinter1 = ",xinter1
			print "xinter2 = ", xinter2
			print "angle1 = ", arc.inArc(xinter1,debug=True)
			print "angle2 = ", arc.inArc(xinter2,debug=True)
			
		#Check which intersection is the actual one (t1/t2)
		if t1 >= 0 and t1 <= 1: 
			if debug:
				print "intersection due to t1"
			
			if arc.inArc(xinter1):
				if debug:
					print "Returning xinter1 = ", xinter1
				return xinter1
			
		if t2 >= 0 and t2 <= 1:
			if debug:
				print "intersection due to t2"
			
			if arc.inArc(xinter2):
				if debug:
					print "Returning xinter2 = ", xinter2    
				return xinter2
				
		if debug:
			print "xinter1 and xinter2 do not lie on arc, returning False"
			
		return False,False
	
	
class sticky(BC):
	
	#Init
	def __init__(self,w,Id,edge,direcBehaviour=1):
		super(sticky, self).__init__(w,0,Id,edge,direcBehaviour)
		
	def hit(self,xold,xnew,debug=False):
		
		if self.edge.typ==0:	
			xinterc=self.segIntersect(xold,xnew,self.edge.v1.x,self.edge.v2.x)
		elif self.edge.typ==1:
                        xinterc=self.arcIntersect(xold,xnew,self.edge,debug=True)
		  
		if xinterc[0]==False:
			xinterc=xnew
                else:
                        pass
                
		return xinterc
		
class setBack(BC):
        
        #Init
	def __init__(self,w,Id,edge,direcBehaviour=1):
		super(setBack, self).__init__(w,1,Id,edge,direcBehaviour)
		
	def hit(self,xold,xnew,breakAtProblem=False,debug=False):
              
                if self.edge.domain.typ=='circle':
			xinterc=self.circleHit(xold,xnew,breakAtProblem=breakAtProblem,debug=debug)
		else:
			if self.edge.typ==0:	
				xinterc=self.segIntersect(xold,xnew,self.edge.v1.x,self.edge.v2.x)
			elif self.edge.typ==1:
				
				#For setBack we do not care about the exact intercep
				xinterc=self.checkArcIntersect(xold,xnew,self.edge,breakAtProblem=breakAtProblem,debug=debug)
				
			if xinterc[0]==False:
				xinterc=xnew
			else:
				xinterc=xold
			
			if direcBehaviour==0:
				self.walker.d=None
			elif direcBehaviour==1:
				self.walker.d=mod(self.walker.d+pi,2*pi)
			
                return xinterc
	
	def circleHit(self,xold,xnew,breakAtProblem=False,debug=False):
	
		if self.edge.domain.typ!='circle':
			if debug:
				print "Warning, geometry is not circle!"
		
		if self.circCheck(xold,self.edge.vcenter.x,self.edge.radius,tol=0.)>=0:
			if debug:
				print "Warning, xold is out or on of circle!"
				if breakAtProblem:
					raw_input()
		
		if self.direcBehaviour==0:
			self.walker.d=None
		elif self.direcBehaviour==1:
			self.walker.d=mod(self.walker.d+pi,2*pi)			
		
		if self.circCheck(xnew,self.edge.vcenter.x,self.edge.radius,tol=0.)>=0:
			return xold
		else:
			return xnew
			
		
		
		
                
	
	
#def absorb(BC):

#def reflect(BC):
	
#def randomReflect(BC):
	