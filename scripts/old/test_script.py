from RW import *
import sys
#from domain import *

#d=domain

#print d.typ
	
#Create random walk
rw=RW()
print rw.tstart
print rw.domain.RW


#Build domain
#d=rw.domain

#print domain, type(domain)


raw_input()

d.add_vertex([10,10])
d.add_vertex([-10,10])
d.add_vertex([-10,-10])
d.add_vertex([10,-10])

for i in range(len(d.vertices)-1):
	d.add_edge(d.vertices[i],d.vertices[i+1])
d.add_edge(d.vertices[-1],d.vertices[0])	

#Add walkers
rw.add_walker(x0=[9,9])
rw.add_walker(color='b',x0=[5,0])
rw.add_walker(color='g',x0=[0,5])
rw.add_walker(color='y',x0=[5,5])

#Create run
run=rw.new_run()

#Draw domain
d.draw(ann=True)

#Scale plotting window
#xs=[]
#ys=[]
#for v in d.vertices:
#	xs.append(v.x[0])
#	ys.append(v.x[1])
#xmax=max(xs)
#ymax=max(xs)
#xmin=min(xs)
#ymin=min(xs)

#run.ax_traj.set_xlim([xmin-1,xmax+1])
#run.ax_traj.set_ylim([ymin-1,ymax+1])

run.scale_plot()

plt.draw()


#print rw.BC.seg_intersect(d.vertices[3].x,d.vertices[0].x,d.vertices[4].x,d.vertices[5].x)

raw_input()

run.start()
#raw_input()