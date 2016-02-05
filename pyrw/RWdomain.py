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

#PyRW
import RWgeometry as RWgeo
import RWessentials as rwe

#Numpy
import numpy as np

#Matplotlib
import matplotlib.pyplot as plt

#===========================================================================
#Module description
#===========================================================================

"""
Domain module of pyrw containing classes for defining all the elements defining
the geometry of the domain for random walkers, including the following classes:

(1 domain)
"""

#===========================================================================
#Module classes
#===========================================================================


class domain:
	
		
	"""Domain class for defining random walk domain.

	:param RW:  A pyrw RW.
	:type RW: pyrw.RWRW
	:param typ: Type of domain 
	:type typ: str
	
	"""
	
	def __init__(self,RW,typ='poly'):
		
		self.edges=[]
		self.vertices=[]
		self.arcs=[]
		self.lines=[]
		self.RW=RW
		
	def addVertex(self,x):
		
		"""Adds vertex to domain.

		:param x:  2D coordinate.
		:type x: pyrw.RWRW
		:returns: pyrw.geometry.vertex -- vertex object
		
		"""
			
		if len(self.vertices)==0:
			new_Id=0
		else:
			Ids=[]
			for v in self.vertices:
				Ids.append(v.Id)
			new_Id=max(Ids)+1	
		
		v=RWgeo.vertex(self,x,new_Id)
		self.vertices.append(v)	
		
		return v
		
	def addLine(self,v1,v2):
		
		
		"""Adds line from v1 to v2 to domain.

		:param v1:  Vertex object.
		:type v1: pyrw.geometry.vertex
		:param v2:  Vertex object.
		:type v2: pyrw.geometry.vertex
		:returns: pyrw.geometry.line -- line object
		
		"""
		
		if len(self.lines)==0:
			new_Id=0
		else:
			Ids=[]
			for e in self.lines:
				Ids.append(e.Id)
			new_Id=max(Ids)+1	
		
		e=RWgeo.line(self,v1,v2,new_Id)
		self.lines.append(e)
		self.edges.append(e)
		
		return e
	
	def addArc(self,vstart,vcenter=None,vend=None,angle=None):
		
		"""Adds arc from vstart to vend around vcenter to domain.

		:param vstart:  Vertex object.
		:type vstart: pyrw.geometry.vertex
		:param vcenter:  Vertex object.
		:type vcenter: pyrw.geometry.vertex
		:param vend:  Vertex object.
		:type vend: pyrw.geometry.vertex
		:param angle: Angle.
		:type angle: float
		:returns: pyrw.geometry.arc -- arc object
		
		"""
		
		if len(self.arcs)==0:
			new_Id=0
		else:
			Ids=[]
			for a in self.arcs:
				Ids.append(a.Id)
			new_Id=max(Ids)+1
		a=RWgeo.arc(self,vstart,vcenter,new_Id,vend=vend,angle=angle)
		self.arcs.append(a)
		self.edges.append(a)
		
		return a
	
	def addCircle(self,vcenter,radius,BC=""):
		
		"""Adds circle around vcenter with r=radius to domain.

		:param vcenter:  Vertex object.
		:type vcenter: pyrw.geometry.vertex
		:param radius:  Radius of circle.
		:type radius: float
		:returns: pyrw.geometry.circle -- circle object
		"""
		
		c=RWgeo.circle(self,vcenter,radius)
		self.typ='circle'
			
		return c

	def addRectangle(self,voffset,lenx,leny):
		
		"""Adds rectangle with offset voffset and sidelengths lenx,leny to domain.

		:param voffset:  Vertex object.
		:type voffset: pyrw.geometry.vertex
		:param lenx:  Sidelength in x direction.
		:type lenx: float
		:param leny:  Sidelength in y direction.
		:type leny: float
		:returns: pyrw.geometry.rectangle -- rectangle object
		"""
		
		r=RWgeo.rectangle(self,voffset,lenx,leny)
		self.typ='poly'
		return r
	
	def setRW(self,rw):
		self.RW=rw
		return self.RW
	
	def edgeByID(self,ID):
		
		"""Returns edge given its ID

		:param ID:  ID of edge.
		:type ID: int
		:returns: pyrw.geometry.edge -- edge object
		"""
		
		for i,e in enumerate(self.edges):
			if e.ID==ID:
				return e,i
		return False,False
		
	def draw(self,r=None,color=None,ann=False):
		
		"""Draw all geometrical elements associated with domain.
		
		:param r: pyrw run, if None, picks last run of main pyrw.RWRW object. 
		:type r: pyrw.RWrun
		:param color: color of elements in matplotlib syntax, e.g. 'r' or (0.1,1,0.5)
		:type color: matplotlib color
		:param ann: Annotation Flag
		:type ann: bool
		
		"""
		
		if ann==None:
			ann=False
		
		if color==None:
			color='k'
		
		if r==None:
			r=self.RW.runs[-1]
		
		if not hasattr(r,'fig_traj'):
			r.fig_traj=plt.figure()
			r.ax_traj=r.fig_traj.add_subplot(111)
			r.fig_traj.show()
		
		for v in self.vertices:
			v.draw(r=r,color=color,ann=ann)
		for e in self.edges:
			e.draw(r=r,color=color,ann=ann)	
		for a in self.arcs:
			a.draw(r=r,color=color,ann=ann)	
		
	def getExtend(self):
		
		"""Returns x-y-extend of domain.

		:returns: (float,float,float,float) -- (minX,maxX,minY,maxY)
		"""
		
		x=[]
		y=[]
		for v in self.vertices:
			x.append(v.x[0])
			y.append(v.x[1])
		
		return min(x), max(x), min(y),max(y)
	
	def verticesCoordsToList(self):
		
		"""Returns list with coordinates of all vertices of domain.

		:returns: list -- list with coordinates
		"""
		
		l=[]
		for v in self.vertices:
			l.append(v.x)
		return l
	
	def genRandomPoint(self):
		
		"""Returns random coordinate inside domain.

		:returns: array -- coordinate
		"""
		
		xmin,xmax,ymin,ymax=self.getExtend()
		poly=self.verticesCoordsToList()
		
		outside=True
		while outside:
	
			xrand=(xmax - xmin) * np.random.random() + xmin
			yrand=(ymax - ymin) * np.random.random() + ymin
		
			if self.typ=='poly':
				if rwe.checkInsidePoly([xrand,yrand],poly):
					return np.array([xrand,yrand])
			if self.typ=='circle':
				if rwe.checkInsideCircle([xrand,yrand],self.edges[0].vcenter.x,0.999*self.edges[0].radius,tol=0.)<0:
					return np.array([xrand,yrand])
			else:
				print "Warning, can not generate random points for geometry of typ = ", self.typ
				return False,False
				
		
		