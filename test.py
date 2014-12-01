"""
Unit testing
"""
import unittest
import os.path
import arcpy
import forestryTools

class TestUsingFeatureService(unittest.TestCase):

    # useful variables
    dirThis = os.path.dirname(__file__)
    lyrStnds = os.path.join(dirThis, 'resources', 'StandsInventory.lyr')
    gdbSrtch = os.path.join(dirThis, 'resources', 'test_data.gdb')

    # overwrite previous outputs if they exist
    arcpy.env.overwriteOutput = True

    def test_150by150_defaultUnits(self):

        forestryTools.postPointsByDimensionRandom(
            inputFeatures=self.lyrStnds,
            xGridSpacing=150,
            yGridSpacing=150,
            outputFeatureClass=os.path.join(self.gdbSrtch, 'random150by150default'),
            inputUnitMeasure='Feet'
        )

    def test_3by3_chains(self):

        forestryTools.postPointsByDimensionRandom(
            inputFeatures=self.lyrStnds,
            xGridSpacing=3,
            yGridSpacing=3,
            outputFeatureClass=os.path.join(self.gdbSrtch, 'random6by6chains'),
            inputUnitMeasure='Chains'
        )