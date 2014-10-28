__author__ = 'Joel McCune (http://github.com/knu2xs)'

# import modules
import arcpy
import os.path

# variables
inputFeatures = arcpy.GetParameterAsText(0)
outputWorkspace = arcpy.GetParameterAsText(1)
xGridSpacing = arcpy.GetParameterAsText(2)
yGridSpacing = arcpy.GetParameterAsText(3)
inputUnitMeasure = 'Foot'

# set spatial reference to be the same as the input feature class
sr = arcpy.Describe(inputFeatures).spatialReference
arcpy.env.outputCoordinateSystem = sr

# assuming a feature is selected, create a layer only referencing these features
standFc = arcpy.arcpy.CopyFeatures_management(inputFeatures, 'standTemp')[0]

# get the extent of the selection layer
extent = arcpy.Describe(standFc).extent

# if the spatial reference unit of measure is meters and the input dimensions are feet, convert to meters
if sr.linearUnitName == 'Meters' and inputUnitMeasure == 'Feet':
    xGridSpacing *= 3.28084
    yGridSpacing *= 3.28084

# set the origin to 1/2 of the grid spacing, effectively in the middle of what would be a grid cell
origin = arcpy.Point(extent.XMin + 0.5 * xGridSpacing, extent.YMin + 0.5 * yGridSpacing)

# get number of points for width and height based on point being in middle of dimensional grid
xCount = (extent.witdh - xGridSpacing) / xGridSpacing
yCount = (extent.height - yGridSpacing) / yGridSpacing

# point array to populate
postArray = arcpy.Array()

# list of input polygon geometries
standGeomList = []

# get geometry object from the input feature
with arcpy.da.SearchCursor(inputFeatures, 'SHAPE@') as cursor:
    for row in cursor:
        standGeomList.append(row[0])

# for every post position horizontally
for x in range(1, xCount):

    # set the x coordinate to the column times spacing plus the origin coordinates
    xCoord = x * xGridSpacing + origin.X

    # for every post position vertically
    for y in range(1, yCount):

        # set the y coordinate to the row times spacing plus the origin coordinates
        yCoord = y * yGridSpacing + origin.Y

        # create point object
        thisPost = arcpy.Point(xCoord, yCoord)

        # for every stand geometry
        for standGeom in standGeomList:

            # if the current post is within the stand polygon
            if thisPost.within(standGeom):

                # add the post to the array
                postArray.append(thisPost)

                # stop and break out of the current for loop
                break

# create output feature class from the array of points
outFc = arcpy.CopyFeatures_management(postArray, os.path.join(outputWorkspace, 'standSamplePosts'))