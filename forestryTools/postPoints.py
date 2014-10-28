"""
Purpose:        Drop post points for stand sampling given polygons for input.
DOB:            28 Oct 2014
"""
__author__ = 'Joel McCune (http://github.com/knu2xs)'

# import modules
import arcpy
import os.path
import sys


def byDimension(inputFeatures, outputWorkspace, xGridSpacing, yGridSpacing, inputUnitMeasure='Foot'):
    """
    :param inputFeatures: Input stands as selected features from a feature layer.
    :param outputWorkspace: Where to save the output post points.
    :param xGridSpacing: The horizontal grid spacing.
    :param yGridSpacing: The vertical grid spacing.
    :param inputUnitMeasure: The unit of measure for grid spacing, either Meters or Feet
    :return: outFc: Path to the output feature class of post points.
    """

    # set spatial reference to be the same as the input feature class
    sr = arcpy.Describe(inputFeatures).spatialReference
    arcpy.env.outputCoordinateSystem = sr

    # assuming a feature is selected, create a layer only referencing these features
    standFc = arcpy.arcpy.CopyFeatures_management(inputFeatures, 'standTemp')[0]

    # get the extent of the selection layer
    extent = arcpy.Describe(standFc).extent

    # ensure the unit of measure is either feet or meters
    if inputUnitMeasure != ('Feet' or 'feet' or 'Meters' or 'meters'):
        arcpy.AddError('Invalid unit of measure. Please specify either feet or meters for inputUnitMeasure.')
        arcpy.ExecuteError()

    # if the spatial reference unit of measure is meters and the input dimensions are feet, convert to meters
    if sr.linearUnitName == 'Meters' and (inputUnitMeasure == 'Feet' or inputUnitMeasure == 'feet'):
        xGridSpacing *= 3.28084
        yGridSpacing *= 3.28084

    # if the spatial reference unit of measure is feet and the input dimensions are meters, convert to feet
    elif sr.linearUnitName == 'Feet' and (inputUnitMeasure != 'Meters' or inputUnitMeasure != 'meters'):
        xGridSpacing /= 3.28084
        yGridSpacing /= 3.28084

    # set the origin to 1/2 of the grid spacing, effectively in the middle of what would be a grid cell
    origin = arcpy.Point(
        extent.XMin + (xGridSpacing / 2),
        extent.YMin + (yGridSpacing / 2)
    )

    # get number of points for width and height based on point being in middle of dimensional grid
    xCount = int((extent.width - xGridSpacing) / xGridSpacing)
    yCount = int((extent.height - yGridSpacing) / yGridSpacing)

    # point list to populate
    postList = []

    # list of input polygon geometries
    standGeomList = []

    # get geometry object from the input feature
    with arcpy.da.SearchCursor(inputFeatures, 'SHAPE@') as cursor:
        for row in cursor:
            standGeomList.append(row[0])

    # for every post position horizontally
    for x in range(0, xCount):

        # set the x coordinate to the column times spacing plus the origin coordinates
        xCoord = x * xGridSpacing + origin.X

        # for every post position vertically
        for y in range(0, yCount):

            # set the y coordinate to the row times spacing plus the origin coordinates
            yCoord = y * yGridSpacing + origin.Y

            # create point geometry object from coordinates
            thisPost = arcpy.PointGeometry(arcpy.Point(xCoord, yCoord), sr)

            # for every stand geometry
            for standGeom in standGeomList:

                # if the current post is within the stand polygon
                if thisPost.within(standGeom):

                    # add the post to the array
                    postList.append(thisPost)

                    # stop and break out of the current for loop
                    break



    # create output feature class from the array of points
    outFc = arcpy.CopyFeatures_management(postList, os.path.join(outputWorkspace, 'standSamplePosts'))[0]

    # return the path to the output feature class
    return outFc

if __name__ == '__main__':
    inputFeatures = sys.argv[0]
    outputWorkspace = sys.argv[1]
    xGridSpacing = sys.argv[2]
    yGridSpacing = sys.argv[3]
    byDimension(inputFeatures, outputWorkspace, xGridSpacing, yGridSpacing)