from numpy import *
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
		
		if min(linalg.norm(self.walker.x-array(self.walker.hitGroupLoc),axis=1))<self.walker.detectRadius:
			
			if debug:
				print "Walker ", self.walker.wid, " encountered walker ", self.walker.hitGroupWalkers[argmin(linalg.norm(self.walker.x-array(self.walker.hitGroupLoc),axis=1))].wid
			
			suc_rand=random.random()
			if suc_rand<min(suc,self.suc):
				if debug:
					print "Walker ", self.walker.wid, " terminated at walker ", self.walker.hitGroupWalkers[argmin(linalg.norm(self.walker.x-array(self.walker.hitGroupLoc),axis=1))].wid
				self.walker.currRun.stop(True)
				return True

		return False
	
	
#class kill(HC):
	
	##Init
	#def __init__(self,w,Id,edge):
		#super(kill, self).__init__(w,1,Id,edge)		