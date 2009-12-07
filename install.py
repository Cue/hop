#!/usr/bin/python

import os.path
import sys

def install_hop():
	bashrc_path = os.path.expanduser("~/.bashrc")

	# First check if the reference to hop.bash is already installed.
	bashrc = open(bashrc_path, "r")
	for line in bashrc:
		if line.find('/hop.bash') != -1:
			print "ERROR: hop is already installed"
			return
	bashrc.close()
	
	# If not, install the reference to hop.bash.
	source_command = "source %s" % os.path.join(sys.path[0], 'hop.bash')
	bashrc = open(bashrc_path, "a")
	bashrc.writelines([
		"\n",
		"# Initialize the 'hop' script\n",
		source_command,
		"\n"])
	bashrc.close()
	
	print "Done.  Now type '. ~/.bashrc'.  Then type 'hop'."


if __name__ == "__main__":
	install_hop()