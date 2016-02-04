import pickle
import platform

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
        
        
        	
	
        