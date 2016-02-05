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

#PyRW
import RWBC
import RWHC
import RWstep
import RWessentials as rwe

#===========================================================================
#Module description
#===========================================================================

"""
walker module of pyrw containing classes describing all properties of
walkers, including the following classes:

(1) walker

"""



#===========================================================================
#Module classes
#===========================================================================

class walker:
	
	def __init__(self,RW,x0=np.array([0,0]),RWtyp='MRW',color='r',wid=None,BCs=[],BCtyp='sticky',HCtyp=None,hitGroup=[],typ='typ0',hitTypes=None,detectRadius=1.,successRate=1.):
		
		#Refer to RW
		self.RW=RW
		
		#ID
		self.wid=wid
		
		#Coordinates
		self.x0=np.array(x0)
		self.x=self.x0.copy()
		self.xold=self.x0.copy()
		self.d=None
		
		#Detection radius
		self.detectRadius=detectRadius
		
		#SuccessRate
		self.successRate=successRate
		
		#Color for plotting
		self.color=color
		
		#RW type
		self.RWtyp=RWtyp
		
		#Walker Type
		self.typ=typ
		
		#Set current run to None
		self.currRun=None
		
		#Bookkeeping of trajectory
		self.traj=[self.x0]
		
		#BCs
		self.BCmap=np.zeros((2,len(self.RW.domain.edges)))
		self.BCIds=[]
		self.BCtyp=0
		
		if BCs==[]:
			self.BCs=[]
			self.BCs=self.setAllBCs(BCtyp)
		else:
			self.BCs=BCs
		
		#Hit Condition
		self.HCtyp=HCtyp
		self.hitTypes=hitTypes
		
		if self.HCtyp!=None:
			if hitGroup==[]:
				self.hitGroup=self.genHitGroup()
			
			self.HC=self.genHC(HCtyp,hitGroup)
		else:
			self.HC=None
		
		#Step
		self.step=self.genStep(self.RWtyp)
		
		#Walker statistics
		self.L=None
		self.SD=None
		
	def setAllBCs(self,typ):
		for i,e in enumerate(self.RW.domain.edges):
			newBC=self.genBC(typ,e)
			self.BCmap[0,i]=e.Id
			self.BCmap[1,i]=newBC.Id
			self.BCs.append(newBC)
		self.updateBCIds()
		self.updateBCTyp()
		
		return self.BCs
		
	def setBC(self,typ,ID):
		e,idx=self.RW.domain.edgeByID(ID)
		self.BCs[idx]=genBC(typ)
		self.updateBCTyp()
		
	def genBC(self,typ,edge):
		
		try:
			newId=max(self.BCIds)+1
		except ValueError:
			newId=0
			
		if typ=='sticky':
			return RWBC.sticky(self,newId,edge)
		elif typ=='reflect':
			return RWBC.reflect(self,newId,edge)
		elif typ=='randomReflect':	
			return RWBC.randomReflect(self,newId,edge)
		elif typ=='setBack':
			return RWBC.setBack(self,newId,edge)
		elif typ=='absorb':
			return RWBC.absorb(self,newId,edge)
		
	def getBCIds(self):
		return self.BCIds
	
	def genHC(self,typ,hitGroup):
		if typ=='stop':
			return RWHC.stop(self.RW,self,hitGroup,suc=self.successRate)
		
	def updateBCIds(self):
		self.BCIds=[]
		for BC in self.BCs:
			self.BCIds.append(BC.Id)
	
	def allBCsSame(self):
		for i in range(len(self.BCs)-1):
			if self.BCs[i].typ!=self.BCs[i+1].typ:
				return False
		return True
	
	def genHitGroup(self):
		
		self.hitGroup=[]
		self.hitGroupWalkers=[]
		
		if self.hitTypes==None or self.hitTypes==[]:
			self.hitTypes=[]
			for w in self.RW.walkers:
				
				if (self.typ!=w.typ) and (w.typ not in self.hitTypes):
					self.hitTypes.append(w.typ)
		
		for i,w in enumerate(self.RW.walkers):
			if w.wid!=self.wid:
				
				if w.typ in self.hitTypes:
					
					self.hitGroup.append(i)
					self.hitGroupWalkers.append(w)
		return self.hitGroup
	
	def getHitGroupLoc(self):
		self.hitGroupLoc=[]
		for i in self.hitGroup:
			self.hitGroupLoc.append(self.RW.walkers[i].x)
		
		return self.hitGroupLoc
		
	def updateBCTyp(self):
		if self.allBCsSame():
			self.BCtyp=self.BCs[0].typ
		else:
			self.BCtyp=-1
	
	def checkBC(self):
                
		#Remember current location
                xtemp=self.x.copy()
		
		#In case of a circle and setBack/sticky we do not need to check all edges (saves us additional calls of hit)
                if self.RW.domain.typ=='circle' and self.BCtyp in [0,1]:
			self.x=self.BCs[0].hit(self.xold,self.x)
                else:
			#Loop through all BCs
			for i,BC in enumerate(self.BCs):
				
				#Check if boundary hit
				self.x=BC.hit(self.xold,self.x)
				
				#Check if self.x changed, if so, break (trajectory can only pass through one edge)
				if not (self.x==xtemp).all():       
					break
					
		return self.x
	
	def checkHC(self):
		
		if self.HC!=None:
			self.getHitGroupLoc()
			
			self.HC.hit(debug=False)
			
	def getDetectRadius(self):
		return self.detectRadius
	
	def setDetectRadius(self,radius):
		self.detectRadius=radius
		return self.detectRadius
	
	def setX0(self,x0):
		self.x0=x0
		return self.x0
	
	def getX0(self):
		return self.x0
	
	def genStep(self,typ,rs=[1.,3.],gammas=[0.5,0.5],kappas=[0.,3.]):	
		if typ=='MRW':
			self.step=RWstep.MRWstep(self,rs[0])
		elif typ=='CRW':
			self.step=RWstep.CRWstep(self,rs[0],rs[1],gammas[0])
		elif typ=='CorRW':
			self.step=RWstep.CRWstep(self,r,kappas[1])
		elif typ=='CCRW':
			self.step=RWstep.CCRWstep(self,rs[0],rs[1],gammas[0],kappas[1])
		else:
			self.step=RWstep.step(self,-1)
			for i in range(len(rs)):
				self.step.addSuperposition(rs[i],gammas[i],kappas[i])
				self.step.checkGammas()
				
		return self.step		
				
	def setToStart(self):
		self.x=self.x0.copy()
		self.xold=self.x0.copy()
		self.d=None		
	
	def toTraj(self):
		self.traj.append(self.x)
		return self.traj	
	
	def plotTraj(self,draw=True,color=None):
		
		self.currRun.checkFig()
		
		traj=array(self.traj)
		if color==None:
			self.currRun.ax_traj.plot(traj[:,0],traj[:,1],self.color)
		else:	
			self.currRun.ax_traj.plot(traj[:,0],traj[:,1],color)
			
		if draw:
			plt.draw()
		
	def setCurrRun(self,r):
		self.currRun=r
		return r
	
	def computeTrajLength(self):
		d=[]
		for i in range(len(self.traj)-1):
			d.append(rwe.dist(self.traj[i],self.traj[i+1]))
		self.L=sum(d)
		return self.L
	
	def getTrajLength(self):
		return self.L
	
	def computeSquaredDisplacement(self):
		self.SD=(self.x-self.x0)**2
		return self.SD
	
	def getSquaredDisplacement(self):
		return self.SD
		
	def computeStatistics(self):
		self.computeSquaredDisplacement()
		self.computeTrajLength()
	
	def genRandomX0(self):
		
		x=self.RW.domain.genRandomPoint()
		if x[0]!=False:
			self.x0=x
		
		
		