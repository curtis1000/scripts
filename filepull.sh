#!/bin/bash

if [ -z $1 ]; then
        echo "Usage: filepull host path"
        exit 1
fi

if [ -z $2 ]; then
        echo "Usage: filepull host path"
        exit 1
fi

rsync -vre ssh $1:$2/* $2/
