#!/bin/bash

HOP_PATH=`dirname $BASH_SOURCE`
PATH_OR_OUTPUT=`hop-script $*`
if [ $? -eq 255 ]; then
  cd $PATH_OR_OUTPUT
else
  echo "$PATH_OR_OUTPUT"
fi

