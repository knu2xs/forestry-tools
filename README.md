forestry-tools
==============

The scripts and associated ArcGIS custom toolbox in this repository are designed to facilitate silviculture workflows. Currently there are two tools facilitating creation of sampling points covering the entire stand area to ensure uniform sampling; equal distribution and random distribution across a grid. This set of tools is licensed under an Apache 2.0 license.

If you find this toolbox useful, please contribute to it. Every open source project, big or small, is the product of people contributing to it. You can contribute by developing and also contributing to the documentation. Please feel free to [fork this project](https://help.github.com/articles/fork-a-repo/), add additional tools and functionality, and submit a [pull requrest](https://help.github.com/articles/using-pull-requests/). If you do not code, but understand the methology and science tools, please feel free to flesh out or clarify the documentation both in the toolbox, and also in the repository, either in this readme or in the [wiki] (https://github.com/knu2xs/forestry-tools/wiki).

## Create Points with Constant Spacing

Equal distribution distributes points across a uniform grid pattern, allowing you to independently control both vertical and horizontal spacing. This methodology facilitates uniform sampling across the stand area.

The tool expects five parameter inputs; the input feature class, units of measure, vertical spacing, horizontal spacing, and the output feature class.

* **Input Stands Feature Class** - This is a polygon feature class delineating the stands you would like to creating sampling points for. It honors selected features. Hence, if you select stands either interactively, by attribute or by location, sample points will only be created inside the selected features. Also, the spatial reference for this feature class must be a projected coordinate system.

* **Grid Unit of Measure** - This is the linear unit of measure defining the sample point grid spacing. It can be either feet, meters or chains. The default is feet.

* **X Grid Spacing** - This is the linear spacing distance for the horizontal or x axis. The default unit of measure is feet.

* **Y Grid Spacing** - This is the linear spacing distance for the vertical or y axis. The default unit of measure is feet.

* **Output Feature Class** - This is the location and name of the points feature class to be created by the tool.

## Create Points Randomly in Grid

This tool creates a grid across the area of the selected stands. Inside each of the grid areas it places a randomly distributed point inside of the stand. Hence if you specify 110 x 110 ft. grid spacing. The tool will create a grid across your stand areas with each grid area covering 110 x 100 ft. Inside of each of these 110 x 110 ft. areas, it will randomly place one sampling point. This methodology achieves both a uniform and random sampling of the stand areas.

Similar to the Equal Distribution tool, the Random Points Within Grid tool expects five parameter inputs; the input feature class, units of measure, vertical spacing, horizontal spacing, and the output feature class.

* **Input Stands Feature Class** - This is a polygon feature class delineating the stands you would like to creating sampling points for. It honors selected features. Hence, if you select stands either interactively, by attribute or by location, sample points will only be created inside the selected features. Also, the spatial reference for this feature class must be a projected coordinate system.

* **Units of Measure** (not yet implemented) - This is the linear unit of measure defining the sample point spacing. It can be either feet, meters or chains. The default is feet.

* **X Spacing Distance** - This is the linear spacing distance for the grid's horizontal or x axis. The default unit of measure is feet.

* **Y Spacing Distance** - This is the linear spacing distance for the grid's vertical or y axis. The default unit of measure is feet.

* **Output Feature Class** - This is the location and name of the points feature class to be created by the tool.


## Apache License 2.0

Copyright 2014 Joel McCune

Licensed under the Apache License, Version 2.0 (the "License"); you may not use the scripts and tools in this repository except in compliance with the License. A copy of the License is included in this repository or you may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. Please, see the License for the specific language governing permissions and limitations under the License.