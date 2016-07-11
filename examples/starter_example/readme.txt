starter_example -- An example pipeline that should demonstrate ariadne's pipeline model.

Introduction:
Ariadne is effectively a wrapper for Luigi (a process management and execution tool) 
that integrates support for machine learning specific functionality. As such, Ariadne
should be used to run pipelines consisting of steps that make use of its machine 
learning functionality.

This pipeline should make use of the latest ariadne pipeline model and was written 
to demonstrate how it could be used in the real world.

How this pipeline works:
The example pipeline creates a directory tree and performs various tasks to illustrate
ariadne's dependency resolution system. 

The pipeline executes the following stages:

1. Directory creation - the mkdir plugin is invoked three times.
2. File creation - the makefile plugin is invoked twice.
3. Addition and file output - This is the top level plugin. it specifies all other plugins as its dependencies.
