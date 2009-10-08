#!/bin/bash

PATH_OR_OUTPUT=`./go.py $*`
if [ $? -eq 255 ]; then
  cd $PATH_OR_OUTPUT
else
  echo "$PATH_OR_OUTPUT"
fi

