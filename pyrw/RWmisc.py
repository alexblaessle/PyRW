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

#Misc
import pickle
import platform
import csv

#===========================================================================
#Module description
#===========================================================================

"""
Miscellaneous module of pyrw containing functions for IO, printing etc., including 
the following functions:

(1) printVariable
(2) setVariable
(3) saveToPickle
(4) loadFromPickle
(5) listToCSV
"""

#===========================================================================
#Module functions
#===========================================================================

def printVariable(var,obj):
        print var, " = ", vars(obj)[str(var)]
        return var

def setVariable(var,obj,val):
        vars(obj)[str(var)]=val
        return val

def saveToPickle(obj,fn=None):

        if fn==None:
                if hasattr(obj,"name"):
                        fn=obj.name+".pk"
                else:
                        fn="unnamed"+".pk"
                
        with open(fn, 'wb') as output:
                pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)
        
        return fn

def loadFromPickle(fn):
        if platform.system() in ["Darwin","Linux"]:
                filehandler=open(fn, 'r')
        elif platform.system() in ["Windows"]:
                filehandler=open(fn, 'rb')
                
        loadedFile=pickle.load(filehandler)
        
        return loadedFile


def listToCSV(l,fn=None):
        wfile=csv.writer(open(fn_save,'wb'), delimiter=';')
        wfile.writerow(l)
        wfile.close()
        
        
        	
	
        