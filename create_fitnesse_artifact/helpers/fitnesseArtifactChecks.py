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
# FitNesse Artifact Checks
# @Since: 23-OCT-2019
# @Author: Jac. Beekers
# @Version: 20191023.0 - JBE - Initial

import logging
from pathlib import Path

import supporting.errorcodes as err
from supporting.logging import customLogger


class FitNesseArtifactChecks:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.custom_logger = customLogger.CustomLogger('FitNesseArtifactChecks', True)

    def fitnesse_artifact_checks(self, fitnesse_settings):
        thisproc = "fitnesseartifactchecks"
        self.custom_logger.log(self.logger, logging.DEBUG, thisproc, 'started')
        result = err.OK

        if not fitnesse_settings.fitnessedeploylist:
            self.custom_logger.log(self.logger, err.IGNORE.level, thisproc, err.NO_DEPLOYLIST.message)
            self.custom_logger.log(self.logger, err.IGNORE.level, thisproc,
                                   "Assuming FitNesse is NOT part of the solution.")
            result = err.IGNORE
        else:
            deploylistFile = Path(fitnesse_settings.fitnessedeploylist)
            if not deploylistFile.is_file():
                self.custom_logger.log(self.logger, err.IGNORE.level, thisproc,
                                       "fitnessedeploylist is >" + fitnesse_settings.fitnessedeploylist + "<. "
                                       + err.DEPLOYLIST_NF.message + " - FitNesse artifact IGNORED.")
                result = err.IGNORE

        self.custom_logger.log(self.logger, logging.DEBUG, thisproc, 'completed with >' + str(result.rc) + "<.")
        return result
