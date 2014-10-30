forestry-tools
==============

The scripts and associated ArcGIS custom toolbox in this repository are designed to facilitate silviculture workflows. Currently there are two tools to facilitating creation of sampling points covering the entire stand area ensuring uniform sampling, equal distribution and random distribution across a grid.

# Equal Distribution

Equal distribution distributes points across a uniform grid pattern, allowing you to independently control both vertical and horizontal spacing. The tool expects five parameter inputs, the input feature class, units of measure, vertical spacing, horizontal spacing, and the output feature class.

* **Input Stands Feature Class** - This is a polygon feature class delineating the stands you would like to creating sampling points for. It honors selected features. Hence, if you select stands either interactively, by attribute or by location, sample points will only be created inside the selected features.
