import RWdomain
import RWgeometry as RWgeo
import RWessentials as rwe

from numpy import *
import matplotlib.pyplot as plt


class domain:
	
	def __init__(self,RW,typ='poly'):
		
		self.edges=[]
		self.vertices=[]
		self.arcs=[]
		self.lines=[]
		self.RW=RW
		
	def addVertex(self,x):
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
		
		c=RWgeo.circle(self,vcenter,radius)
		self.typ='circle'
			
		return c

	def addRectangle(self,voffset,lenx,leny):
		r=RWgeo.rectangle(self,voffset,lenx,leny)
		self.typ='poly'
		return r
	
	def setRW(self,rw):
		self.RW=rw
		return self.RW
	
	def edgeByID(self,ID):
		for i,e in enumerate(self.edges):
			if e.ID==ID:
				return e,i
		return False,False
		
	def draw(self,r=None,color=None,ann=None):
		
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
		x=[]
		y=[]
		for v in self.vertices:
			x.append(v.x[0])
			y.append(v.x[1])
		
		return min(x), max(x), min(y),max(y)
	
	def verticesCoordsToList(self):
		l=[]
		for v in self.vertices:
			l.append(v.x)
		return l
	
	def genRandomPoint(self):
		
		xmin,xmax,ymin,ymax=self.getExtend()
		poly=self.verticesCoordsToList()
		
		outside=True
		while outside:
	
			xrand=(xmax - xmin) * random.random() + xmin
			yrand=(ymax - ymin) * random.random() + ymin
		
			if self.typ=='poly':
				if rwe.checkInsidePoly([xrand,yrand],poly):
					return array([xrand,yrand])
			if self.typ=='circle':
				if rwe.checkInsideCircle([xrand,yrand],self.edges[0].vcenter.x,0.999*self.edges[0].radius,tol=0.)<0:
					return array([xrand,yrand])
			else:
				print "Warning, can not generate random points for geometry of typ = ", self.typ
				return False,False
				
		
		