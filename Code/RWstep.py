from numpy import *
import RWsuperposition

class step(object):

	#Init
	def __init__(self,w,typ):
		self.walker=w
		self.typ=typ
		self.superpositions=[]
	
	def updateGammaDist(self):
		self.gammaVec=[0.]
		for s in self.superpositions:
			self.gammaVec.append(self.gammaVec[-1]+s.gamma)
		return self.gammaVec
		
	def checkGammas(self,debug=False):
		sumGammas=0
		for s in self.superpositions:
			sumGammas=sumGammas+s.gamma
		if sumGammas==1:
			return True
		else:
			if debug:
				print "Warning, gammas do not sum up to 1!"
			return False
	
	def performStep(self):
		
		#Pick random number to choose which superposition
		rand_mode=random.random()
		
		#Check which superposition to perform
		for i in range(len(self.gammaVec)): 
			#print self.gamaVec[i], " <= ", rand_mode , " < = " 
			if self.gammaVec[i]<=rand_mode and rand_mode<=self.gammaVec[i+1]:
				self.superpositions[i].doStep()
				break
			
	def addSuperposition(self,r,gamma,kappa):
		
		try:
			newId=max(self.getSuperpositionIds)+1
		except TypeError:
			newId=0
		
		s=RWsuperposition.superposition(self.walker,r,gamma,kappa,newId)
		self.superpositions.append(s)
		
		self.updateGammaDist()
		return s
	
	def getSuperpositionIds(self):
		ids=[]
		for s in self.superpositions:
			ids.append(s.Id)
		
		return ids
	
class MRWstep(step):
	
	#Init
	def __init__(self,w,r):
		super(MRWstep, self).__init__(w,0)
		
		#Add simple Brownian step
		self.addSuperposition(r,1,0)
			
class CRWstep(step):
	
	#Init
	def __init__(self,w,r1,r2,gamma):
		super(CRWstep, self).__init__(w,1)
		
		#Add two superpositions
		self.addSuperposition(r1,gamma,0)
		self.addSuperposition(r2,gamma,0)
		
class CorRWstep(step):
	
	#Init
	def __init__(self,w,r,kappa):
		super(CorRWstep, self).__init__(w,2)
		
		#Add simple correlated random walk
		self.addSuperposition(r,1,kappa)
		
class CCRWstep(step):
	
	#Init
	def __init__(self,w,r1,r2,gamma,kappa):
		super(CCRWstep, self).__init__(w,3)
		
		#Add two superpositions, one MRW and one CorRW
		self.addSuperposition(r1,gamma,0)
		self.addSuperposition(r2,1-gamma,kappa)
		
	def setParms(self,parms):
                self.scaleR(parms[0])
                self.setGamma(parms[1])
                self.setKappa(parms[2])
                
	def scaleR(self,rScale):
                r1=self.superpositions[0].getR()
                self.setR2(rScale*r1)
                return rScale*r1
        
        def setGamma(self,gamma):
                self.superpositions[0].setGamma(gamma)
                self.superpositions[1].setGamma(1-gamma)
                return gamma
        
        def setKappa(self,kappa):
                self.superpositions[1].setKappa(kappa)
                return kappa
        
        def setR1(self,r):
                self.superpositions[0].setR(r)
                return r
        
        def setR2(self,r):
                self.superpositions[1].setR(r)
                return r
                
                
		
	
	
	
	
	
		