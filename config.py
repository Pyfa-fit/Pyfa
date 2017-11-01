import os
import sys
import ctypes
import platform

from logbook import Logger

if platform.system() is "Windows":
    from ctypes import windll, wintypes
else:
    windll = wintypes = None

pyfalog = Logger(__name__)

# Load variable overrides specific to distribution type
try:
    import configforced
except ImportError:
    pyfalog.warning("Failed to import: configforced")
    configforced = None

# Turns on debug mode
debug = False
# Defines if our saveddata will be in pyfa root or not
saveInRoot = False

# Version data
version = "2017.06.26"
if hasattr(sys, 'frozen'):
    tag = ""
else:
    tag = "(live)"
expansionName = "YC119.5"
expansionVersion = "1.0"
evemonMinVersion = "2"

pyfaPath = None
savePath = None
saveDB = None
gameDB = None
logPath = None
gamedatabasename = None
esiurl = None


def isFrozen():
    if hasattr(sys, 'frozen'):
        return True
    else:
        return False


def __createDirs(path):
    if not os.path.exists(path):
        os.makedirs(path)


def defPaths(customSavePath):
    global debug
    global pyfaPath
    global savePath
    global saveDB
    global gameDB
    global saveInRoot
    global gamedatabasename

    pyfalog.debug("Configuring Pyfa")

    # The main pyfa directory which contains run.py
    # Python 2.X uses ANSI by default, so we need to convert the character encoding
    pyfaPath = getattr(configforced, "pyfaPath", pyfaPath)
    if pyfaPath is None:
        pyfaPath = getPyfaPath()

    # Where we store the saved fits etc, default is the current users home directory
    if saveInRoot is True:
        savePath = getattr(configforced, "savePath", None)
        if savePath is None:
            savePath = getPyfaPath(u"saveddata")
    else:
        savePath = getattr(configforced, "savePath", None)
        if savePath is None:
            if customSavePath is None:  # customSavePath is not overriden
                savePath = getSavePath()
            else:
                savePath = customSavePath

    __createDirs(savePath)

    if isFrozen():
        os.environ["REQUESTS_CA_BUNDLE"] = getPyfaPath(u"cacert.pem")
        os.environ["SSL_CERT_FILE"] = getPyfaPath(u"cacert.pem")

    # The database where we store all the fits etc
    saveDB = getSavePath(u"saveddata.db")

    # The database where the static EVE data from the datadump is kept.
    # This is not the standard sqlite datadump but a modified version created by eos
    # maintenance script
    gameDB = getattr(configforced, "gameDB", gameDB)
    if not gameDB:
        gameDB = getPyfaPath(unicode(gamedatabasename))

    # DON'T MODIFY ANYTHING BELOW
    import eos.config

    # Caching modifiers, disable all gamedata caching, its unneeded.
    eos.config.gamedataCache = False
    # saveddata db location modifier, shouldn't ever need to touch this
    eos.config.saveddata_connectionstring = "sqlite:///" + saveDB + "?check_same_thread=False"
    eos.config.gamedata_connectionstring = "sqlite:///" + gameDB + "?check_same_thread=False"

    # initialize the settings
    from service.settings import EOSSettings
    eos.config.settings = EOSSettings.getInstance().EOSSettings  # this is kind of confusing, but whatever


def getPyfaPath(Append=None):
    base = __file__
    base_alt = sys.argv[0]

    try:
        base = unicode(base)
        base_alt = unicode(base_alt)
    except:
        base = unicode(base, sys.getfilesystemencoding())
        base_alt = unicode(base_alt, sys.getfilesystemencoding())

    root = os.path.dirname(os.path.realpath(base))

    if not os.path.isdir(root):
        root = os.path.dirname(os.path.realpath(base_alt))

    if not Append:
        return root

    try:
        Append = unicode(Append)
    except:
        Append = unicode(Append, sys.getfilesystemencoding())

    path = os.path.realpath(os.path.join(root, Append))

    return path


def getSavePath(Append=None):
    if saveInRoot:
        root = getPyfaPath()
    else:
        if platform.system() is "Windows":
            root = os.path.join(expand_user(), u".pyfa")
        else:
            root = os.path.expanduser(os.path.join(u"~", u".pyfa"))

    if not Append:
        return root

    try:
        Append = unicode(Append)
    except:
        Append = unicode(Append, sys.getfilesystemencoding())

    path = os.path.realpath(os.path.join(root, Append))

    return path


class GUID(ctypes.Structure):
    if wintypes:
        _fields_ = [
             ('Data1', wintypes.DWORD),
             ('Data2', wintypes.WORD),
             ('Data3', wintypes.WORD),
             ('Data4', wintypes.BYTE * 8)
        ]

        def __init__(self, l, w1, w2, b1, b2, b3, b4, b5, b6, b7, b8):
            """Create a new GUID."""
            self.Data1 = l
            self.Data2 = w1
            self.Data3 = w2
            self.Data4[:] = (b1, b2, b3, b4, b5, b6, b7, b8)

        def __repr__(self):
            b1, b2, b3, b4, b5, b6, b7, b8 = self.Data4
            return 'GUID(%x-%x-%x-%x%x%x%x%x%x%x%x)' % (
                       self.Data1, self.Data2, self.Data3, b1, b2, b3, b4, b5, b6, b7, b8)


def expand_user():
    """
    There's a bug in Python 2.x for `expanduser` when running in Windows, and there are unicode characters in the path.
    We have to roll our own to work around it.
    See:
    http://bugs.python.org/issue13207
    http://stackoverflow.com/questions/23888120/an-alternative-to-os-path-expanduser
    """

    # constants to be used according to the version on shell32
    CSIDL_PROFILE = 40
    FOLDERID_Profile = GUID(0x5E6C858F, 0x0E22, 0x4760, 0x9A, 0xFE, 0xEA, 0x33, 0x17, 0xB6, 0x71, 0x73)

    if windll:
        # get the function that we can find from Vista up, not the one in XP
        get_folder_path = getattr(windll.shell32, 'SHGetKnownFolderPath', None)

        if get_folder_path is not None:
            # ok, we can use the new function which is recomended by the msdn
            ptr = ctypes.c_wchar_p()
            get_folder_path(ctypes.byref(FOLDERID_Profile), 0, 0, ctypes.byref(ptr))
            return ptr.value
        else:
            # use the deprecated one found in XP and on for compatibility reasons
            get_folder_path = getattr(windll.shell32, 'SHGetSpecialFolderPathW', None)
            buf = ctypes.create_unicode_buffer(300)
            get_folder_path(None, buf, CSIDL_PROFILE, False)
            return buf.value
