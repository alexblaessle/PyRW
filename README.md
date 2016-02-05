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

The API of pyrw can be found [here](http://pyrw.readthedocs.org/en/latest/pyrw.html#submodules "toAPI")

