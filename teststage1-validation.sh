#!/bin/bash

if [ -d testdir ]; then
	echo "Testdir exists!"
	exit 0
else
	echo "ERROR: Testdir doesn't exist."
	exit 1
fi
