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
# Process deploy list for FitNesse artifacts
# @Since: 23-OCT-2019
# @Author: Jac. Beekers
# @Version: 20191023.0 - JBE - Initial
# @Version: 20200529.0 - JBE - Changes due to changes in logging

import logging
import os
from pathlib import Path

import supporting.deploylist
import supporting.errorcodes as err
from supporting import filehandling
from supporting import generalSettings
from supporting.filehandling import copy_file
from supporting.generatezip import addto_zip
from supporting.generatezip import generate_zip
from supporting.logging import customLogger

from create_fitnesse_artifact.helpers import fitnesseConstants


class BuildFitNesseArtifact:

    def __init__(self, fitnesse_settings, deploylist=fitnesseConstants.DEFAULT_FITNESSE_DEPLOYLIST):
        self.main_proc = 'BuildFitNesseArtifact'
        #        self.logger = logging.getLogger(self.main_proc)
        self.logger = logging.getLogger(__name__)
        self.custom_logger = customLogger.CustomLogger(self.main_proc, True)
        self.entrynr = 0
        self.level = 0
        self.previous_schema = 'AUQW&^D*AD&FS'
        self.deploylist = deploylist
        self.fitnesse_settings = fitnesse_settings

    def processEntry(self, deployEntry):
        logger = self.logger
        thisproc = "processEntry"
        result = err.OK
        self.custom_logger.log(logger, logging.DEBUG, thisproc, "Current directory is >" + os.getcwd() + "<.")
        self.custom_logger.log(logger, logging.DEBUG, thisproc,
                               "Started to work on deploy entry >" + deployEntry + "<.")

        directory, suppress_zip = deployEntry.split(':', 2)
        self.custom_logger.log(logger, logging.DEBUG, thisproc,
                               'Directory is >' + directory + '< and suppress_zip is >' + suppress_zip + '<')
        zipfilename = self.fitnesse_settings.target_fitnesse_directory + "/" + directory.replace('/', '_') + ".zip"
        self.custom_logger.log(logger, logging.DEBUG, thisproc, 'zipfilename is >' + zipfilename + "<.")

        directoryPath = Path(directory)
        if directoryPath.is_dir():
            self.custom_logger.log(logger, logging.DEBUG, thisproc, 'Found directory >' + directory + "<.")
            sourcefitnessedir = ""
        else:
            sourcefitnessedir = self.fitnesse_settings.source_fitnesse_directory + "/"
            self.custom_logger.log(logger, logging.DEBUG, thisproc, 'directory >' + directory + '< not found. Trying >'
                                   + sourcefitnessedir + directory + '<...')
            directory = sourcefitnessedir + directory
            directoryPath = Path(directory)
            if directoryPath.is_dir():
                self.custom_logger.log(logger, logging.DEBUG, thisproc, 'Found directory >' + directory + "<.")
            else:
                self.custom_logger.log(logger, err.SQLFILE_NF.level, thisproc,
                                       "directory checked >" + directory + "<. " + err.DIRECTORY_NF.message)
                result = err.DIRECTORY_NF
                return result

        if suppress_zip == 'Y':
            self.custom_logger.log(logger, logging.DEBUG, thisproc, "zip files will be ignored.")
            result = generate_zip(sourcefitnessedir, directory, zipfilename, '*', 'zip')
            self.custom_logger.log(logger, logging.DEBUG, thisproc, "generate_zip returned: " + result.code)
            self.custom_logger.log(logger, logging.DEBUG, thisproc, "Adding wiki file >" + directory + ".wiki< to zip.")
            result = addto_zip(sourcefitnessedir, directory + '.wiki', zipfilename, '*', 'zip')
        else:
            self.custom_logger.log(logger, logging.DEBUG, thisproc, "zip files will be included.")
            result = generate_zip(sourcefitnessedir, directory, zipfilename)
            self.custom_logger.log(logger, logging.DEBUG, thisproc, "generate_zip returned: " + result.code)
            self.custom_logger.log(logger, logging.DEBUG, thisproc, "Adding wiki file >" + directory + ".wiki< to zip.")
            result = addto_zip(sourcefitnessedir, directory + '.wiki', zipfilename)

        self.custom_logger.log(logger, logging.DEBUG, thisproc,
                               "Completed with rc >" + str(result.rc) + "< and code >" + result.code + "<.")
        return result

    def processList(self):
        latestError = err.OK
        result, deployItems = supporting.deploylist.getWorkitemList(self.deploylist)
        if result.rc == err.OK.rc:
            filehandling.create_directory(self.fitnesse_settings.target_fitnesse_directory)
            copy_file(self.deploylist, generalSettings.artifactDir)
            for deployEntry in supporting.deploylist.deployItems:
                result = self.processEntry(deployEntry)
                if result.rc != 0:
                    latestError = result
        else:
            # if no deploy list, then that is just fine.
            if result.rc == err.IGNORE.rc:
                latestError = err.OK
            else:
                latestError = result
        return latestError
