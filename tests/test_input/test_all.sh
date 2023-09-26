#!/bin/bash
for FILE in *.py ; do
  echo "TESTING:" $FILE
  pytest $FILE
  [ $? -eq 0 ] || exit 1
done