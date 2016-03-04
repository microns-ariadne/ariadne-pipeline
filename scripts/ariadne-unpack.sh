#!/bin/bash

file=$1
ext=$2

if [ "$ext" == ".tar" ]; then
	tar -xf $file
fi

if [ "$ext" == ".tar.gz" ]; then
	tar -xzf $file
fi

if [ "$ext" == ".tgz" ]; then
	tar -xzf $file
fi
