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

class simulation:
	
	def __init__(self,domainType='circle',NRuns=50):
                
                self.RWs=[]
                
                self.RWParmsVaried={}
                
                self.EnvParmsVaried={}
                
                self.domainType=domainType
                
                self.NRuns=NRuns
                
                #self.
        
        def createRWs(self):
                
                parmCombinations=self.combinations(self.RWParmsVaried)
                
                for comb in parmCombinations:

                        #Create RW
                        rw=RWRW.RW()

                        #Grab domain
                        d=rw.domain
                        
                        #Build circular domain
                        if self.domainType=='circle':
                                vcenter=d.addVertex([0,0])
                                c=d.addCircle(vcenter,35)

                        #Add run
                        r=rw.addNRuns(self.NRuns)
                                     
        def combinations(self,parms,out=None):
                
                #Grab parmvecs
                arrays=[]
                for parm in parms:
                        arrays.append(parm.parmVec)
                        
                #Convert all arrays to np arrays
                arrays = [np.asarray(x) for x in arrays]
                
                #Bring to same dtype
                dtype = arrays[0].dtype
                
                #Compute number of combinations
                n = np.prod([x.size for x in arrays])
                
                #Create output array if None is given
                if out is None:
                        out = np.zeros([n, len(arrays)], dtype=dtype)
                
                #Compute size of repeats
                m = n / arrays[0].size
                out[:,0] = np.repeat(arrays[0], m)
                
                #Check if there is another array to go through
                if arrays[1:]:
                        
                        #Recursively call combinations again
                        combinations(arrays[1:], out=out[0:m,1:])
                        
                        #Append results
                        for j in xrange(1, arrays[0].size):
                                out[j*m:(j+1)*m,1:] = out[0:m,1:]
                
                return out
                