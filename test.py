"""
Unit testing
"""
import unittest
import os.path
import arcpy
import forestryTools


class TestUsingLocalData(unittest.TestCase):

    # useful variables
    dirThis = os.path.dirname(__file__)
    fcTracts = r'D:\dev\forestry-tools\resources\data.gdb\Demographic_Layers__BDS__Tracts'
    lyrTracts = arcpy.MakeFeatureLayer_management(fcTracts, 'lyrTracts', "ID = '53033029204'")
    gdbSrtch = os.path.join(dirThis, 'resources', 'data.gdb')

    # overwrite previous outputs if they exist
    arcpy.env.overwriteOutput = True

    def test_random150by150_defaultUnits(self):

        forestryTools.postPointsByDimensionRandom(
            inputFeatures=self.lyrTracts,
            xGridSpacing=150,
            yGridSpacing=150,
            outputFeatureClass=os.path.join(self.gdbSrtch, 'random150by150default')
        )

    def test_random6by6_chains(self):

        forestryTools.postPointsByDimensionRandom(
            inputFeatures=self.lyrTracts,
            xGridSpacing=6,
            yGridSpacing=6,
            outputFeatureClass=os.path.join(self.gdbSrtch, 'random6by6chains'),
            inputUnitMeasure='Chains'
        )

    def test_regular150by150_defaultUnits(self):

        forestryTools.postPointsByDimension(
            inputFeatures=self.lyrTracts,
            xGridSpacing=150,
            yGridSpacing=150,
            outputFeatureClass=os.path.join(self.gdbSrtch, 'regular150by150default')
        )

    def test_regular6by6_chains(self):

        forestryTools.postPointsByDimension(
            inputFeatures=self.lyrTracts,
            xGridSpacing=6,
            yGridSpacing=6,
            outputFeatureClass=os.path.join(self.gdbSrtch, 'regular6by6chains'),
            inputUnitMeasure='Chains'
        )