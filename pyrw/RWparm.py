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

from numpy import *

class RWparm:

        def __init__(self,name,walker,startValue,endValue,steps=10,spacing='linear'):
                
                self.name=name
                self.walker=walker
                
                self.startValue=startValue
                
                self.endValue=endValue
                
                self.steps=steps
                
                self.spacing=spacing
                
                self.parmVec=linspace(self.startValue,self.endValue,self.steps)

                