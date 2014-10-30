forestry-tools
==============

The scripts and associated ArcGIS custom toolbox in this repository are designed to facilitate silviculture workflows. Currently there are two tools facilitating creation of sampling points covering the entire stand area to ensure uniform sampling; equal distribution and random distribution across a grid.

## Equal Distribution

Equal distribution distributes points across a uniform grid pattern, allowing you to independently control both vertical and horizontal spacing. This methodology facilitates uniform sampling across the stand area.

The tool expects five parameter inputs; the input feature class, units of measure, vertical spacing, horizontal spacing, and the output feature class.

* **Input Stands Feature Class** - This is a polygon feature class delineating the stands you would like to creating sampling points for. It honors selected features. Hence, if you select stands either interactively, by attribute or by location, sample points will only be created inside the selected features. Also, the spatial reference for this feature class must be a projected coordinate system.

* **Units of Measure** (not yet implemented) - This is the linear unit of measure defining the sample point spacing. It can be either feet, meters or chains. The default is feet.

* **Vertical Spacing Distance** - This is the linear spacing distance for the vertical or x axis. The default unit of measure is feet.

* **Horizontal Spacing Distance** - This is the linear spacing distance for the horizontal or y axis. The default unit of measure is feet.

* **Output Feature Class** - This is the location and name of the points feature class to be created by the tool.

## Random Points Within Grid

This tool creates a grid across the area of the selected stands. Inside each of the grid areas it places a randomly distributed point inside of the stand. Hence if you specify 110 x 110 ft. grid spacing. The tool will create a grid across your stand areas with each grid area covering 110 x 100 ft. Inside of each of these 110 x 110 ft. areas, it will randomly place one sampling point. This methodology achieves both a uniform and random sampling of the stand areas.

Similar to the Equal Distribution tool, the Random Points Within Grid tool expects five parameter inputs; the input feature class, units of measure, vertical spacing, horizontal spacing, and the output feature class

* **Units of Measure** (not yet implemented) - This is the linear unit of measure defining the sample point spacing. It can be either feet, meters or chains. The default is feet.

* **Vertical Spacing Distance** - This is the linear spacing distance for the grid's vertical or x axis. The default unit of measure is feet.

* **Horizontal Spacing Distance** - This is the linear spacing distance for the grid's horizontal or y axis. The default unit of measure is feet.

* **Output Feature Class** - This is the location and name of the points feature class to be created by the tool.
