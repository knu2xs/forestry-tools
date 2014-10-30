"""
Purpose:    Drop post points for stand sampling given polygons for input.
DOB:        28 Oct 2014
"""
__author__ = 'Joel McCune (http://github.com/knu2xs)'

# import modules
import arcpy
import os.path


def byDimension(inputFeatures, xGridSpacing, yGridSpacing, outputFeatureClass, inputUnitMeasure='Feet'):
    """
    :param inputFeatures: Input stands as selected features from a feature layer.
    :param xGridSpacing: The horizontal grid spacing.
    :param yGridSpacing: The vertical grid spacing.
    :param outputFeatureClass: Where to save the output post points.
    :param inputUnitMeasure: The unit of measure for grid spacing, either Meters or Feet
    :return: outFc: Path to the output feature class of post points.
    """

    # ensure grid spacings are int
    xGridSpacing = int(xGridSpacing)
    yGridSpacing = int(yGridSpacing)

    # set spatial reference to be the same as the input feature class
    sr = arcpy.Describe(inputFeatures).spatialReference
    arcpy.env.outputCoordinateSystem = sr

    # ensure the data is saved in a projected coordinate system
    if sr.projectionCode == 0:
        arcpy.AddError(
            'Your input stands feature class appears to only have a geographic coordinate system. ' +
            'It must have a projected coordinate system for this tool to work. ' +
            'Please project your stands feature class and try again.'
        )
        arcpy.ExecuteError()

    # assuming a feature is selected, create a layer only referencing these features
    standFc = arcpy.CopyFeatures_management(inputFeatures, os.path.join('in_memory', 'standTemp'))[0]

    # get the extent of the selection layer
    extent = arcpy.Describe(standFc).extent

    # ensure the unit of measure is either feet or meters
    if inputUnitMeasure.lower() != ('feet' or 'meters' or 'chains'):
        arcpy.AddError('Invalid unit of measure. Please specify either feet or meters for inputUnitMeasure.')
        arcpy.ExecuteError()

    # if the spatial reference unit of measure is meters
    if sr.linearUnitName == 'Meters':

        # and the input unit of measure is feet, convert to meters
        if inputUnitMeasure.lower() == 'feet':
            xGridSpacing *= 3.28084
            yGridSpacing *= 3.28084

        # and the input unit of measure is chains, convert to meters
        elif inputUnitMeasure.lower() == 'chains':
            xGridSpacing *= 20.1168
            yGridSpacing *= 20.1168

    # if the spatial reference unit of measure is feet
    elif sr.linearUnitName == 'Feet':

        # and the input dimensions are meters, convert to feet
        if inputUnitMeasure.lower() == 'meters':
            xGridSpacing *= 0.3048
            yGridSpacing *= 0.3048

        # and the input dimenstions are chains, convert to feet
        if inputUnitMeasure.lower() == 'chains':
            xGridSpacing *= 66
            yGridSpacing *= 66

    # set the origin to 1/2 of the grid spacing, effectively in the middle of what would be a grid cell
    origin = arcpy.Point(
        extent.XMin + (xGridSpacing / 2),
        extent.YMin + (yGridSpacing / 2)
    )

    # get number of points for width and height based on point being in middle of dimensional grid
    xCount = int((extent.width - xGridSpacing) / xGridSpacing + 1)
    yCount = int((extent.height - yGridSpacing) / yGridSpacing + 1)

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
    outFc = arcpy.CopyFeatures_management(postList, outputFeatureClass)

    # return the path to the output feature class
    return outFc

# call the function
byDimension(
    inputFeatures=arcpy.GetParameter(0),
    inputUnitMeasure=arcpy.GetParameterAsText(1),
    xGridSpacing=arcpy.GetParameterAsText(2),
    yGridSpacing=arcpy.GetParameterAsText(3),
    outputFeatureClass=arcpy.GetParameterAsText(4)
)