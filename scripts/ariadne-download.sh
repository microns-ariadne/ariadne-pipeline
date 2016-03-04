#!/bin/sh

echo $1
#wget -q $1
curl -O -s $1
exit $?
