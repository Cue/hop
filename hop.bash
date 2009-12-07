#!/bin/bash

GO_PATH=$(cd `dirname $BASH_SOURCE` && pwd)
alias go=". $GO_PATH/go.sh"

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

_go_complete()
{
	local cur prev
	COMPREPLY=()
	cur="${COMP_WORDS[COMP_CWORD]}"
	prev="${COMP_WORDS[COMP_CWORD-1]}"
	
	# TODO(robbywalker): Autocomplete of options when cur starts with -
	if [ "$prev" == "-a" ] || [ "$prev" == "--add" ]; then
		COMPREPLY=( $(compgen -d -- ${cur}) )
		_add_slashes
	else
		COMPREPLY=( $( compgen -W "`go --autocomplete $cur`" -- ${cur} ) )
	fi
	return 0
}

complete -F _go_complete -o nospace go
