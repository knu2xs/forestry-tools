"""
Purpose:    Drop post points for stand sampling given polygons for input.
DOB:        28 Oct 2014
"""
__author__ = 'Joel McCune (http://github.com/knu2xs)'
__license__ = "Apache"
__version__ = "2.0"
__maintainer__ = "Joel McCune"
__email__ = "joel.mccune+github@gmail.com"
__status__ = "Production"

# import modules
import arcpy
import os.path
import random


def byDimensionRandom(inputFeatures, xGridSpacing, yGridSpacing, outputFeatureClass, inputUnitMeasure='Feet'):
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
    if inputUnitMeasure.lower() != ('feet' or 'meters'):
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

        # and the input dimensions are chains, convert to feet
        if inputUnitMeasure.lower() == 'chains':
            xGridSpacing *= 66
            yGridSpacing *= 66

    # set the origin
    origin = arcpy.Point(extent.XMin, extent.YMin)

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

    # for every grid box horizontally
    for x in range(0, xCount):

        # set the x coordinate minimum to the column times spacing plus the origin coordinates
        boxXMin = x * xGridSpacing + origin.X

        # set the x coordinate maximum to the column plus one times spacing plus the origin coordinate
        boxXMax = (x + 1) * xGridSpacing + origin.X

        # for every post position vertically
        for y in range(0, yCount):

            # set the y coordinate minimum to the row times spacing plus the origin coordinates
            boxYMin = y * yGridSpacing + origin.Y

            # set the y coordinate maximum to the row plus one times spacing plus the origin coordinate
            boxYMax = (y + 1) * yGridSpacing + origin.Y

            # create polygon geometry for the current bounding box
            boxGeometry = arcpy.Polygon(
                arcpy.Array([
                    arcpy.Point(boxXMin, boxYMin),
                    arcpy.Point(boxXMin, boxYMax),
                    arcpy.Point(boxXMax, boxYMax),
                    arcpy.Point(boxXMax, boxYMin)
                ]),
            sr)

            # for every stand geometry
            for standGeom in standGeomList:

                # if any part of the current bounding box extent is within any part of the stand
                if boxGeometry.overlaps(standGeom) or boxGeometry.within(standGeom):

                    # create a geometry with just the overlap area
                    overlapGeom = standGeom.intersect(boxGeometry, 4)

                    # create a point geometry object with the same spatial reference as the rest of the data
                    thisPoint = arcpy.Point()
                    thisPointGeom = arcpy.PointGeometry(thisPoint, sr)

                    # while the point is not within the geometry of the stand, keep trying to create another point
                    while not thisPointGeom.within(overlapGeom):

                        # generate a random point within the overlap geometry extent
                        thisPoint.X = random.uniform(overlapGeom.extent.XMin, overlapGeom.extent.XMax)
                        thisPoint.Y = random.uniform(overlapGeom.extent.YMin, overlapGeom.extent.YMax)

                        # update the point geometry
                        thisPointGeom = arcpy.PointGeometry(thisPoint, sr)

                    # Now, with an intersecting point in hand, add it to the list
                    postList.append(thisPointGeom)

    # create output feature class from the array of points
    outFc = arcpy.CopyFeatures_management(postList, outputFeatureClass)

    # return the path to the output feature class
    return outFc

# call the function
byDimensionRandom(
    inputFeatures=arcpy.GetParameter(0),
    inputUnitMeasure=arcpy.GetParameterAsText(1),
    xGridSpacing=arcpy.GetParameterAsText(2),
    yGridSpacing=arcpy.GetParameterAsText(3),
    outputFeatureClass=arcpy.GetParameterAsText(4)
)