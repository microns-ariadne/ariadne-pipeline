#!/bin/bash

echo $1
olddir=`pwd`

if [ "$2" != "" ]; then
	if [ ! -d "$2" ]; then
		mkdir -p $2
	fi

	cd $2
fi

curl -O -s $1
status=$?
cd $olddir

exit $status
