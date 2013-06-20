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

function hop
{
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
    cd "$THE_PATH"
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
}


_has_subdirectory()
{
	for subpath in $1/*; do
		[ -d "$subpath" ] && return 0
	done
	return 1
}

_add_slashes()
{
	local i index=0
	for i in ${COMPREPLY[@]}; do
		if _has_subdirectory $i; then
			COMPREPLY[index++]="$i/"
		else
			COMPREPLY[index++]="$i "
		fi
	done
}

_hop_complete()
{
	local cur prev
	COMPREPLY=()
	cur="${COMP_WORDS[COMP_CWORD]}"
	prev="${COMP_WORDS[COMP_CWORD-1]}"

	# TODO(robbywalker): Autocomplete of options when cur starts with -
	if [ "$prev" == "-S" ] || [ "$prev" == "--add-server-json" ]; then
		COMPREPLY=( $(compgen -f -- ${cur}) )
		_add_slashes
	elif [ "$prev" == "-a" ] || [ "$prev" == "--add" ]; then
		COMPREPLY=( $(compgen -d -- ${cur}) )
		_add_slashes
	else
		COMPREPLY=( $( compgen -W "`hop --autocomplete $cur`" -- ${cur} ) )
	fi
	return 0
}

complete -F _hop_complete -o nospace hop
