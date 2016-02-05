import pyrw

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
w=rw.addWalker(BCtyp='setBack',typ='pred',HCtyp='stop',RWtyp='CCRW')

#Add 5 prey random walkers randomly across the domain
for i in range(5):
	w2=rw.addWalker(BCtyp='setBack',color='m',x0=[-5,1],typ='prey')
	w2.genRandomX0()

#Define walker of interest
rw.setVarForAllRuns('walkerOfInterest',w)

#Run RW
rw.runs[0].start(plotStep=True)

#Print Final statistic
rw.computeStatistics()
rw.printStatistics()

#Save everything to pickle file
#rw.saveToFile("myfirstrw.pk")


raw_input("Done, press [ENTER] to quit")

