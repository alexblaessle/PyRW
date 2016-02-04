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

                