#Simple example script of predator chasing 5 prey in circular domain
#RW simulation stops of predator finds a prey.

import pyrw
import numpy as np

#Create RW
rw=pyrw.RWRW.RW()

#Grab domain
d=rw.domain

#Build circular domain
vcenter=d.addVertex([0,0])
c=d.addCircle(vcenter,35)

##Add run
r=rw.addNRuns(1)

#Draw domain
d.draw(ann=False)

#Add predator random walker to the middle of the circular domain
#w=rw.addWalker(BCtyp='setBack',typ='pred',HCtyp='stop',RWtyp='CCRW')
w=rw.addWalker(BCtyp='setBack',typ='pred',RWtyp='SCCRW')

w.step.setOrigGamma(0.8)
w.step.setGammaStep(0.3)
w.step.setGammaMin(0.2)


#w.step.set

##Add 5 prey random walkers randomly across the domain
#for i in range(5):
	#w2=rw.addWalker(BCtyp='setBack',color='m',x0=[-5,1],typ='prey')
	#w2.genRandomX0()

#Define walker of interest
rw.setVarForAllRuns('walkerOfInterest',w)

#Run RW







rw.runs[0].start(plotStep=False)

rw.runs[0].plotTraj()

traj=np.array(w.traj)

print traj.shape


raw_input()

#Print Final statistic
rw.computeStatistics()
rw.printStatistics()

raw_input()

raw_input("Done, press [ENTER] to quit")

