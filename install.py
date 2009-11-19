#!/usr/bin/python

import os.path
import sys

def install_go():
	bashrc_path = os.path.expanduser("~/.bashrc")

	# First check if the reference to go.bash is already installed.
	bashrc = open(bashrc_path, "r")
	for line in bashrc:
		if line.find('/go.bash') != -1:
			print "ERROR: go is already installed"
			return
	bashrc.close()
	
	# If not, install the reference to go.bash.
	source_command = "source %s" % os.path.join(sys.path[0], 'go.bash')
	bashrc = open(bashrc_path, "a")
	bashrc.writelines([
		"\n",
		"# Initialize the 'go' script\n",
		source_command,
		"\n"])
	bashrc.close()
	
	print "Done.  Now type '. ~/.bashrc'.  Then type 'go'."


if __name__ == "__main__":
	install_go()