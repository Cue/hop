hop
================

Quickly navigate to common directories.

Copyright 2011 by The hop Authors.


Installation
----------------

Due to the fact that hop must modify your bash settings to work, at this time it must be installed from source:

    git clone git://github.com/Greplin/hop.git

    cd hop

    python setup.py install

    python setup.py install_data

If you do not have a virtualenv set up, you may need to run the last command using 'sudo'.

It's also only compatible with bash at this time.  Pull requests welcome.


Usage
-----------------

    # Add a dir
    hop -a /var/vhosts/mysite.com

    # Jump by basename
    hop mysite.com

    # Tab complete
    hop m<tab>

    # Or just use the shortest unique prefix (a la git)
    hop m

    # Use custom aliases
    hop -a /var/vhosts/myothersite.com --as mos
    hop mos

    # Add ssh shortcuts
    hop -s user@externalsite.com --as ext
    hop ext


Authors
-----------------
Greplin, Inc.

@jibs
