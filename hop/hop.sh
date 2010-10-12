#!/bin/bash

HOP_PATH=`dirname $BASH_SOURCE`
PATH_OR_OUTPUT=`hop-script $*`
case $? in
  255 )
    cd $PATH_OR_OUTPUT
    ;;
  254 )
    ssh $PATH_OR_OUTPUT
    ;;
  *)
    echo "$PATH_OR_OUTPUT"
    ;;
esac
