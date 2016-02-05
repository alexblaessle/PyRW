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


import RWessentials as rwe

class HC(object):
	
	#Init
	def __init__(self,RW,w,typ,Id,suc=1.):
		self.walker=w
		self.typ=typ
		self.Id=Id
		self.RW=RW
		self.suc=suc
		
	def hitRW(self,x1,x2,r1):
		if rwe.dist(x1,x2)<r1:
			return True
		else:
			return False
		
		

	
class stop(HC):
	
	#Init
	def __init__(self,RW,w,Id,suc=1.):
		super(stop, self).__init__(RW,w,0,Id,suc=suc)
		
	def hit(self,suc=1.,debug=False):
		
		if min(np.linalg.norm(self.walker.x-np.array(self.walker.hitGroupLoc),axis=1))<self.walker.detectRadius:
			
			if debug:
				print "Walker ", self.walker.wid, " encountered walker ", self.walker.hitGroupWalkers[argmin(linalg.norm(self.walker.x-array(self.walker.hitGroupLoc),axis=1))].wid
			
			suc_rand=np.random.random()
			if suc_rand<min(suc,self.suc):
				if debug:
					print "Walker ", self.walker.wid, " terminated at walker ", self.walker.hitGroupWalkers[argmin(np.linalg.norm(self.walker.x-np.array(self.walker.hitGroupLoc),axis=1))].wid
				self.walker.currRun.stop(True)
				return True

		return False
	
	
#class kill(HC):
	
	##Init
	#def __init__(self,w,Id,edge):
		#super(kill, self).__init__(w,1,Id,edge)		