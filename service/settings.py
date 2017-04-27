# =============================================================================
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
# =============================================================================

import cPickle
import os.path
import urllib2

import config
import eos.config as eos_config
from logbook import Logger

pyfalog = Logger(__name__)


class SettingsProvider(object):
    BASE_PATH = config.getSavePath(u'settings')
    settings = {}
    _instance = None

    @classmethod
    def getInstance(cls):
        if cls._instance is None:
            cls._instance = SettingsProvider()

        return cls._instance

    def __init__(self):
        if hasattr(self, 'BASE_PATH'):
            if not os.path.exists(self.BASE_PATH):
                os.mkdir(self.BASE_PATH)

    def getSettings(self, area, defaults=None):

        if defaults is None:
            defaults = []

        s = self.settings.get(area)

        if s is None and hasattr(self, 'BASE_PATH'):
            p = os.path.join(self.BASE_PATH, area)

            if os.path.exists(p):
                # noinspection PyBroadException
                try:
                    f = open(p, "rb")
                    info = cPickle.load(f)
                except:
                    info = {}
                    # TODO: Add logging message that we failed to open the file
            else:
                info = {}

            s = Settings(p, info)

        for item in defaults:
            if item not in s.info:
                s.info[item] = defaults[item]

        self.settings[area] = s

        return s

    def saveAll(self):
        for settings in self.settings.itervalues():
            settings.save()


class Settings(object):
    def __init__(self, location, info):
        self.location = location
        self.info = info

    def save(self):
        f = open(self.location, "wb")
        cPickle.dump(self.info, f, cPickle.HIGHEST_PROTOCOL)

    def __getitem__(self, k):
        try:
            return self.info[k]
        except KeyError as e:
            pyfalog.warning("Failed to get setting for '{0}'. Exception: {1}", k, e)
            return None

    def __setitem__(self, k, v):
        self.info[k] = v

    def __iter__(self):
        return self.info.__iter__()

    def iterkeys(self):
        return self.info.iterkeys()

    def itervalues(self):
        return self.info.itervalues()

    def iteritems(self):
        return self.info.iteritems()

    def keys(self):
        return self.info.keys()

    def values(self):
        return self.info.values()

    def items(self):
        return self.info.items()


class NetworkSettings(object):
    _instance = None

    # constants for serviceNetworkDefaultSettings["mode"] parameter
    PROXY_MODE_NONE = 0  # 0 - No proxy
    PROXY_MODE_AUTODETECT = 1  # 1 - Auto-detected proxy settings
    PROXY_MODE_MANUAL = 2  # 2 - Manual proxy settings

    @classmethod
    def getInstance(cls):
        if cls._instance is None:
            cls._instance = NetworkSettings()

        return cls._instance

    def __init__(self):

        serviceNetworkDefaultSettings = {
            "mode"    : self.PROXY_MODE_AUTODETECT,
            "type"    : "https",
            "address" : "",
            "port"    : "",
            "access"  : 15,
            "login"   : None,
            "password": None
        }

        self.serviceNetworkSettings = SettingsProvider.getInstance().getSettings(
                "pyfaServiceNetworkSettings", serviceNetworkDefaultSettings)

    def isEnabled(self, setting_type):
        if setting_type & self.serviceNetworkSettings["access"]:
            return True
        return False

    def toggleAccess(self, setting_type, toggle=True):
        bitfield = self.serviceNetworkSettings["access"]

        if toggle:  # Turn bit on
            self.serviceNetworkSettings["access"] = setting_type | bitfield
        else:  # Turn bit off
            self.serviceNetworkSettings["access"] = ~setting_type & bitfield

    def getMode(self):
        return self.serviceNetworkSettings["mode"]

    def getAddress(self):
        return self.serviceNetworkSettings["address"]

    def getPort(self):
        return self.serviceNetworkSettings["port"]

    def getType(self):
        return self.serviceNetworkSettings["type"]

    def getAccess(self):
        return self.serviceNetworkSettings["access"]

    def setMode(self, mode):
        self.serviceNetworkSettings["mode"] = mode

    def setAddress(self, addr):
        self.serviceNetworkSettings["address"] = addr

    def setPort(self, port):
        self.serviceNetworkSettings["port"] = port

    def setType(self, setting_type):
        self.serviceNetworkSettings["type"] = setting_type

    def setAccess(self, access):
        self.serviceNetworkSettings["access"] = access

    @staticmethod
    def autodetect():

        proxy = None
        proxydict = urllib2.ProxyHandler().proxies

        validPrefixes = ("http", "https")

        for prefix in validPrefixes:
            if prefix not in proxydict:
                continue
            proxyline = proxydict[prefix]
            proto = "{0}://".format(prefix)
            if proxyline[:len(proto)] == proto:
                proxyline = proxyline[len(proto):]
            proxAddr, proxPort = proxyline.split(":")
            proxPort = int(proxPort.rstrip("/"))
            proxy = (proxAddr, proxPort)
            break

        return proxy

    def getProxySettings(self):

        if self.getMode() == self.PROXY_MODE_NONE:
            return None
        if self.getMode() == self.PROXY_MODE_AUTODETECT:
            return self.autodetect()
        if self.getMode() == self.PROXY_MODE_MANUAL:
            return self.getAddress(), int(self.getPort())

    def getProxyAuthDetails(self):
        if self.getMode() == self.PROXY_MODE_NONE:
            return None
        if (self.serviceNetworkSettings["login"] is None) or (self.serviceNetworkSettings["password"] is None):
            return None
        # in all other cases, return tuple of (login, password)
        return self.serviceNetworkSettings["login"], self.serviceNetworkSettings["password"]

    def setProxyAuthDetails(self, login, password):
        if (login is None) or (password is None):
            self.serviceNetworkSettings["login"] = None
            self.serviceNetworkSettings["password"] = None
            return
        if login == "":  # empty login unsets proxy auth info
            self.serviceNetworkSettings["login"] = None
            self.serviceNetworkSettings["password"] = None
            return
        self.serviceNetworkSettings["login"] = login
        self.serviceNetworkSettings["password"] = password


class HTMLExportSettings(object):
    """
    Settings used by the HTML export feature.
    """
    _instance = None

    @classmethod
    def getInstance(cls):
        if cls._instance is None:
            cls._instance = HTMLExportSettings()

        return cls._instance

    def __init__(self):
        serviceHTMLExportDefaultSettings = {
            "path"   : config.getSavePath(u'pyfaFits.html'),
            "minimal": False
        }
        self.serviceHTMLExportSettings = SettingsProvider.getInstance().getSettings(
                "pyfaServiceHTMLExportSettings",
                serviceHTMLExportDefaultSettings
        )

    def getMinimalEnabled(self):
        return self.serviceHTMLExportSettings["minimal"]

    def setMinimalEnabled(self, minimal):
        self.serviceHTMLExportSettings["minimal"] = minimal

    def getPath(self):
        return self.serviceHTMLExportSettings["path"]

    def setPath(self, path):
        self.serviceHTMLExportSettings["path"] = path


class UpdateSettings(object):
    """
    Settings used by update notification
    """
    _instance = None

    @classmethod
    def getInstance(cls):
        if cls._instance is None:
            cls._instance = UpdateSettings()

        return cls._instance

    def __init__(self):
        # Settings
        # Updates are completely suppressed via network settings
        # prerelease - If True, suppress prerelease notifications
        # version    - Set to release tag that user does not want notifications for
        serviceUpdateDefaultSettings = {"prerelease": True, 'version': None}
        self.serviceUpdateSettings = SettingsProvider.getInstance().getSettings(
                "pyfaServiceUpdateSettings",
                serviceUpdateDefaultSettings
        )

    def get(self, setting_type):
        return self.serviceUpdateSettings[setting_type]

    def set(self, setting_type, value):
        self.serviceUpdateSettings[setting_type] = value


class CRESTSettings(object):
    _instance = None

    @classmethod
    def getInstance(cls):
        if cls._instance is None:
            cls._instance = CRESTSettings()

        return cls._instance

    def __init__(self):
        # mode
        # 0 - Implicit authentication
        # 1 - User-supplied client details
        serviceCRESTDefaultSettings = {"mode": 0, "server": 0, "clientID": "", "clientSecret": "", "timeout": 60}

        self.serviceCRESTSettings = SettingsProvider.getInstance().getSettings(
                "pyfaServiceCRESTSettings",
                serviceCRESTDefaultSettings
        )

    def get(self, setting_type):
        return self.serviceCRESTSettings[setting_type]

    def set(self, setting_type, value):
        self.serviceCRESTSettings[setting_type] = value


class GeneralSettings(object):
    _instance = None

    @classmethod
    def getInstance(cls):
        if cls._instance is None:
            cls._instance = GeneralSettings()

        return cls._instance

    def __init__(self):
        # mode
        # 0 - Do not show
        # 1 - Minimal/Text Only View
        # 2 - Full View
        GeneralDefaultSettings = {
            "itemSearchLimit": 150,
            "marketSearchDelay": 250,
            "fontSize": 'NORMAL',
            "showAllMarketGroups": False,
        }

        self.serviceGeneralDefaultSettings = SettingsProvider.getInstance().getSettings("pyfaGeneralSettings", GeneralDefaultSettings)

    def get(self, type):
        return self.serviceGeneralDefaultSettings[type]

    def set(self, type, value):
        self.serviceGeneralDefaultSettings[type] = value


class DatabaseSettings(object):
    _instance = None

    @classmethod
    def getInstance(cls):
        if cls._instance is None:
            cls._instance = DatabaseSettings()

        return cls._instance

    def __init__(self):
        # mode
        # 0 - Do not show
        # 1 - Minimal/Text Only View
        # 2 - Full View
        DatabaseDefaultSettings = {
            "ImportItemsNotInMarketGroups": False,
            "ImportItemsNotPublished": False,
            "UpdateThreads": 25,
        }

        self.serviceDatabaseDefaultSettings = SettingsProvider.getInstance().getSettings("pyfaDatabaseSettings", DatabaseDefaultSettings)

    def get(self, type):
        return self.serviceDatabaseDefaultSettings[type]

    def set(self, type, value):
        self.serviceDatabaseDefaultSettings[type] = value


class StatViewSettings(object):
    _instance = None

    @classmethod
    def getInstance(cls):
        if cls._instance is None:
            cls._instance = StatViewSettings()

        return cls._instance

    def __init__(self):
        # mode
        # 0 - Do not show
        # 1 - Minimal/Text Only View
        # 2 - Full View
        serviceStatViewDefaultSettings = {
            "resources"    : 2,
            "resistances"  : 2,
            "recharge"     : 2,
            "firepower"    : 2,
            "capacitor"    : 2,
            "targetingMisc": 1,
            "price"        : 2,
            "miningyield"  : 2,
            "drones"       : 2,
            "outgoing"     : 2,
        }

        self.serviceStatViewDefaultSettings = SettingsProvider.getInstance().getSettings("pyfaServiceStatViewSettings", serviceStatViewDefaultSettings)

    def get(self, type):
        return self.serviceStatViewDefaultSettings[type]

    def set(self, type, value):
        self.serviceStatViewDefaultSettings[type] = value


class ContextMenuSettings(object):
    _instance = None

    @classmethod
    def getInstance(cls):
        if cls._instance is None:
            cls._instance = ContextMenuSettings()

        return cls._instance

    def __init__(self):
        # mode
        # 0 - Do not show
        # 1 - Show
        ContextMenuDefaultSettings = {
            "ammoPattern"           : 1,
            "amount"                : 1,
            "cargo"                 : 1,
            "cargoAmmo"             : 1,
            "changeAffectingSkills" : 1,
            "damagePattern"         : 1,
            "droneRemoveStack"      : 1,
            "droneSplit"            : 1,
            "droneStack"            : 1,
            "factorReload"          : 1,
            "fighterAbilities"      : 1,
            "implantSets"           : 1,
            "itemStats"             : 1,
            "itemRemove"            : 1,
            "marketJump"            : 1,
            "metaSwap"              : 1,
            "moduleAmmoPicker"      : 1,
            "moduleGlobalAmmoPicker": 1,
            "openFit"               : 1,
            "priceClear"            : 1,
            "project"               : 1,
            "shipJump"              : 1,
            "tacticalMode"          : 1,
            "targetResists"         : 1,
            "whProjector"           : 1,
        }

        self.ContextMenuDefaultSettings = SettingsProvider.getInstance().getSettings("pyfaContextMenuSettings", ContextMenuDefaultSettings)

    def get(self, type):
        return self.ContextMenuDefaultSettings[type]

    def set(self, type, value):
        self.ContextMenuDefaultSettings[type] = value


class EOSSettings(object):
    _instance = None

    @classmethod
    def getInstance(cls):
        if cls._instance is None:
            cls._instance = EOSSettings()

        return cls._instance

    def __init__(self):
        self.EOSSettings = SettingsProvider.getInstance().getSettings("pyfaEOSSettings", eos_config.settings)

    def get(self, type):
        return self.EOSSettings[type]

    def set(self, type, value):
        self.EOSSettings[type] = value

# @todo: migrate fit settings (from fit service) here?
