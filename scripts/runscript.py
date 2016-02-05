import RWRW
import RWBC
from numpy import *
import RWessentials as rwe
import matplotlib.pyplot as plt
import RWmisc
import sys
import time

#Movement parameters
gammaVec=arange(0.,1.,0.2)
rVec=arange(1,10,2)
kappaVec=arange(1,4,2)

#Generate combinations
parmCombs=rwe.combinations([rVec,gammaVec,kappaVec])

#Initial positions
nInitPos=1

#Runs
nRuns=1

#Number of prey
NPrey=10

#Bookkeeping array
RWs=[]

#Domain radius
RDomain=35

#Maximum number of timesteps
tMax=100000

tInit=[]
tSim=[]
tPost=[]

tStartAll=time.clock()

#Vary movement parameters
for k,parm in enumerate(parmCombs):
        
        #Vary initial position
        for j in range(nInitPos):
                
                tStart=time.clock()
                
                #Create RW
                rw=RWRW.RW(tend=tMax)

                #Grab domain
                d=rw.domain

                #Build circular domain
                vcenter=d.addVertex([0,0])
                c=d.addCircle(vcenter,RDomain)

                #Add run
                r=rw.addNRuns(nRuns)

                #Add predator
                w=rw.addWalker(BCtyp='setBack',typ='pred',HCtyp='stop',RWtyp='CCRW',successRate=0.8,detectRadius=1)
                
                #Add Prey and randomize initial position
                for i in range(NPrey):
                        w2=rw.addWalker(BCtyp='setBack',color='m',x0=array([-5,1]),typ='prey')
                        w2.genRandomX0()
                
                #Define important walker
                rw.setVarForAllRuns('walkerOfInterest',w)

                #Define movement parameters of predator
                w.step.setParms(parm)
                
                tInit.append(time.clock()-tStart)
                tStart=time.clock()
                
                #Run all runs
                rw.runAll(printProcess=False,printRunProcess=False)
                
                tSim.append(time.clock()-tStart)
                tStart=time.clock()
                
                rw.computeStatistics()
                #rw.printStatistics()

                RWs.append(rw)

                #rw.saveToFile("results/test/RW"+"_R"+str(RDomain)+"_IC"+str(j)+'_r'+str(nRuns)+'_t'+str(tMax)+'_rat'+str(parm[0])+'_gamma'+str(parm[1])+'_kappa'+str(parm[2])+".pk")
                
                tPost.append(time.clock()-tStart)
                
                
        #Print process
        currPerc=floor(float(k)/float(len(parmCombs))*100)
        sys.stdout.write("\r%d%%" %currPerc)  
        sys.stdout.flush()

tTotal=time.clock()-tStartAll

rts=[]

tStep=[]
tBC=[]
tHC=[]
tTraj=[]

for rw in RWs:        
        rts.append(rw.getTotalRuntime())
        
        tStep.append(rw.totaltStep)
        tHC.append(rw.totaltHC)
        tBC.append(rw.totaltBC)
        tTraj.append(rw.totaltTraj)
        
print "Mean Runtimes:" , mean(rts)
print "Sum Runtimes:" , sum(rts)
print "%tinit:", sum(tInit)/tTotal*100
print "%tSim:", sum(tSim)/tTotal*100
print "%tPost:", sum(tPost)/tTotal*100

print "%tStep:", sum(tStep)/sum(rts)*100
print "%tBC:", sum(tBC)/sum(rts)*100
print "%tHC:", sum(tHC)/sum(rts)*100
print "%tTraj:", sum(tTraj)/sum(rts)*100

x=arange(len(rts))
plt.plot(x,rts)
plt.show()

raw_input()

