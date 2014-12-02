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
    lyrStnds = os.path.join(dirThis, 'resources', 'StandsInventory.lyr')
    gdbSrtch = os.path.join(dirThis, 'resources', 'test_data.gdb')

    # overwrite previous outputs if they exist
    arcpy.env.overwriteOutput = True

    def test_random150by150_defaultUnits(self):

        forestryTools.postPointsByDimensionRandom(
            inputFeatures=self.lyrStnds,
            xGridSpacing=150,
            yGridSpacing=150,
            outputFeatureClass=os.path.join(self.gdbSrtch, 'random150by150default')
        )

    def test_random6by6_chains(self):

        forestryTools.postPointsByDimensionRandom(
            inputFeatures=self.lyrStnds,
            xGridSpacing=6,
            yGridSpacing=6,
            outputFeatureClass=os.path.join(self.gdbSrtch, 'random6by6chains'),
            inputUnitMeasure='Chains'
        )

    def test_regular150by150_defaultUnits(self):

        forestryTools.postPointsByDimension(
            inputFeatures=self.lyrStnds,
            xGridSpacing=150,
            yGridSpacing=150,
            outputFeatureClass=os.path.join(self.gdbSrtch, 'regular150by150default')
        )

    def test_regular6by6_chains(self):

        forestryTools.postPointsByDimensionRandom(
            inputFeatures=self.lyrStnds,
            xGridSpacing=6,
            yGridSpacing=6,
            outputFeatureClass=os.path.join(self.gdbSrtch, 'regular6by6chains'),
            inputUnitMeasure='Chains'
        )