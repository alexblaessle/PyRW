from numpy import *

class superposition:
	
	def __init__(self,w,r,gamma,kappa,Id):
		
		self.walker=w
		
		self.r=r
		self.gamma=gamma
		self.kappa=kappa
		
		self.Id=Id
		
	def doStep(self):
		
	
		#Direction
		if self.kappa==0 or self.walker.d==None:
			phi_rand=random.uniform(-1,1,1)[0]*pi
		else:
			phi_rand=random.vonmises(self.walker.d,self.kappa)
		direc=array([cos(phi_rand),sin(phi_rand)])
		
		#Choosing step length
		rho_rand=abs(random.exponential(self.r))
		
		#update coordinate
		self.walker.xold=self.walker.x.copy()
		self.walker.x=self.walker.x+rho_rand*direc
		
		#Safe direction
		self.walker.d=phi_rand
		
		return self.walker.x, self.walker.d
        
        def setR(self,r):
                self.r=r
                return r
        
        def getR(self):
                return self.r
        
        def setGamma(self,gamma):
                self.gamma=gamma
                return self.gamma
        
        def getGamma(self):
                return self.gamma
        
        def setKappa(self,kappa):
                self.kappa=kappa
                return self.kappa
        
        def getKappa(self):
                return self.kappa
                
                
                