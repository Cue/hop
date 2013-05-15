#!/usr/bin/env python
# Copyright 2011 The hop Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import anydbm
import optparse
import os
import os.path
import sys

try:
  import simplejson as json
except ImportError:
  import json



def basename(path):
  """Always returns a basename, even if a path ends with a slash."""
  (dir_, basename_) = os.path.split(path)
  if basename_:
    return basename_
  else:
    return os.path.basename(dir_)


def command_add_server(options, args, db):
  """Adds a server to the set of shortcuts."""
  server = args[0]
  store_as = '$server$%s' % server
  name = options.add_as or server
  if name not in db:
    print "Adding '%s' as '%s'." % (server, name)
    db[name] = store_as
  elif db[name] != store_as:
    print "A shortcut for '%s' already exists.  Use hop -r '%s' to remove it" % (name, name)
  else:
    print "No change to '%s'." % name
  return True


def command_add_server_json(options, args, db):
  """Adds a server to the set of shortcuts."""

  servers = json.loads(file(args[0]).read())
  for name, server in servers.items():
    store_as = '$server$%s' % server
    if name not in db:
      print "Adding '%s' as '%s'." % (server, name)
      db[name] = store_as
    elif db[name] != store_as:
      print "A shortcut for '%s' already exists.  Use hop -r '%s' to remove it" % (name, name)
    else:
      print "No change to '%s'." % name
  return True


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
        print "Adding '%s' as '%s'." % (path, name)
        db[name] = path
      elif db[name] != path:
        print "A shortcut for '%s' already exists.  Use hop -r '%s' to remove it" % (name, name)
      else:
        print "No change to '%s'." % name

      count += 1
    else:
      print "'%s' is not a directory.  Ignoring." % path

  print "Created %d new shortcuts." % count
  return True


def beginning_with(cmd, db):
  """Returns a list of commands that begin with the string cmd"""
  possibilities = []
  for shortcut in db.keys():
    if shortcut.startswith(cmd):
      possibilities.append(shortcut)
  return possibilities


def command_hop(options, args, db):
  """Prints the name of the directory implied by the shortcut."""
  if len(args) != 1:
    return False

  shortcut = False
  if args[0] in db:
    shortcut = args[0]
  else:
    possibilities = beginning_with(args[0], db)
    if len(possibilities) == 1:
      shortcut = possibilities[0]

  if shortcut:
    # Prints the name and path to cd / ssh to, hop.sh actually performs the cd or ssh.
    print shortcut
    value = db[shortcut]
    if value.startswith('$server$'):
      print value[8:]
      sys.exit(254)
    else:
      print db[shortcut]
      sys.exit(255)

  print "No shortcut named '%s' exists." % args[0]
  return True


def command_remove(options, args, db):
  """Removes the named shortcut from the set of shortcuts."""
  count = 0
  for shortcut in args:
    if shortcut in db:
      del db[shortcut]
      print "Removed shortcut '%s'." % shortcut
      count += 1
    else:
      print "No shortcut named '%s' exists." % shortcut
  print "Removed %d shortcuts." % count
  return True


def command_autocomplete(options, args, db):
  """Returns a list of shortcut names that start with the last argument"""
  prefix = ''
  if args:
    prefix = args[-1]
  for shortcut in beginning_with(prefix, db):
    print shortcut
  return True


def command_list(options, args, db):
  """Lists the available shortcuts."""
  for shortcut in sorted(db.keys()):
    print "%s => %s" % (shortcut, db[shortcut])
  return True


def command_convert(*_):
  """Convert the database"""
  hop_file = os.path.expanduser('~/.hop')
  if os.path.isfile('%s.db' % hop_file):
    db = anydbm.open(hop_file)
    x = {}
    for k in db.keys():
      x[k] = db[k]

    with open(os.path.expanduser('~/.hop.json.db'), 'w') as f:
      f.write(json.dumps(x))
  return True


commands = {
  'add': command_add,
  'add_server': command_add_server,
  'add_server_json': command_add_server_json,
  'autocomplete': command_autocomplete,
  'hop': command_hop,
  'remove': command_remove,
  'list': command_list,
  'convert':command_convert
}


def main():
  parser = optparse.OptionParser(usage="usage: hop [options] [directories/shortcuts]")

  group = optparse.OptionGroup(parser, "Adding shortcuts")
  group.add_option("-a", "--add",
                     dest="command",
                     action="append_const",
                     const="add",
                     help="add shortcuts to the given directories.  when none are given, adds a shortcut " +
                      "to the current directory")
  group.add_option("--as",
                     dest="add_as",
                     help="specify a custom NAME for the new shortcut. Only works when creating only 1 shortcut.")
  parser.add_option_group(group)

  group = optparse.OptionGroup(parser, "Adding SSH shortcuts")
  group.add_option("-s", "--add-server",
                     dest="command",
                     action="append_const",
                     const="add_server",
                     help="add shortcut to the given server. Can be used with --as (see above)")
  parser.add_option_group(group)

  group = optparse.OptionGroup(parser, "Adding multiple SSH shortcuts")
  group.add_option("-S", "--add-server-json",
                     dest="command",
                     action="append_const",
                     const="add_server_json",
                     help="add shortcuts to the given servers.")
  parser.add_option_group(group)

  group = optparse.OptionGroup(parser, "Removing shortcuts")
  group.add_option("-r", "--remove",
                     dest="command",
                     action="append_const",
                     const="remove",
                     help="remove shortcuts with the given names")
  parser.add_option_group(group)

  group.add_option("-c", "--convert",
                     dest="command",
                     action="append_const",
                     const="convert",
                     help="convert the datastore")
  parser.add_option_group(group)

  group = optparse.OptionGroup(parser, "Listing available shortcuts")
  group.add_option("-l", "--list",
                   dest="command",
                     action="append_const",
                     const="list",
                     help="list all shortcuts")
  parser.add_option_group(group)

  parser.add_option("--autocomplete",
                     dest="command",
                     action="append_const",
                     const="autocomplete",
                     help=optparse.SUPPRESS_HELP)

  if len(sys.argv) == 1:
    # Print the help when called with no arguments.
    parser.print_help()
    sys.exit(0)

  (options, args) = parser.parse_args()

  if not options.command or not len(options.command):
    # It's a request to hop somewhere.
    command = 'hop'

  elif len(options.command) > 1:
    # The user has specified multiple commands.
    print "Only one command can be run at a time.  You specified [%s]" % (','.join(options.command))
    sys.exit(1)

  else:
    command = options.command[0]

  if command in commands:
    db = JsonDbm(os.path.expanduser('~/.hop.json.db'))
    db.read()
    if not commands[command](options, args, db):
      parser.print_help()
  else:
    print "Unknown command: %s" % command



class JsonDbm(object):
  """A dbm-like object that writes to disk on every setattr.
  Only works for very simple datastorage cases.
  """


  def __init__(self, path):
    self._path = path
    self._cache = None


  def read(self):
    """Read the file"""
    try:
      with open(self._path, 'r') as f:
        self._cache = json.loads(f.read())
    except IOError:
      self._cache = {}


  def _write(self, values):
    """Write the file to disk"""
    with open(self._path, 'w') as f:
      f.write(json.dumps(values))


  def __getitem__(self, item):
    if not self._cache:
      self.read()
    return self._cache[item]


  def __setitem__(self, key, value):
    self._cache[key] = value
    self._write(self._cache)


  def __contains__(self, item):
    return item in self._cache


  def __len__(self):
    return len(self._cache)


  def __delitem__(self, key):
    del self._cache[key]
    self._write(self._cache)


  def keys(self):
    """Return the keys"""
    return self._cache.keys()

if __name__ == '__main__':
  main()
