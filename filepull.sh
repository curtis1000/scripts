#!/bin/bash

# This script mirrors files over ssh from a remote system to the local system, and it 
# makes the assumption that you want them placed in the same path.

if [ -z $1 ] || [ -z $2 ]; then
        echo "Usage: filepull.sh host path"
        exit 1
fi

rsync -vre ssh $1:$2/* $2/
