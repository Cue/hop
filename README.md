hop
================

Navigate to common directories more easily.

Copyright 2011 by The hop Authors.


Installation
----------------

Due to the fact that hop must modify your bash settings to work, at this time it must be installed from source:

  git://github.com/Greplin/hop.git

  cd hop

	python setup.py install

If you do not have a virtualenv set up, you may need to run the last command using 'sudo'.

It's also only compatible with bash at this time.  Pull requests welcome.


Usage
-----------------

	hop -a /var/vhosts/mysite.com
	hop mysite.com
	hop m<tab>

	hop -a /var/vhosts/myothersite.com --as mos
	hop mos

	hop -s user@externalsite.com --as ext
	hop ext

	hop -a /try/just/using/a/unique/prefix
	hop p


Authors
-----------------
Greplin, Inc.
