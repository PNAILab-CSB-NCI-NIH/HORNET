#!/bin/bash
for FOLDER in *; do
  if [ -f $FOLDER/test_all.sh ]; then
    cd $FOLDER
    ./test_all.sh
    [ $? -eq 0 ] || exit 1
    sleep 1
    cd ..
  fi
done
echo -e "\n-----------------------------------\n| Successfully ran all unittests. |\n-----------------------------------"