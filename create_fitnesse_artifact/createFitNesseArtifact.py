#  MIT License
#
#  Copyright (c) 2020 Jac. Beekers
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.
#

"""
.. versionchanged:: 20200530.0
    * moved FitNesse to its own package
    * changes due to logging module changes
    * documentation
"""
__since__ = '23-OCT-2019'
__version__ = '20200530.0'
__author__ = 'Jac. Beekers'
__licence__ = 'MIT'
__url__ = 'https://github.com/consag/devops_fitnesse_tools'

import argparse
import datetime
import logging
import sys

import supporting.errorcodes as err
import supporting.generalSettings as generalsettings
from supporting.logging import customLogger

import create_fitnesse_artifact.helpers.artifact
from create_fitnesse_artifact.helpers import fitnesseArtifactChecks
from create_fitnesse_artifact.helpers import fitnesseSettings


# result = err.OK

class CreateFitNesseArtifact:

    def __init__(self, argv, log_on_console=True):
        self.now = datetime.datetime.now()
        self.arguments = argv
        self.main_proc = 'CreateFitNesseArtifact'
        self.log_on_console = log_on_console
        self.logger = logging.getLogger(__name__)
        self.custom_logger = customLogger.CustomLogger(self.main_proc, log_on_console)
        self.result_logger = customLogger.CustomLogger.configurelogger(self.custom_logger)
        self.fitnesse_settings = fitnesseSettings.FitNesseSettings()
        self.fitnesse_checks = fitnesseArtifactChecks.FitNesseArtifactChecks()
        self.result = err.OK

    def parse_the_arguments(self, arguments):
        """Parses the provided arguments and exits on an error.
        Use the option -h on the command line to get an overview of the required and optional arguments.

        Args:
            arguments: List containing command line arguments

        Returns:
            A list with validated command line arguments
        """
        parser = argparse.ArgumentParser(prog=self.main_proc)
        args = parser.parse_args(arguments)

        return args

    def runit(self, arguments):
        """Creates a FitNesse artifact, consisting on collected test directories and files
        It uses a deploy list that contains subdirectories.
        Module uses environment variables that steer the artifact creation.

        Args:
            arguments: The command line arguments (none actually at the moment)
        """
        thisproc = "runit"
        args = self.parse_the_arguments(arguments)
        logger = self.logger

        self.custom_logger.log(logger, logging.DEBUG, thisproc, 'Started')
        self.custom_logger.log(logger, logging.DEBUG, thisproc, 'logDir is >' + generalsettings.logDir + "<.")

        # Check requirements for artifact generation
        generalsettings.getenvvars()
        self.fitnesse_settings.getfitnesseenvvars()
        self.fitnesse_settings.outfitnesseenvvars()

        self.result = self.fitnesse_checks.fitnesse_artifact_checks(self.fitnesse_settings)
        if self.result.rc == err.IGNORE.rc:
            # deploylist is not mandatory since 2020-02-09
            self.custom_logger.log(logging, self.result.level, thisproc, 'Artifact ignored.')
            self.result = err.OK
        else:
            if self.result.rc != err.OK.rc:
                self.custom_logger.log(logger, logging.ERROR, thisproc,
                                       'FitNesse Artifact Checks failed with >' + self.result.message + "<.")
                self.custom_logger.writeresult(self.result_logger, self.result)
            else:
                builder = create_fitnesse_artifact.helpers.artifact.BuildFitNesseArtifact(self.fitnesse_settings
                                                                                          ,
                                                                                          self.fitnesse_settings.fitnessedeploylist)
                self.result = builder.processList()
                self.custom_logger.writeresult(self.result_logger, self.result)

        self.custom_logger.log(logger, logging.DEBUG, thisproc, 'Completed with return code >' + str(self.result.rc)
                               + '< and result code >' + self.result.code + "<.")
        #    supporting.writeresult(resultlogger, result)
        # supporting.exitscript(resultlogger, result)
        return self.result


if __name__ == '__main__':
    fitnesse = CreateFitNesseArtifact(sys.argv[1:], log_on_console=False)
    result = fitnesse.runit(fitnesse.arguments)
    fitnesse.custom_logger.exitscript(fitnesse.result_logger, result)
