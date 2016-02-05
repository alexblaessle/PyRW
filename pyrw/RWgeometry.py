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

#PyRW modules
import RWessentials as rwe

#Numpy
import numpy as np

#Matplotlib
import matplotlib.pyplot as plt

#===========================================================================
#Module description
#===========================================================================

#Geometry module of pyrw containing classes for defining the 2D geometry of 
#the domain for random walkers, including the following classes:

#(1) vertex
#(2) edge
#(3) line
#(4) arc
#(5) circe
#(6) rectangle

#===========================================================================
#Module classes
#===========================================================================

class vertex:
	
	"""Vertex class for defining domain geometry.

	:param domain:  A pyrw domain.
	:type domain: pyrw.RWdomain
	:param x: A coordinate, e.g. [0,1].
	:type x: array
	:param Id: ID of vertex.
	:type Id: int
	
	"""
	
	def __init__(self,domain,x,Id):
		
		self.domain=domain
		
		self.x=np.array(x)
		self.Id=Id
				
	def draw(self,r=None,color=None,ann=False):
		
		"""Draw vertex
		
		:param r: pyrw run, if None, picks last run of main pyrw.RWRW object. 
		:type r: pyrw.RWrun object
		:param color: color of vertex in matplotlib syntax, e.g. 'r' or (0.1,1,0.5)
		:type color: matplotlib color
		:param ann: Annotation Flag
		:type ann: bool
		
		"""
		
		if ann==None:
			ann=False
		
		
		if r==None:
			r=self.domain.RW.runs[-1]
		
		if not hasattr(r,'fig_traj'):
			r.fig_traj=plt.figure()
			r.ax_traj=r.fig_traj.add_subplot(111)
			r.fig_traj.show()
		
		r.ax_traj.plot(self.x[0],self.x[1],color=color,marker=".")
		if ann:
			r.ax_traj.annotate('v'+str(self.Id), xy=(self.x[0], self.x[1]),xytext=(self.x[0]+0.5, self.x[1]+0.5),)
		plt.draw()
		
	def setX(self,x):
		"""Define vertex location
		
		:param x: A coordinate, e.g. [0,1]
		:type x: array
		
		"""
		self.x=x

class edge:
	
	"""Edge class for defining domain geometry.

	:param domain:  A pyrw domain.
	:type domain: pyrw.RWdomain
	:param Id: ID of edge.
	:type Id: int
	:param typ: Edge type
	:type typ: int
	
	"""
	
	def __init__(self,domain,Id,typ):
		self.domain=domain
		self.Id=Id
		self.typ=typ
		
	def getDomain(self):
		return self.domain
	
	def getId(self):
		return self.Id
	
	def getTyp(self):
		return self.typ
	
	def decodeTyp(self):
		
		"""Returns type of edge in words.
		
		:returns: str -- type of the edge
		"""
		
		if typ==1:
			return "arc"
		elif typ==0:
			return "line"
	
class line(edge):
	
	"""Line class for defining domain geometry.

	:param domain:  A pyrw domain.
	:type domain: pyrw.RWdomain
	:param Id: ID of line.
	:type Id: int
	:param v1: Start vertex of the line.
	:type v1: pyrw.RWgeometry.vertex
	:param v2: Second vertex of the line.
	:type v2: pyrw.RWgeometry.vertex
	
	"""
	
	def __init__(self,domain,v1,v2,Id):
		
		edge.__init__(self,domain,Id,0)

		self.v1=v1
		self.v2=v2
	
		
	def draw(self,r=None,color=None,ann=False):
		
		"""Draw line
		
		:param r: pyrw run, if None, picks last run of main pyrw.RWRW object. 
		:type r: pyrw.RWrun
		:param color: color of line in matplotlib syntax, e.g. 'r' or (0.1,1,0.5)
		:type color: matplotlib color
		:param ann: Annotation Flag
		:type ann: bool
		
		"""
		
		if ann==None:
			ann=False
		
		
		if r==None:
			r=self.domain.RW.runs[-1]
		
		if not hasattr(r,'fig_traj'):
			r.fig_traj=plt.figure()
			r.ax_traj=r.fig_traj.add_subplot(111)
			r.fig_traj.show()
		
		r.ax_traj.plot([self.v1.x[0],self.v2.x[0]],[self.v1.x[1],self.v2.x[1]],color=color,linestyle='-')
		if ann:
			
			r.ax_traj.annotate('e'+str(self.Id), xytext=((self.v2.x[0]+self.v1.x[0])/2., (self.v2.x[1]+self.v1.x[1])/2.+0.5),xy=(self.v1.x[0]+0.5, self.v1.x[1]+0.5),)
		
		plt.draw()

class arc(edge):
	
	"""Arc class for defining domain geometry.

	:param domain:  A pyrw domain.
	:type domain: pyrw.RWdomain
	:param vstart: Start vertex of the arc.
	:type vstart: pyrw.RWgeometry.vertex
	:param vcenter: Center vertex of the arc.
	:type vcenter: pyrw.RWgeometry.vertex
	:param Id: ID of arc.
	:type Id: int
	:param vend: Second vertex of the arc.
	:type vend: pyrw.RWgeometry.vertex
	:param angle: Angle of arc.
	:type angle: float
	
	"""
	
	def __init__(self,domain,vstart,vcenter,Id,vend=None,angle=None):
		
		edge.__init__(self,domain,Id,1)
		
		self.vcenter=vcenter
		self.vstart=vstart
		self.vend=None
		self.angle=None
		self.radius=None
		
		#Check input
		
		#3 points given, check if they have the right distance
		if vend!=None and vcenter!=None and angle==None:
			self.genFromPoints(vcenter,vstart,vend)
				
		#2 points and angle given
		elif angle!=None and vcenter!=None and vend==None:
			self.genFromAngle(vcenter,vstart,angle)
			
		#3 points and angle given, then try use angle way
		elif angle!=None and vcenter!=None and vend!=None:
			print "Warning: Given angle and vend, will use angle version to initialize arc with arc id ", self.Id
			self.genFromAngle(vcenter,vstart,angle)
			
			
	def genFromPoints(self,vcenter,vstart,vend):
		
		""" Initializes arc if vend was given at initialization
		
		:param vstart: Start vertex of the arc.
		:type vstart: pyrw.RWgeometry.vertex
		:param vcenter: Center vertex of the arc.
		:type vcenter: pyrw.RWgeometry.vertex
		:param vend: Second vertex of the arc.
		:type vend: pyrw.RWgeometry.vertex
		
		"""
		
		if np.linalg.norm(vend.x-vcenter.x)==np.linalg.norm(vstart.x-vcenter.x):
				
			self.vcenter=vcenter
			self.vstart=vstart
			self.vend=vend
			
			#Compute angle and radius
			self.computeRadius()	
			self.computeAngle()
			
		else:
			print "Warning, |vcenter-vstart|!=|vcenter-vend|. Will not initialize arc ", self.Id ," properly"
		
	def genFromAngle(self,vcenter,vstart,angle):
		
		""" Initializes arc if angle was given at initialization
		
		:param vstart: Start vertex of the arc.
		:type vstart: pyrw.RWgeometry.vertex
		:param vcenter: Center vertex of the arc.
		:type vcenter: pyrw.RWgeometry.vertex
		:param angle: Angle of arc.
		:type angle: float
		
		"""
		
		self.angle=angle
		self.vcenter=vcenter
		self.vstart=vstart
		self.vend=vertex([0,0])
		
		self.computeRadius()
		self.computeVend()
		
	
	def computeAngle(self,debug=False):
		
		"""Computes both angle and angle_offset of arc
		
		:param debug: Debugging flag.
		:type debug: bool
		:returns: (float,float) -- angle, angle_offset
		
		"""
		
		self.angle_offset=rwe.angle_from_vertices(self.vcenter,vertex(self.domain,[self.radius,0.],-1),self.vstart)
		self.angle=rwe.direc_angle(self.vstart.x-self.vcenter.x,self.vend.x-self.vcenter.x)
	
		if debug:
			print "angle_offset = ", self.angle_offset
			print "angle = ", self.angle
		
		return self.angle,self.angle_offset
	
	def computeRadius(self):
		self.radius=np.linalg.norm(self.vstart.x-self.vcenter.x)
		return self.radius
	
	def computeVend(self):
		self.vend.setX(self.computePoint(self.angle,self.radius))
	
	def computeVstart(self):
		self.vstart.setX(self.computePoint(self.angle_offset,self.radius))
	
	def computePoint(self,angle,radius):
		
		"""Computes point on arc
		
		:param angle: Point's angle.
		:type angle: float
		:param radius: Point's radius.
		:type radius: float
		
		"""
		
		return self.vcenter+radius*np.array([np.cos(angle),np.sin(angle)])
		
	def setAngle(self,angle):
		
		self.angle=angle
		self.computeVend()
		return angle
		
	def setRadius(self,radius):
		self.radius=radius
		self.computeVend()
		self.computeVstart()
		
		return radius
	
	def inArc(self,x,debug=False):
		
		"""Checks if points x lies on arc
		
		:param x: coordinate.
		:type x: array
		:param debug: Debugging flag.
		:type debug: bool
		
		"""
		
		a=rwe.compute_angle(np.array([self.radius,0])-self.vcenter.x,x-self.vcenter.x)
		
		if debug:
			print 
			print "Angle(x) = " , a
			print "arc.angle = " , self.angle
			print "arc.angle_offset = " , self.angle_offset
			
			
		if np.mod(a,2*np.pi)<self.angle+self.angle_offset and self.angle_offset<=np.mod(a,2*pi):
			if debug:
				print True
			return True
		else:
			if debug:
				print False
			return False
	
	def getRadius(self):
		return self.radius
	
	def getAngle(self):
		return self.angle
	
	def getAngleOffset(self):
		return self.angle_offset
	
	def getVstart(self):
		return self.vstart
	
	def getVend(self):
		return self.vend
	
	def getXstart(self):
		return self.vstart.x
	
	def getXend(self):
		return self.vend.x
	
	def getVcenter(self):
		return self.vcenter
	
	def getXcenter(self):
		return self.vcenter.x
	
	def draw(self,r=None,color=None,ann=False):
		
		"""Draw arc
		
		:param r: pyrw run, if None, picks last run of main pyrw.RWRW object. 
		:type r: pyrw.RWrun
		:param color: color of arc in matplotlib syntax, e.g. 'r' or (0.1,1,0.5)
		:type color: matplotlib color
		:param ann: Annotation Flag
		:type ann: bool
		
		"""
		
		if ann==None:
			ann=False
		
		if r==None:
			r=self.domain.RW.runs[-1]
		
		if not hasattr(r,'fig_traj'):
			r.fig_traj=plt.figure()
			r.ax_traj=r.fig_traj.add_subplot(111)
			r.fig_traj.show()
			
		xvec,yvec=rwe.create_arc_curve(self.vcenter,self.angle,self.angle_offset,self.radius)
		
		r.ax_traj.plot(xvec,yvec,color='r',linestyle='-')
		if ann:
			r.ax_traj.annotate('a'+str(self.Id), xytext=((self.vstart.x[0]+self.vend.x[0])/2., (self.vstart.x[1]+self.vend.x[1])/2.),xy=(self.vcenter.x[0]+0.5, self.vcenter.x[1]+0.5),)
		
		plt.draw()

class circle:
	
	"""Circle class for defining domain geometry.

	:param domain:  A pyrw domain.
	:type domain: pyrw.RWdomain
	:param vcenter: Center vertex of the arc.
	:type vcenter: pyrw.RWgeometry.vertex
	:param radius: Radius.
	:type radius: float
	
	"""
	
	
	def __init__(self,domain,vcenter,radius):
		self.domain=domain
		
		
		self.vcenter=vcenter
		self.radius=radius
		
		vright=self.domain.addVertex([vcenter.x[0]+radius,vcenter.x[1]])
		vtop=self.domain.addVertex([vcenter.x[0],vcenter.x[1]+radius])
		vleft=self.domain.addVertex([vcenter.x[0]-radius,vcenter.x[1]])
		vbottom=self.domain.addVertex([vcenter.x[0],vcenter.x[1]-radius])
		
		self.vertices=[self.vcenter,vright,vtop,vleft,vbottom]
		
		arc1=self.domain.addArc(vright,vcenter,vend=vtop)
		arc2=self.domain.addArc(vtop,vcenter,vend=vleft)
		arc3=self.domain.addArc(vleft,vcenter,vend=vbottom)
		arc4=self.domain.addArc(vbottom,vcenter,vend=vright)
		
		self.arcs=[arc1,arc2,arc3,arc4]
		
	def setRadius(self,radius):
		
		self.radius=radius
		
		for a in self.arcs:
			a.setRadius(radius)
			
	def setXcenter(self,x):	
		self.vcenter.setX(x)
		self.setRadius(self.radius)
		
		return x
	
	def setVcenter(self,v):	
		self.vcenter=v
		self.setRadius(self.radius)
		
		return vcenter
	
	def getRadius(self):
		return self.radius
	
	def getVcenter(self):
		return self.vcenter
	
	def getXcenter(self):
		return self.vcenter.x
	
	def getVertices(self):
		return self.vertices
	
	def getArcs(self):
		return self.arcs
	
	def getDomain(self):
		return self.domain
	
	def draw(self):
		
		for a in self.arcs:
			a.draw()
			
class rectangle:
	
	"""Rectangle class for defining domain geometry.

	:param domain:  A pyrw domain.
	:type domain: pyrw.RWdomain
	:param voffset: Offset vertex of the arc.
	:type voffset: pyrw.RWgeometry.vertex
	:param lenx: Sidelength in x direction.
	:type lenx: float
	:param leny: Sidelength in y direction.
	:type leny: float
	
	"""
	
	def __init__(self,domain,voffset,lenx,leny):
		
		self.domain=domain

		self.voffset=voffset
		self.lenx=lenx
		self.leny=leny
		
		vright=self.domain.addVertex([voffset.x[0]+lenx,voffset.x[1]])
		vtop=self.domain.addVertex([voffset.x[0]+lenx,voffset.x[1]]+leny)
		vleft=self.domain.addVertex([voffset.x[0],voffset.x[1]]+leny)
		
		self.vertices=[self.vcenter,vright,vtop,vleft,vbottom]
		
		e1=self.domain.addLine(voffset,vright)
		e2=self.domain.addLine(vright,vtop)
		e3=self.domain.addLine(vtop,vleft)
		e4=self.domain.addLine(vleft,voffset)
		
		self.edges=[e1,e2,e3,e4]
	
	def setLenx(self,lenx):
		self.vertices[1].setX([self.voffset.x[0]+lenx,self.voffset.x[1]])
		self.vertices[2].setX([self.voffset.x[0]+lenx,self.voffset.x[1]]+self.leny)
	
	def setLeny(self,leny):
		self.vertices[3].setX([self.voffset.x[0],self.voffset.x[1]]+leny)
		self.vertices[2].setX([self.voffset.x[0]+lenx,self.voffset.x[1]]+self.leny)
	
	def setXoffset(self,xoffset):
		self.voffset.setX(xoffset)
		self.setLenx(self.lenx)
		self.setLeny(self.leny)
		
	def getXoffset(self):
		return self.voffset.x
	
	def getVoffset(self):
		return self.voffset
	
	def getLenx(self):
		return self.lenx
	
	def getLeny(self):
		return self.leny
		
	def getEdges(self):
		return self.edges
	
	def getVertices(self):
		return self.vertices
	
	def getDomain(self):
		return self.domain
		
	def draw(self,r=None,color=None,ann=None):
		for v in self.vertices:
			v.draw(r=r,color=color,ann=ann)
		for e in self.edges:
			e.draw(r=r,color=color,ann=ann)
			
		
	
		
					
		
	