#!/bin/bash

HOP_PATH=`dirname $BASH_SOURCE`
PATH_OR_OUTPUT=`hop-script $*`
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
