# ===============================================================================
# Copyright (C) 2010 Diego Duclos
#
# This file is part of eos.
#
# eos is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# eos is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with eos.  If not, see <http://www.gnu.org/licenses/>.
# ===============================================================================

import re

from sqlalchemy.orm import reconstructor

import eos.db
from eqBase import EqBase
from eos.saveddata.price import Price as types_Price
from eos.staticData import Slot

try:
    from collections import OrderedDict
except ImportError:
    from utils.compat import OrderedDict

from logbook import Logger

pyfalog = Logger(__name__)
# Keep a list of handlers that fail to import so we don't keep trying repeatedly.
badHandlers = []


class Effect(EqBase):
    """
    The effect handling class, it is used to proxy and load effect handler code,
    as well as a container for extra information regarding effects coming
    from the gamedata db.

    @ivar ID: the ID of this effect
    @ivar name: The name of this effect
    @ivar description: The description of this effect, this is usualy pretty useless
    @ivar published: Wether this effect is published or not, unpublished effects are typicaly unused.
    """
    # Filter to change names of effects to valid python method names
    nameFilter = re.compile("[^A-Za-z0-9]")

    @reconstructor
    def init(self):
        """
        Reconstructor, composes the object as we grab it from the database
        """
        self.__generated = False
        self.__effectModule = None
        self.handlerName = re.sub(self.nameFilter, "", self.name).lower()

    @property
    def handler(self):
        """
        The handler for the effect,
        It is automaticly fetched from effects/<effectName>.py if the file exists
        the first time this property is accessed.
        """
        if not self.__generated:
            self.__generateHandler()

        pyfalog.debug("Generating effect: {0} ({1}) [runTime: {2}]", self.name, self.effectID, self.runTime)

        return self.__handler

    @property
    def runTime(self):
        """
        The runTime that this effect should be run at.
        This property is also automaticly fetched from effects/<effectName>.py if the file exists.
        the possible values are:
        None, "early", "normal", "late"
        None and "normal" are equivalent, and are also the default.

        effects with an early runTime will be ran first when things are calculated,
        followed by effects with a normal runTime and as last effects with a late runTime are ran.
        """
        if not self.__generated:
            self.__generateHandler()

        return self.__runTime

    @property
    def activeByDefault(self):
        """
        The state that this effect should be be in.
        This property is also automaticly fetched from effects/<effectName>.py if the file exists.
        the possible values are:
        None, True, False

        If this is not set:
        We simply assume that missing/none = True, and set it accordingly
        (much as we set runTime to Normalif not otherwise set).
        Nearly all effect files will fall under this category.

        If this is set to True:
        We would enable it anyway, but hey, it's double enabled.
        No effect files are currently configured this way (and probably will never be).

        If this is set to False:
        Basically we simply skip adding the effect to the effect handler when the effect is called,
        much as if the run time didn't match or other criteria failed.
        """
        if not self.__generated:
            self.__generateHandler()

        return self.__activeByDefault

    @activeByDefault.setter
    def activeByDefault(self, value):
        """
        Just assign the input values to the activeByDefault attribute.
        You *could* do something more interesting here if you wanted.
        """
        self.__activeByDefault = value

    @property
    def effectType(self):
        """
        The type of the effect, automaticly fetched from effects/<effectName>.py if the file exists.

        Valid values are:
        "passive", "active", "projected", "gang", "structure"

        Each gives valuable information to eos about what type the module having
        the effect is. passive vs active gives eos clues about wether to module
        is activatable or not (duh!) and projected and gang each tell eos that the
        module can be projected onto other fits, or used as a gang booster module respectivly
        """
        if not self.__generated:
            self.__generateHandler()

        return self.__type

    @property
    def isImplemented(self):
        """
        Whether this effect is implemented in code or not,
        unimplemented effects simply do nothing at all when run
        """
        return self.handler != effectDummy

    def isType(self, _type):
        """
        Check if this effect is of the passed type
        """
        return self.effectType is not None and _type in self.effectType

    def __generateHandler(self):
        """
        Grab the handler, type and runTime from the effect code if it exists,
        if it doesn't, set dummy values and add a dummy handler
        """
        global badHandlers

        # Skip if we've tried to import before and failed
        if self.handlerName not in badHandlers:
            try:
                self.__effectModule = effectModule = __import__('eos.effects.' + self.handlerName, fromlist=True)
                self.__handler = getattr(effectModule, "handler", effectDummy)
                self.__runTime = getattr(effectModule, "runTime", "normal")
                self.__activeByDefault = getattr(effectModule, "activeByDefault", True)
                t = getattr(effectModule, "effectType", None)

                t = t if isinstance(t, tuple) or t is None else (t,)
                self.__type = t
            except ImportError as e:
                # Effect probably doesn't exist, so create a dummy effect and flag it with a warning.
                self.__handler = effectDummy
                self.__runTime = "normal"
                self.__activeByDefault = True
                self.__type = None
                pyfalog.debug("ImportError generating handler: {0}", e)
                badHandlers.append(self.handlerName)
            except AttributeError as e:
                # Effect probably exists but there is an issue with it.  Turn it into a dummy effect so we can continue, but flag it with an error.
                self.__handler = effectDummy
                self.__runTime = "normal"
                self.__activeByDefault = True
                self.__type = None
                pyfalog.error("AttributeError generating handler: {0}", e)
                badHandlers.append(self.handlerName)
            except Exception as e:
                self.__handler = effectDummy
                self.__runTime = "normal"
                self.__activeByDefault = True
                self.__type = None
                pyfalog.critical("Exception generating handler:")
                pyfalog.critical(e)
                badHandlers.append(self.handlerName)

            self.__generated = True
        else:
            # We've already failed on this one, just pass a dummy effect back
            self.__handler = effectDummy
            self.__runTime = "normal"
            self.__activeByDefault = True
            self.__type = None

    def getattr(self, key):
        if not self.__generated:
            self.__generateHandler()

        return getattr(self.__effectModule, key, None)


def effectDummy(*args, **kwargs):
    pass


class Item(EqBase):
    MOVE_ATTRS = (4,  # Mass
                  38,  # Capacity
                  161)  # Volume

    MOVE_ATTR_INFO = None

    @classmethod
    def getMoveAttrInfo(cls):
        info = getattr(cls, "MOVE_ATTR_INFO", None)
        if info is None:
            cls.MOVE_ATTR_INFO = info = []
            for _id in cls.MOVE_ATTRS:
                info.append(eos.db.getAttributeInfo(_id))

        return info

    def moveAttrs(self):
        self.__moved = True
        for info in self.getMoveAttrInfo():
            val = getattr(self, info.name, 0)
            if val != 0:
                attr = Attribute()
                attr.info = info
                attr.value = val
                self.__attributes[info.name] = attr

    @reconstructor
    def init(self):
        self.__race = None
        self.__requiredSkills = None
        self.__requiredFor = None
        self.__moved = False
        self.__offensive = None
        self.__assistive = None
        self.__overrides = None
        self.__price = None

    @property
    def attributes(self):
        if not self.__moved:
            self.moveAttrs()

        return self.__attributes

    def getAttribute(self, key, default=None):
        if key in self.attributes:
            return self.attributes[key].value
        else:
            return default

    def setAttribute(self, key, value):
        try:
            if key not in self.attributes:
                # TODO: Add values in if missing
                self.attributes.append(key)

            self.attributes[key].value = value
            return True
        except (AttributeError, KeyError):
            return False

    def isType(self, _type):
        for effect in self.effects.itervalues():
            if effect.isType(_type):
                return True

        return False

    @property
    def overrides(self):
        if self.__overrides is None:
            self.__overrides = {}
            overrides = eos.db.getOverrides(self.ID)
            for x in overrides:
                if x.attr.name in self.__attributes:
                    self.__overrides[x.attr.name] = x

        return self.__overrides

    def setOverride(self, attr, value):
        from eos.saveddata.override import Override
        if attr.name in self.__overrides:
            override = self.__overrides.get(attr.name)
            override.value = value
        else:
            override = Override(self, attr, value)
            self.__overrides[attr.name] = override
        eos.db.save(override)

    def deleteOverride(self, attr):
        override = self.__overrides.pop(attr.name, None)
        eos.db.saveddata_session.delete(override)
        eos.db.commit()

    srqIDMap = {182: 277, 183: 278, 184: 279, 1285: 1286, 1289: 1287, 1290: 1288}

    @property
    def requiredSkills(self):
        if self.__requiredSkills is None:
            requiredSkills = OrderedDict()
            self.__requiredSkills = requiredSkills
            # Map containing attribute IDs we may need for required skills
            # { requiredSkillX : requiredSkillXLevel }
            combinedAttrIDs = set(self.srqIDMap.iterkeys()).union(set(self.srqIDMap.itervalues()))
            # Map containing result of the request
            # { attributeID : attributeValue }
            skillAttrs = {}
            # Get relevant attribute values from db (required skill IDs and levels) for our item
            for attrInfo in eos.db.directAttributeRequest((self.ID,), tuple(combinedAttrIDs)):
                attrID = attrInfo[1]
                attrVal = attrInfo[2]
                skillAttrs[attrID] = attrVal
            # Go through all attributeID pairs
            for srqIDAtrr, srqLvlAttr in self.srqIDMap.iteritems():
                # Check if we have both in returned result
                if srqIDAtrr in skillAttrs and srqLvlAttr in skillAttrs:
                    skillID = int(skillAttrs[srqIDAtrr])
                    skillLvl = skillAttrs[srqLvlAttr]
                    # Fetch item from database and fill map
                    item = eos.db.getItem(skillID)
                    requiredSkills[item] = skillLvl
        return self.__requiredSkills

    @property
    def requiredFor(self):
        if self.__requiredFor is None:
            self.__requiredFor = dict()

            # Map containing attribute IDs we may need for required skills

            # Get relevant attribute values from db (required skill IDs and levels) for our item
            q = eos.db.getRequiredFor(self.ID, self.srqIDMap)

            for itemID, lvl in q:
                # Fetch item from database and fill map
                item = eos.db.getItem(itemID)
                self.__requiredFor[item] = lvl

        return self.__requiredFor

    factionMap = {
        500001: "caldari",
        500002: "minmatar",
        500003: "amarr",
        500004: "gallente",
        500005: "jove",
        500010: "guristas",
        500011: "angel",
        500012: "blood",
        500014: "ore",
        500016: "sisters",
        500018: "mordu",
        500019: "sansha",
        500020: "serpentis"
    }

    @property
    def race(self):
        if self.__race is None:

            try:
                if self.category.categoryName == 'Structure':
                    self.__race = "upwell"
                else:
                    self.__race = self.factionMap[self.factionID]
            # Some ships (like few limited issue ships) do not have factionID set,
            # thus keep old mechanism for now
            except KeyError:
                # Define race map
                race_map = {
                    1  : "caldari",
                    2  : "minmatar",
                    4  : "amarr",
                    5  : "sansha",  # Caldari + Amarr
                    6  : "blood",  # Minmatar + Amarr
                    8  : "gallente",
                    9  : "guristas",  # Caldari + Gallente
                    10 : "angelserp",  # Minmatar + Gallente, final race depends on the order of skills
                    12 : "sisters",  # Amarr + Gallente
                    16 : "jove",
                    32 : "sansha",  # Incrusion Sansha
                    128: "ore"
                }
                # Race is None by default
                race = None
                # Check primary and secondary required skills' races
                if race is None:
                    skillRaces = tuple(filter(lambda rid: rid, (s.raceID for s in tuple(self.requiredSkills.keys()))))
                    if sum(skillRaces) in race_map:
                        race = race_map[sum(skillRaces)]
                        if race == "angelserp":
                            if skillRaces == (2, 8):
                                race = "angel"
                            else:
                                race = "serpentis"
                # Rely on item's own raceID as last resort
                if race is None:
                    race = race_map.get(self.raceID, None)
                # Store our final value
                self.__race = race
        return self.__race

    @property
    def assistive(self):
        """Detects if item can be used as assistance"""
        # Make sure we cache results
        if self.__assistive is None:
            assistive = False
            # Go through all effects and find first assistive
            for effect in self.effects.itervalues():
                if effect.isAssistance is True:
                    # If we find one, stop and mark item as assistive
                    assistive = True
                    break
            self.__assistive = assistive
        return self.__assistive

    @property
    def offensive(self):
        """Detects if item can be used as something offensive"""
        # Make sure we cache results
        if self.__offensive is None:
            offensive = False
            # Go through all effects and find first offensive
            for effect in self.effects.itervalues():
                if effect.isOffensive is True:
                    # If we find one, stop and mark item as offensive
                    offensive = True
                    break
            self.__offensive = offensive
        return self.__offensive

    def requiresSkill(self, skill, level=None):
        for s, l in self.requiredSkills.iteritems():
            if isinstance(skill, basestring):
                if s.name == skill and (level is None or l == level):
                    return True

            elif isinstance(skill, int) and (level is None or l == level):
                if s.ID == skill:
                    return True

            elif skill == s and (level is None or l == level):
                return True

            elif hasattr(skill, "item") and skill.item == s and (level is None or l == level):
                return True

        return False

    @property
    def price(self):
        try:
            if self.__price is None:
                db_price = eos.db.getPrice(self.ID)
                # do not yet have a price in the database for this item, create one
                if db_price is None:
                    pyfalog.debug("Creating a price for {0}", self.ID)
                    self.__price = types_Price(self.ID)
                    eos.db.add(self.__price)
                    eos.db.commit()
                else:
                    self.__price = db_price
        except Exception as e:
            # We want to catch our failure and log it, but don't bail out for a single missing price tag.
            pyfalog.error("Failed to get price for typeID: {0}", self.ID)
            pyfalog.error(e)

            if not hasattr(self, '__price'):
                self.__price = types_Price(self.ID)
            else:
                if not self.__price.price:
                    self.__price.price = 0
            self.__price.failed = True

        return self.__price

    @property
    def slot(self):
        effectSlotMap = {
            "rigSlot"    : Slot.RIG,
            "loPower"    : Slot.LOW,
            "medPower"   : Slot.MED,
            "hiPower"    : Slot.HIGH,
            "subSystem"  : Slot.SUBSYSTEM,
            "serviceSlot": Slot.SERVICE
        }
        if self is None:
            return None
        for effectName, slot in effectSlotMap.iteritems():
            if effectName in self.effects:
                return slot
        if self.group.name == "Effect Beacon":
            return Slot.SYSTEM

    def __repr__(self):
        return u"Item(ID={}, name={}) at {}".format(
                self.ID, self.name, hex(id(self))
        )


class MetaData(EqBase):
    pass


class ItemEffect(EqBase):
    pass


class AttributeInfo(EqBase):
    pass


class Attribute(EqBase):
    pass


class Category(EqBase):
    pass


class AlphaClone(EqBase):
    @reconstructor
    def init(self):
        self.skillCache = {}

        for x in self.skills:
            self.skillCache[x.typeID] = x

    def getSkillLevel(self, skill):
        if skill.item.ID in self.skillCache:
            return self.skillCache[skill.item.ID].level
        else:
            return None


class AlphaCloneSkill(EqBase):
    pass


class Group(EqBase):
    pass


class Icon(EqBase):
    pass


class MarketGroup(EqBase):
    def __repr__(self):
        return u"MarketGroup(ID={}, name={}, parent={}) at {}".format(
                self.ID, self.name, getattr(self.parent, "name", None), hex(id(self))
        ).encode('utf8')


class MetaGroup(EqBase):
    pass


class MetaType(EqBase):
    pass


class Unit(EqBase):
    pass


class Traits(EqBase):
    pass
