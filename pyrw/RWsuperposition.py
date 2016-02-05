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

import numpy as np

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
			phi_rand=np.random.uniform(-1,1,1)[0]*np.pi
		else:
			phi_rand=np.random.vonmises(self.walker.d,self.kappa)
		direc=np.array([np.cos(phi_rand),np.sin(phi_rand)])
		
		#Choosing step length
		rho_rand=abs(np.random.exponential(self.r))
		
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
                
                
                