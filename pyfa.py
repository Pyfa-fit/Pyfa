#!/usr/bin/env python
# ==============================================================================
# Copyright (C) 2010 Diego Duclos
#
# This file is part of pyfa.
#
# pyfa is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pyfa is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pyfa.  If not, see <http://www.gnu.org/licenses/>.
# ==============================================================================

import inspect
import os
import platform
import re
import sys
import traceback
from imp import find_module
from optparse import AmbiguousOptionError, BadOptionError, OptionParser
from multiprocessing import freeze_support

from service.serviceThreads import executeStartupThreads

from logbook import CRITICAL, DEBUG, ERROR, FingersCrossedHandler, INFO, Logger, NestedSetup, NullHandler, StreamHandler, TimedRotatingFileHandler, WARNING, \
    __version__ as logbook_version

import config

try:
    import wxversion
except ImportError:
    wxversion = None

try:
    import sqlalchemy
except ImportError:
    sqlalchemy = None

pyfalog = Logger(__name__)


class PassThroughOptionParser(OptionParser):
    """
    An unknown option pass-through implementation of OptionParser.

    OSX passes -psn_0_* argument, which is something that pyfa does not handle. See GH issue #423
    """

    def _process_args(self, largs, rargs, values):
        while rargs:
            try:
                OptionParser._process_args(self, largs, rargs, values)
            except (BadOptionError, AmbiguousOptionError) as e:
                pyfalog.error("Bad startup option passed.")
                largs.append(e.opt_str)


class LoggerWriter(object):
    def __init__(self, level):
        # self.level is really like using log.debug(message)
        # at least in my case
        self.level = level

    def write(self, message):
        # if statement reduces the amount of newlines that are
        # printed to the logger
        if message not in {'\n', '    '}:
            self.level(message.replace("\n", ""))

    def flush(self):
        # create a flush method so things can be flushed when
        # the system wants to. Not sure if simply 'printing'
        # sys.stderr is the correct way to do it, but it seemed
        # to work properly for me.
        self.level(sys.stderr)


class PreCheckException(Exception):
    def __init__(self, msg):
        try:
            ln = sys.exc_info()[-1].tb_lineno
        except AttributeError:
            ln = inspect.currentframe().f_back.f_lineno
        self.message = "{0.__name__} (line {1}): {2}".format(type(self), ln, msg)
        self.args = self.message,


def handleGUIException(exc_type, exc_value, exc_traceback):
    try:
        # Try and import wx in case it's missing.
        # noinspection PyPackageRequirements
        import wx
        from gui.errorDialog import ErrorFrame
    except:
        # noinspection PyShadowingNames
        wx = None
        # noinspection PyShadowingNames
        ErrorFrame = None

    tb = traceback.format_tb(exc_traceback)

    try:
        # Try and output to our log handler
        with logging_setup.threadbound():
            module_list = list(set(sys.modules) & set(globals()))
            if module_list:
                pyfalog.info("Imported Python Modules:")
                for imported_module in module_list:
                    module_details = sys.modules[imported_module]
                    pyfalog.info("{0}: {1}", imported_module, getattr(module_details, '__version__', ''))

            pyfalog.critical("Exception in main thread: {0}", exc_value.message)
            # Print the base level traceback
            traceback.print_tb(exc_traceback)

            if wx and ErrorFrame:
                pyfa_gui = wx.App(False)
                if exc_type == PreCheckException or isinstance(exc_value, ImportError):
                    ErrorFrame(exc_value, tb, "Missing prerequisites\nPlease import all modules from requirements.txt")
                else:
                    ErrorFrame(exc_value, tb)

                pyfa_gui.MainLoop()

            pyfalog.info("Exiting.")
    except:
        # Most likely logging isn't available. Try and output to the console
        module_list = list(set(sys.modules) & set(globals()))
        if module_list:
            pyfalog.info("Imported Python Modules:")
            for imported_module in module_list:
                module_details = sys.modules[imported_module]
                print(str(imported_module) + ": " + str(getattr(module_details, '__version__', '')))

        print("Exception in main thread: " + str(exc_value.message))
        traceback.print_tb(exc_traceback)

        if wx and ErrorFrame:
            pyfa_gui = wx.App(False)
            if exc_type == PreCheckException or isinstance(exc_value, ImportError):
                ErrorFrame(exc_value, tb, "Missing prerequisites")
            else:
                ErrorFrame(exc_value, tb)

            pyfa_gui.MainLoop()

        print("Exiting.")

    finally:
        # TODO: Add cleanup when exiting here.
        sys.exit()


# Replace the uncaught exception handler with our own handler.
sys.excepthook = handleGUIException

logVersion = logbook_version.split('.')
if int(logVersion[0]) < 1:
    print ("Logbook version >= 1.0.0 is recommended. You may have some performance issues by continuing to use an earlier version.")

# Parse command line options
usage = "usage: %prog [--root]"
parser = PassThroughOptionParser(usage=usage)
parser.add_option("-r", "--root", action="store_true", dest="rootsavedata", help="if you want pyfa to store its data in root folder, use this option", default=False)
parser.add_option("-w", "--wx28", action="store_true", dest="force28", help="Force usage of wxPython 2.8", default=False)
parser.add_option("-d", "--debug", action="store_true", dest="debug", help="Set logger to debug level.", default=False)
parser.add_option("-t", "--title", action="store", dest="title", help="Set Window Title", default=None)
parser.add_option("-s", "--savepath", action="store", dest="savepath", help="Set the folder for savedata", default=None)
parser.add_option("-l", "--logginglevel", action="store", dest="logginglevel", help="Set desired logging level [Critical|Error|Warning|Info|Debug]", default="Error")
parser.add_option("-e", "--esiurl", action="store", dest="esiurl", help="Path to use for ESI.",
                  default="https://esi.tech.ccp.is/latest/swagger.json?datasource=tranquility")
parser.add_option("-g", "--gamedatabasename", action="store", dest="gamedatabasename", help="Name to use for the gamedata database", default="eve.db")

(options, args) = parser.parse_args()

if options.logginglevel == "Critical":
    options.logginglevel = CRITICAL
elif options.logginglevel == "Error":
    options.logginglevel = ERROR
elif options.logginglevel == "Warning":
    options.logginglevel = WARNING
elif options.logginglevel == "Info":
    options.logginglevel = INFO
elif options.logginglevel == "Debug":
    options.logginglevel = DEBUG
else:
    options.logginglevel = ERROR

if __name__ == "__main__":
    freeze_support()
    # Configure paths
    if options.rootsavedata is True:
        config.saveInRoot = True

    config.esiurl = options.esiurl
    config.gamedatabasename = options.gamedatabasename

    # set title if it wasn't supplied by argument
    if options.title is None:
        options.title = "Pyfa.fit %s %s - Python Fitting Assistant" % (config.version, config.tag)

    config.debug = options.debug

    # convert to unicode if it is set
    if options.savepath is not None:
        options.savepath = unicode(options.savepath)
    config.defPaths(options.savepath)

    # Basic logging initialization

    # Logging levels:
    # logbook.CRITICAL
    # logbook.ERROR
    # logbook.WARNING
    # logbook.INFO
    # logbook.DEBUG
    # logbook.NOTSET

    if options.debug:
        savePath_filename = u"Pyfa_debug.log"
    else:
        savePath_filename = u"Pyfa.log"

    config.logPath = config.getSavePath(savePath_filename)

    try:
        if options.debug:
            logging_mode = "Debug"
            logging_setup = NestedSetup([
                # make sure we never bubble up to the stderr handler
                # if we run out of setup handling
                NullHandler(),
                StreamHandler(
                        sys.stdout,
                        bubble=False,
                        level=options.logginglevel
                ),
                TimedRotatingFileHandler(
                        config.logPath,
                        level=0,
                        backup_count=3,
                        bubble=True,
                        date_format='%Y-%m-%d',
                ),
            ])
        else:
            logging_mode = "User"
            logging_setup = NestedSetup([
                # make sure we never bubble up to the stderr handler
                # if we run out of setup handling
                NullHandler(),
                FingersCrossedHandler(
                        TimedRotatingFileHandler(
                                config.logPath,
                                level=0,
                                backup_count=3,
                                bubble=False,
                                date_format='%Y-%m-%d',
                        ),
                        action_level=ERROR,
                        buffer_size=1000,
                        # pull_information=True,
                        # reset=False,
                )
            ])
    except:
        print("Critical error attempting to setup logging. Falling back to console only.")
        logging_mode = "Console Only"
        logging_setup = NestedSetup([
            # make sure we never bubble up to the stderr handler
            # if we run out of setup handling
            NullHandler(),
            StreamHandler(
                    sys.stdout,
                    bubble=False
            )
        ])

    with logging_setup.threadbound():
        pyfalog.info("Starting Pyfa")

        pyfalog.info("Logbook version: {0}", logbook_version)

        pyfalog.info("Running in logging mode: {0}", logging_mode)
        pyfalog.info("Writing log file to: {0}", config.logPath)

        # Output all stdout (print) messages as warnings
        try:
            sys.stdout = LoggerWriter(pyfalog.info)
        except:
            pyfalog.critical("Cannot redirect.  Continuing without writing stdout to log.")

        # Output all stderr messages as critical
        try:
            sys.stderr = LoggerWriter(pyfalog.warning)
        except:
            pyfalog.critical("Cannot redirect.  Continuing without writing stderr to log.")

        pyfalog.info("OS version: {0}", platform.platform())

        pyfalog.info("Python version: {0}", sys.version)
        if sys.version_info < (2, 7) or sys.version_info > (3, 0):
            exit_message = "Pyfa requires python 2.x branch ( >= 2.7 )."
            raise PreCheckException(exit_message)

        if hasattr(sys, 'frozen'):
            pyfalog.info("Running in a frozen state.")
        else:
            pyfalog.info("Running in a thawed state.")

        if not hasattr(sys, 'frozen') and wxversion:
            try:
                if options.force28 is True:
                    pyfalog.info("Selecting wx version: 2.8. (Forced)")
                    wxversion.select('2.8')
                else:
                    pyfalog.info("Selecting wx versions: 3.0, 2.8")
                    wxversion.select(['3.0', '2.8'])
            except:
                pyfalog.warning("Unable to select wx version.  Attempting to import wx without specifying the version.")
        else:
            if not wxversion:
                pyfalog.warning("wxVersion not found.  Attempting to import wx without specifying the version.")

        try:
            # noinspection PyPackageRequirements
            import wx
        except:
            exit_message = "Cannot import wxPython. You can download wxPython (2.8+) from http://www.wxpython.org/"
            raise PreCheckException(exit_message)

        pyfalog.info("wxPython version: {0}.", str(wx.VERSION_STRING))

        if sqlalchemy is None:
            exit_message = "\nCannot find sqlalchemy.\nYou can download sqlalchemy (0.6+) from http://www.sqlalchemy.org/"
            raise PreCheckException(exit_message)
        else:
            saVersion = sqlalchemy.__version__
            saMatch = re.match("([0-9]+).([0-9]+)([b\.])([0-9]+)", saVersion)
            config.saVersion = (int(saMatch.group(1)), int(saMatch.group(2)), int(saMatch.group(4)))
            if saMatch:
                saMajor = int(saMatch.group(1))
                saMinor = int(saMatch.group(2))
                betaFlag = True if saMatch.group(3) == "b" else False
                saBuild = int(saMatch.group(4)) if not betaFlag else 0
                if saMajor == 0 and (saMinor < 5 or (saMinor == 5 and saBuild < 8)):
                    pyfalog.critical("Pyfa requires sqlalchemy 0.5.8 at least but current sqlAlchemy version is {0}", format(sqlalchemy.__version__))
                    pyfalog.critical("You can download sqlAlchemy (0.5.8+) from http://www.sqlalchemy.org/")
                    pyfalog.critical("Attempting to run with unsupported version of sqlAlchemy.")
                else:
                    pyfalog.info("Current version of sqlAlchemy is: {0}", sqlalchemy.__version__)
            else:
                pyfalog.warning("Unknown sqlalchemy version string format, skipping check. Version: {0}", sqlalchemy.__version__)

        requirements_path = config.getPyfaPath(u"requirements.txt")
        if os.path.exists(requirements_path):
            filename = open(requirements_path, "r")
            for requirement in filename:
                requirement = requirement.replace("\n", "")
                requirement_parsed = requirement.split(' ')
                if requirement_parsed:
                    try:
                        find_module(requirement_parsed[0])
                    except ImportError as e:
                        pyfalog.warning("Possibly missing required module: {0}", requirement_parsed[0])
                        if len(requirement_parsed) == 3:
                            pyfalog.warning("Recommended version {0} {1}", requirement_parsed[1], requirement_parsed[2])

        logVersion = logbook_version.split('.')
        if int(logVersion[0]) == 0 and int(logVersion[1]) < 10:
            raise PreCheckException("Logbook version >= 0.10.0 is required.")

        if 'wxMac' not in wx.PlatformInfo or ('wxMac' in wx.PlatformInfo and wx.VERSION >= (3, 0)):
            try:
                import requests
                config.requestsVersion = requests.__version__
            except ImportError:
                requests = None
                raise PreCheckException("Cannot import requests. You can download requests from https://pypi.python.org/pypi/requests.")

        import eos.db

        if config.saVersion[0] > 0 or config.saVersion[1] >= 7:
            # <0.7 doesn't have support for events ;_; (mac-deprecated)
            config.sa_events = True
            import eos.events

        # noinspection PyUnresolvedReferences
        pyfalog.debug("Running prefetch service.")
        import service.prefetch  # noqa: F401

        # Make sure the saveddata db exists
        pyfalog.debug("Validate savedata DB path.")
        if not os.path.exists(config.savePath):
            os.mkdir(config.savePath)

        pyfalog.debug("Creating DB metadata.")
        eos.db.saveddata_meta.create_all()

        pyfalog.info("Starting threads")
        executeStartupThreads()

        pyfalog.debug("Importing main GUI interface.")
        from gui.mainFrame import MainFrame

        pyfalog.debug("Creating wx application.")
        pyfa = wx.App(False)

        pyfalog.debug("Creating GUI main frame.")
        MainFrame(options.title)
        pyfalog.debug("Launching Pyfa.")
        pyfa.MainLoop()

        # TODO: Add some thread cleanup code here. Right now we bail, and that can lead to orphaned threads or threads not properly exiting.
        sys.exit()
