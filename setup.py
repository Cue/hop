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

		bashrc_path = os.path.expanduser("~/.bashrc")

		# First check if the reference to hop.bash is already installed.
		bashrc = open(bashrc_path, "r")
		for line in bashrc:
			if line.find('/hop.bash') != -1:
				return
		bashrc.close()

		# If not, install the reference to hop.bash.
		source_command = 'source %s' % os.path.join(sys.prefix, 'hop', 'hop.bash')
		bashrc = open(bashrc_path, "a")
		bashrc.writelines([
			"\n",
			"# Initialize the 'hop' script\n",
			source_command,
			"\n"])
		bashrc.close()

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
      data_files=[('hop', ['hop/hop.bash', 'hop/hop.sh'])],
      entry_points = {
        'console_scripts': [
		  'hop-script = hop.hop:main'
        ]
      },
      cmdclass=dict(install_data=hop_install)
     )
