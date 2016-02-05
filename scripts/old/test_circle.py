#Script to test circular geometry for RWtoolbox

from RW import *
import sys

	
#Create random walk
rw=RW()

#Build domain
d=rw.domain

#Create run
run=rw.new_run()

vstart=d.add_vertex([-10,0])
vend=d.add_vertex([0,10])
vcenter=d.add_vertex([0,0])



a=d.add_arc(vstart,vcenter,vend=vend)

print "a.angle=",a.angle
print "a.angle_offset=",a.angle_offset
print "a.vstart.vid=",a.vstart.vid
print "a.vend.vid=",a.vend.vid



d.draw(ann=True)
run.scale_plot()
raw_input()

