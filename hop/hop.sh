#!/bin/bash

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


HOP_PATH=`dirname $BASH_SOURCE`
if command -v lua &>/dev/null; then
    PATH_OR_OUTPUT=`hop-lua-script $*`
else
    PATH_OR_OUTPUT=`hop-python-script $*`
fi

case $? in
  255 )
    read THE_NAME THE_PATH <<<$PATH_OR_OUTPUT
    echo -ne "\033]0;"$THE_NAME"\007"
    cd $THE_PATH
    ;;
  254 )
    read THE_NAME THE_SERVER <<<$PATH_OR_OUTPUT
    echo -ne "\033]0;"$THE_NAME"\007"
    ssh $THE_SERVER
    ;;
  *)
    echo "$PATH_OR_OUTPUT"
    ;;
esac
