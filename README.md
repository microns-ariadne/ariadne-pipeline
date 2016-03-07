# ariadne-pipeline - Process and software pipeline management tool.

NOTE: ariadne-pipeline is still under development and testing. Overall behavior is mostly stable, but internal APIs and plugin specifications are subject to change.

## Plugin API

Ariadne is ultimately a coordinator for a large number of plugins. As such, it is often necessary to develop new plugins to design different pipelines or just to fit different needs. 

Presently, there are three plugin interfaces:
1. ariadneplugin.Plugin -- A generic executable plugin designed as a building block for pipelines.
2. ariadneplugin.DatasetPlugin -- A plugin intended to wrap and abstract various dataset operations.
3. ariadneplugin.ArchivePlugin -- A plugin that wraps an archive utility.

###### ariadneplugin.Plugin


