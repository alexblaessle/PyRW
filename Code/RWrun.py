from numpy import *
import matplotlib.pyplot as plt
import sys
import time

class run:

	def __init__(self,RW):
		self.tvec=RW.tvec
		self.RW=RW
		self.stopped=False
		self.runtime=None
		self.done=False
		self.tStopped=None
		
		self.groupOfInterest=[]
		
		self.tStepVec=[]
		self.tHCVec=[]
		self.tBCVec=[]
		self.tTrajVec=[]
		
	def start(self,plotStep=False,printProcess=False):
		self.timeStart=time.clock()
		
		#Pass current run to walker, generate hitGroup and set to initial location
		for w in self.RW.walkers:
			w.currRun=self
			w.genHitGroup()
			w.setToStart()
		
		for t in self.tvec:
			
			#Print Process
			if printProcess:
				sys.stdout.write("\r%d" %t)  
				sys.stdout.flush()
			
			if not self.stopped:
				self.tCurrent=t
				self.doStep()
				if plotStep:
					self.plotStep()
			else:
				
				break
			
		self.stop(False)
		
	def stop(self,stopped):
		
		self.done=True
                self.tStop=self.tCurrent
		self.stopped=stopped
		self.computeEndStastics()
		self.runtime=time.clock()-self.timeStart
		
		self.tStep=sum(self.tStepVec)
                self.tBC=sum(self.tBCVec)
                self.tHC=sum(self.tHCVec)
                self.tTraj=sum(self.tTrajVec)
                
                
	def doStep(self,debug=False):
		
		#if debug:
		
		for W in self.RW.walkers:
                        
			#update coordinate
			tStepStart=time.clock()
			W.step.performStep()
			self.tStepVec.append(time.clock()-tStepStart)
			
			
			#Check BC
			tBCStart=time.clock()
			W.checkBC()
                        self.tBCVec.append(time.clock()-tBCStart)
                        
                        
		#Check HC
		for W in self.RW.walkers:
			tHCStart=time.clock()
			W.checkHC()
                        self.tHCVec.append(time.clock()-tHCStart)
                        
			#Update trajectory
			tTrajStart=time.clock()
			W.toTraj()
			self.tTrajVec.append(time.clock()-tTrajStart)
			
	def plotStep(self,color=None):

		self.checkFig()
		
		for W in self.RW.walkers:
                        if color==None:
                                self.ax_traj.plot([W.xold[0],W.x[0]],[W.xold[1],W.x[1]],W.color)
                        else:
                                self.ax_traj.plot([W.xold[0],W.x[0]],[W.xold[1],W.x[1]],color)
                                
		plt.pause(0.0000000001)
		plt.draw()
	
	def plotTraj(self,color=None):
		
		self.checkFig()
		
		for W in self.RW.walkers:
			W.plotTraj(color=color,draw=False)
		
		plt.draw()
	
	def scalePlot(self):
		
		xs=[]
		ys=[]
		for v in self.RW.domain.vertices:
			xs.append(v.x[0])
			ys.append(v.x[1])
		xmax=max(xs)
		ymax=max(xs)
		xmin=min(xs)
		ymin=min(xs)

		self.ax_traj.set_xlim([xmin-1,xmax+1])
		self.ax_traj.set_ylim([ymin-1,ymax+1])
	
	def checkFig(self):
		if not hasattr(self,'fig_traj'):
			self.fig_traj=plt.figure()
			self.ax_traj=self.fig_traj.add_subplot(111)
			self.fig_traj.show()
		
		return self.fig_traj,self.ax_traj
	
	def computeEndStastics(self):
		for w in self.RW.walkers:
			w.computeStatistics()
			
	def getRuntime(self):
		return self.runtime
	
	def setGroupOfInterest(self,group):
                self.groupOfInterest=group
                return self.groupOfInterest
        
        def getGroupOfInterest(self):
                return self.groupOfInterest
        
        def setWalkerOfInterest(self,w):
                self.walkerOfInterest=w
                return w
        
        def getWalkerOfInterest(self):
                return self.walkerOfInterest
                
        
                
                        