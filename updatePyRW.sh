#!/bin/bash

#Build pyrw
sudo python setup.py install

#Update rst files
# sphinx-apidoc -e -P -o source/ ../build/lib.linux-x86_64-2.7/pyrw/ 
sphinx-apidoc -e -P -o docs/source/ pyrw/ 


#Build doc
cd docs
make html
cd ..

