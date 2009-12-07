#!/bin/bash

GO_PATH=`dirname $BASH_SOURCE`
PATH_OR_OUTPUT=`$GO_PATH/go.py $*`
if [ $? -eq 255 ]; then
  cd $PATH_OR_OUTPUT
else
  echo "$PATH_OR_OUTPUT"
fi

