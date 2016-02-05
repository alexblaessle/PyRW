# PyRW
A Python based 2D random walk simulation tool box

## Features

- Allows any type of 2D domain out of different geometrical features  
- Allows for any type of random walker, since random walks can be stacked upon each other as superpositions,such as 
	+ Brownian Walker
	+ Correlated Random Walker
	+ Composite Random Walker
	+ Correlated Composite Random Walker
- Each random walker can respond to each geometrical feature differently with various implemted boundary conditions
- Each random walker can respond to any other random walker differently with various implemted hitting conditions
- Live plotting
- Final Statistics

# Getting Started

## Installation

If you have Python2.7 already installed, simply obtain PyRW

	git clone https://github.com/alexblaessle/PyRW
	
and install via:

	python setup.py install

### Requirements

PyRW only depends on 

- numpy>=1.8.2
- matplotlib>=1.4.3
- pickle

and a bunch of standard Python2.7 libraries such as

- time
- platform
- sys

## API

The API of pyrw can be found [here](http://pyrw.readthedocs.org/en/latest/pyrw.html#submodules "toAPI") .

## Documentation

The Documentation of pyrw can be found [here](http://pyrw.readthedocs.org/en/latest/pyrw.html "toAPI") .

## Example
'''python
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

	raw_input("Done, press [ENTER] to quit")
'''