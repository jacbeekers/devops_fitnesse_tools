import sys
import unittest
from pathlib import Path
from unittest.mock import patch

from supporting import errorcodes

from create_fitnesse_artifact.createFitNesseArtifact import CreateFitNesseArtifact
from create_fitnesse_artifact.helpers.fitnesseConstants import varFitNesseDeployList
from create_fitnesse_artifact.helpers.fitnesseConstants import varSourceFitNesseDir
from create_fitnesse_artifact.helpers.fitnesseConstants import varTargetFitNesseDir
from os.path import abspath

class TestFitNesseArtifact(unittest.TestCase):

    def setUp(self):
        self.fitnesse = CreateFitNesseArtifact(sys.argv[1:], log_on_console=True)

    def test_fitnesse_artifact_all_defaults(self):
        self.result = self.fitnesse.runit(self.fitnesse.arguments)
        assert self.result.rc == 0

    def run_test(self, deploylist='fitnesse_deploylist.txt', source_fitnesse='.', target_fitnesse='.'):
        self.deploylist = deploylist
        self.env = patch.dict('os.environ', {varFitNesseDeployList: self.deploylist
            , varSourceFitNesseDir: source_fitnesse
            , varTargetFitNesseDir: target_fitnesse})
        with self.env:
            self.assertTrue(Path(self.deploylist).exists(),
                            'File >' + self.deploylist + '< does not exist. Cannot test.')
            self.assertTrue(Path(source_fitnesse).exists(),
                            'Source FitNesse path >' + source_fitnesse + '< with full path >'+ abspath(Path(source_fitnesse)) + '< does not exist.')
            self.assertTrue(Path(target_fitnesse).exists(),
                            'Target FitNesse path >' + target_fitnesse + '< does not exist.')
            self.result = self.fitnesse.runit(self.fitnesse.arguments)
        return self.result

    def test_fitnesse_artifact_valid_deploylist_nonexisting_directory(self):
        self.deploylist = 'resources/fitnesse_deploylist_parsetests_nonexisting_directory.txt'
        self.result = self.run_test(self.deploylist)
        self.assertTrue(self.result.rc == errorcodes.DIRECTORY_NF.rc,
                        "The directory should not exist in this test case, which is error code="
                        + str(
                            errorcodes.DIRECTORY_NF.rc) + ". You may also want to check the error codes in the supporting package")

    def test_fitnesse_artifact_valid_deploylist_existing_directories(self):
        self.deploylist = 'resources/fitnesse_deploylist_parsetests_existing_directory.txt'
        self.result = self.run_test(self.deploylist)
        assert self.result.rc == 0

    def fitnesse_suite(self):
        suite = unittest.TestSuite()
        suite.addTest(TestFitNesseArtifact("test_fitnesse_artifact_all_defaults"))
        suite.addTest(TestFitNesseArtifact("test_fitnesse_artifact_valid_deploylist_nonexisting_directory"))
        suite.addTest(TestFitNesseArtifact("test_fitnesse_artifact_valid_deploylist_existing_directories"))
        return suite

    """
    Actual pages from a FitNesse installation
    """

    def test_fitnesse_product1(self):
        """
        Suite that is part of a folder and contains a test page
        Returns: success or not
        """
        self.deploylist = 'resources/fitnesse_product1_deploylist.txt'
        self.result = self.run_test(self.deploylist, source_fitnesse='../fitnesse/FitNesseRoot')
        assert self.result.rc == 0

    def test_basic_fixtures(self):
        """
        Suite that is part of a folder and contains a Suite and a Folder that contains a Suite
        Returns: success or not
        """
        self.deploylist = 'resources/fitnesse_allproducts_deploylist.txt'
        self.result = self.run_test(self.deploylist)
        assert self.result.rc == 0

    def fitnesse_product1_suite(self):
        suite = unittest.TestSuite()
        suite.addTest(TestFitNesseArtifact("test_fitnesse_product1"))
        return suite

    def fitnesse_all_products_suite(self):
        suite = unittest.TestSuite()
        suite.addTest(TestFitNesseArtifact("test_fitnesse_product1"))
        suite.addTest(TestFitNesseArtifact("test_basic_fixtures"))
        return suite
