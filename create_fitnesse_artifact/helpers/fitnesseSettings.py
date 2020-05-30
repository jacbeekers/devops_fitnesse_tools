#  MIT License
#
#  Copyright (c) 2019 Jac. Beekers
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

##
# fitnesseSettings
# @Since: 23-OCT-2019
# @Author: Jac. Beekers
# @Version: 20191023.0 - JBE - Initial
##

import logging
import os

import supporting.generalSettings as generalsettings
from supporting.generalSettings import completePath
from supporting.logging import customLogger

import create_fitnesse_artifact.helpers.fitnesseConstants as constants


class FitNesseSettings:

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.custom_logger = customLogger.CustomLogger('FitNesseSettings', True)
        self.source_fitnesse_directory = constants.DEFAULT_SOURCE_FITNESSEDIR
        self.target_fitnesse_directory = constants.DEFAULT_TARGET_FITNESSEDIR

    def getfitnesseenvvars(self):
        thisproc = "getfitnesseenvvars"
        self.custom_logger.log(self.logger, logging.DEBUG, thisproc, 'started')
        self.fitnessedeploylist = completePath(
            os.environ.get(constants.varFitNesseDeployList, constants.DEFAULT_FITNESSE_DEPLOYLIST),
            generalsettings.sourceDir)
        self.source_fitnesse_directory = completePath(
            os.environ.get(constants.varSourceFitNesseDir, constants.DEFAULT_SOURCE_FITNESSEDIR),
            generalsettings.sourceDir)
        self.target_fitnesse_directory = completePath(
            os.environ.get(constants.varTargetFitNesseDir, constants.DEFAULT_TARGET_FITNESSEDIR),
            generalsettings.sourceDir)

    def outfitnesseenvvars(self):
        thisproc = "outfitnesseenvvars"
        self.custom_logger.log(self.logger, logging.INFO, thisproc,
                               'fitnessedeploylist is >' + self.fitnessedeploylist + "<.")
        self.custom_logger.log(self.logger, logging.INFO, thisproc,
                               'sourcefitnessedir is >' + self.source_fitnesse_directory + "<.")
        self.custom_logger.log(self.logger, logging.INFO, thisproc,
                               'targetfitnessedir is >' + self.target_fitnesse_directory + "<.")
