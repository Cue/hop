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

import os.path
import sys

from setuptools import setup
from distutils.command import install_data


class hop_install(install_data.install_data):
  def run(self):
    install_data.install_data.run(self)


    bash_options = ('~/.bashrc', '~/.bash_profile')
    bashrc_path = None
    for bash in bash_options:
      expanded = os.path.expanduser(bash)
      if os.path.isfile(expanded):
        bashrc_path = expanded
        break
    
    prefix = os.path.join(sys.prefix, 'hop')
    required_commands = {
      '/hop.bash':"# Initialize the 'hop' script\n source %s" % os.path.join(prefix, 'hop.bash'),
      'hop-lua-script':'# Define an entry point for the lua script version of hop\n'
                       'alias hop-lua-script="LUA_PATH=%s %s"' % (os.path.join(prefix, 'json.lua'),
                                                                  os.path.join(prefix, 'hop.lua'))
    }
    # First check if the reference to hop.bash is already installed.
    with open(bashrc_path, "r") as f:
      bashrc_content = f.read()
      for k in required_commands.keys():
        if k in bashrc_content:
          del required_commands[k]

    if required_commands:
      with open(bashrc_path, "a") as f:
        for v in required_commands.values():
          f.write(v + '\n')

    print
    print "Done.  Now type '. ~/.bashrc'.  Then type 'hop'."

    return True


setup(name='Hop',
      version='1.0',
      description='Easily jump to your favorite directories',
      license='Apache',
      author='Greplin',
      author_email='robbyw@greplin.com',
      url='http://www.github.com/Greplin/hop',
      packages=['hop'],
      data_files=[('hop', ['hop/hop.bash', 'hop/hop.sh', 'hop/hop.lua', 'hop/json.lua'])],
      entry_points = {
        'console_scripts': [
      'hop-python-script = hop.hop:main'
        ]
      },
      cmdclass=dict(install_data=hop_install)
     )
