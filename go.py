#!/usr/bin/python
#
# Copyright 2009, Robby Walker
#
# go/go.py
# The directory shortcut command.


import anydbm
import errno
import optparse
import os
import os.path
import sys


def basename(path):
	"""Always returns a basename, even if a path ends with a slash."""
	(dir, basename) = os.path.split(path)
	if basename:
		return basename
	else:
		return os.path.basename(dir)


def command_add(options, args, db):
	"""Adds one or more directories to the set of shortcuts."""
	if not args:
		args = ['']
	
	if len(args) > 1 and options.add_as:
		print "--as cannot be specified for more than one path"
		sys.exit(1)
	
	count = 0
	for subdir in args:
		path = os.path.join(os.getcwd(), subdir)
		if os.path.isdir(path):
			name = options.add_as or basename(path)
			if name not in db:
				print "Adding '%s' as '%s'" % (path, name)
				db[name] = path
			elif db[name] != path:
				print "A shortcut for '%s' already exists.  Use go -r '%s' to remove it" % (name, name)
			else:
				print "No change to '%s'." % name
			
			count += 1
		else:
			print "'%s' is not a directory.  Ignoring." % path

	print "Created %d new shortcuts." % count
	return True


def command_go(options, args, db):
	if len(args) != 1:
		return False
	
	if args[0] in db:
		print db[args[0]]
		sys.exit(255)
	
	print "No shortcut named '%s' found." % args[0]
	# TODO(robbyw): Perform the GO
	
		
commands = {
	'add': command_add,
	'go': command_go
}


if __name__ == "__main__":
	parser = optparse.OptionParser(usage="usage: %prog [options] [directories]")
	
	group = optparse.OptionGroup(parser, "Adding paths")
	group.add_option("-a", "--add",
										dest="command",
										action="append_const",
										const="add",
	                  help="add shortcuts to the given directories.  when none are given, adds a shortcut to the current directory")
	group.add_option("--as",
										dest="add_as",
										help="specify a custom NAME for the new shortcut. Only works when creating only 1 shortcut.")
	parser.add_option_group(group)

	if len(sys.argv) == 1:
		parser.print_help()
		sys.exit(0)
		
	(options, args) = parser.parse_args()
	
	if not options.command or not len(options.command):
		# It's a request to go somewhere.
		command = 'go'
		
	elif len(options.command) > 1:
		# The user has specified multiple commands.
		print "Only one command can be run at a time.  You specified [%s]" % (','.join(options.command))
		sys.exit(1)
	
	else:
		command = options.command[0]

	if command in commands:
		db = anydbm.open(os.path.expanduser('~/.go'), 'c')
		if not commands[command](options, args, db):
			parser.print_help()
	else:
		print "Unknown command: %s" % command
	