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

#Misc
import sys

#PyRW
import RWdomain
import RWwalker
import RWrun
import RWmisc

#===========================================================================
#Module description
#===========================================================================

"""
Random walk RW module of pyrw containing the RW class.
"""

#===========================================================================
#Module classes
#===========================================================================

class RW:
	
	#Creates new RW object
	def __init__(self,tstart=0.,tend=1000.,deltat=1.,N=5,P=1,name="RW"):
		
		self.tstart=tstart
		self.tend=tend
		self.deltat=deltat
		self.N=N
		self.P=P
			
		self.tvec=np.arange(self.tstart,self.tend,self.deltat)
		
		self.runs=[]
		self.walkers=[]
		
		self.domain=RWdomain.domain(self)
		
		self.msd=None
		self.mL=None
		self.mT=None
		
		self.totalRuntime=None
		
		self.name=name
		
	#Create new run
	def addRun(self):
		
		r=RWrun.run(self)	
		self.runs.append(r)
		
		return r
	
	#Create N new runs
	def addNRuns(self,N):
		
		for n in range(N):
		
			r=RWrun.run(self)	
			self.runs.append(r)
			
		return self.runs
	
	#Perform all runs
	def runAll(self,printProcess=True,printRunProcess=False,plotStep=False):
		for i,r in enumerate(self.runs):
			r.start(printProcess=printRunProcess,plotStep=plotStep)
			
			if printProcess:
				currPerc=floor(float(i)/float(len(self.runs))*100)
				sys.stdout.write("\r%d%%" %currPerc)  
				sys.stdout.flush()
		
	#Add walker
	def addWalker(self,x0=np.array([0,0]),RWtyp='MRW',color='b',BCtyp='sticky',HCtyp=None,hitGroup=[],typ='typ0',hitTypes=None,detectRadius=1.,successRate=1.):
		if len(self.walkers)==0:
			new_wid=0
		else:
			wids=[]
			for w in self.walkers:
				wids.append(w.wid)
			new_wid=max(wids)+1	
		
		w=RWwalker.walker(self,x0=x0,RWtyp=RWtyp,color=color,wid=new_wid,BCtyp=BCtyp,HCtyp=HCtyp,hitGroup=hitGroup,typ=typ,hitTypes=hitTypes,detectRadius=detectRadius,successRate=successRate)
		
		self.walkers.append(w)
		
		return w

	def getDomain(self):
		return self.domain
	
	def setDomain(self,d):
		self.domain=d
		self.domain.setRW(self)
		return d
	
	def getWalkerById(self,Id):
		for w in self.walkers:
			if w.wid==Id:
				return w
		return False
		
	def getMeanRuntime(self):
		rt=[]
		for r in self.runs:
			rt.append(r.runtime)
		return np.mean(rt)
	
	def getTotalRuntime(self):
		rt=[]
		tStep=[]
		tBC=[]
		tHC=[]
		tTraj=[]
		
		for r in self.runs:
			rt.append(r.runtime)
                        tStep.append(r.tStep)
                        tHC.append(r.tHC)
                        tBC.append(r.tBC)
                        tTraj.append(r.tTraj)
                        
		self.totalRuntime=sum(rt)
		
		self.totaltStep=sum(tStep)
		self.totaltBC=sum(tBC)
		self.totaltHC=sum(tHC)
		self.totaltTraj=sum(tTraj)
		
		return sum(rt)
        
        
	def computeStatistics(self):
                ts=[]
                ls=[]
                sds=[]
		for r in self.runs:
                        if r.done:
                                w=r.getWalkerOfInterest()
                                w.computeStatistics()
                                ts.append(r.tStop)
                                ls.append(w.L)
                                sds.append(w.SD)
                
                self.mT=np.mean(ts)
                self.mL=np.mean(ls)
                self.msd=np.mean(sds)
                
                self.getTotalRuntime()
                
                return self.mT, self.mL, self.msd, self.totalRuntime
        
        def printStatistics(self):
                print 
                self.printVariable('mT')
                self.printVariable('mL')
                self.printVariable('msd')
                self.printVariable('totalRuntime')
                
        def printVariable(self,var):
                RWmisc.printVariable(var,self)
          
        def setVarForAllRuns(self,var,val):
                for r in self.runs:
                        RWmisc.setVariable(var,r,val)
                return self.runs
        
        def saveToFile(self,fn=None):
		RWmisc.saveToPickle(self,fn=None)
                return fn
         
        def statsToCSV(self,fn=None):
                results=[self.mT,self.mL,self.msd,self.totalRuntime]
                RWmisc.listToCSV(results,fn=fn)
                return fn
                
        
        
          
                                                                