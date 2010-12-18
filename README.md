hop
================

A script to make navigating to common directories easy

Copyright 2010 by Pipelime, Inc.


Installation
----------------

	sudo python setup.py install
	sudo python setup.py install_hop

Usage
-----------------

    # Add a dir
	hop -a /var/vhosts/mysite.com
    # Jump by basename
	hop mysite.com
    # Tab complete
	hop m<tab> => hop mysite.com
    # Or just use the shortest unique prefix (a la git)
    hop m

    # Use custom aliases
	hop -a /var/vhosts/myothersite.com --as mos
	hop mos
	
    # Add ssh shortcuts
	hop -s user@externalsite.com --as ext
	hop ext
