import RWRW
import RWBC
from numpy import *
import RWessentials as rwe
import matplotlib.pyplot as plt
import RWmisc

#Create RW
rw=RWRW.RW()

#Grab domain
d=rw.domain

#Build circular domain
vcenter=d.addVertex([0,0])
c=d.addCircle(vcenter,35)

#Add run
r=rw.addNRuns(3)

#Draw domain
#d.draw(ann=False)

#Add random walkers
w=rw.addWalker(BCtyp='setBack',typ='pred',HCtyp='stop',RWtyp='CCRW')

for i in range(5):
	w2=rw.addWalker(BCtyp='setBack',color='m',x0=array([-5,1]),typ='prey')
	w2.genRandomX0()

rw.setVarForAllRuns('walkerOfInterest',w)

rw.runAll(printProcess=True,printRunProcess=False)
rw.computeStatistics()
rw.printStatistics()

rw.saveToFile("bla.pk")

#print rw.getTotalRuntime()


#Start run
#r.start(plotStep=False)
#r.plotTraj()





raw_input()

