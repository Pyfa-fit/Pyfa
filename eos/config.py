import sys
from os.path import realpath, join, dirname, abspath

from logbook import Logger
import os

istravis = os.environ.get('TRAVIS') == 'true'
pyfalog = Logger(__name__)

debug = False
gamedataCache = True
saveddataCache = True
gamedata_version = ""
gamedata_connectionstring = 'sqlite:///' + realpath(join(dirname(abspath(__file__)), u"..", u"eve.db"))
pyfalog.debug("Gamedata connection string: {0}", gamedata_connectionstring)

if istravis is True or hasattr(sys, '_called_from_test'):
    # Running in Travis. Run saveddata database in memory.
    saveddata_connectionstring = 'sqlite:///:memory:'

try:
    saveddata_connectionstring
except NameError:
    # Only set this if it hasn't been set elsewhere
    saveddata_connectionstring = 'sqlite:///' + realpath(join(dirname(abspath(__file__)), u"..", u"saveddata", u"saveddata.db"))

pyfalog.debug("Saveddata connection string: {0}", saveddata_connectionstring)

settings = {
    "useStaticAdaptiveArmorHardener": False,
    "strictFitting"                 : True,
    "fireAtPercentCapacitor"        : 25,
    "strictSkillLevels"             : True,
}

# Autodetect path, only change if the autodetection bugs out.
path = dirname(__file__)
