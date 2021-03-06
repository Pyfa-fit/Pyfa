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

import time
from copy import deepcopy
from itertools import chain
from math import log, asinh
import datetime

from sqlalchemy.orm import validates, reconstructor
from sqlalchemy.exc import InvalidRequestError
from eos.gnosis import GnosisFormulas, GnosisSimulation

import eos.db
from eos.effectHandlerHelpers import HandledModuleList, HandledDroneCargoList, HandledImplantBoosterList, HandledProjectedDroneList, HandledProjectedModList
from eos.enum import Enum
from eos.saveddata.ship import Ship
from eos.saveddata.drone import Drone
from eos.saveddata.character import Character
from eos.saveddata.citadel import Citadel
from eos.saveddata.module import Module, State, Slot
from logbook import Logger

pyfalog = Logger(__name__)


class ImplantLocation(Enum):
    FIT = 0
    CHARACTER = 1


class Fit(object):
    """Represents a fitting, with modules, ship, implants, etc."""

    PEAK_RECHARGE = 0.25

    def __init__(self, ship=None, name=""):
        """Initialize a fit from the program"""
        # use @mode.setter's to set __attr and IDs. This will set mode as well
        self.ship = ship
        if self.ship:
            self.ship.parent = self

        self.__modules = HandledModuleList()
        self.__drones = HandledDroneCargoList()
        self.__fighters = HandledDroneCargoList()
        self.__cargo = HandledDroneCargoList()
        self.__implants = HandledImplantBoosterList()
        self.__boosters = HandledImplantBoosterList()
        # self.__projectedFits = {}
        self.__projectedModules = HandledProjectedModList()
        self.__projectedDrones = HandledProjectedDroneList()
        self.__projectedFighters = HandledProjectedDroneList()
        self.__character = None
        self.__owner = None

        self.projected = False
        self.name = name
        self.timestamp = time.time()
        self.created = None
        self.modified = None
        self.modeID = None

        self.build()

    @reconstructor
    def init(self):
        """Initialize a fit from the database and validate"""
        self.__ship = None
        self.__mode = None

        if self.shipID:
            item = eos.db.getItem(self.shipID)
            if item is None:
                pyfalog.error("Item (id: {0}) does not exist", self.shipID)
                return

            try:
                try:
                    self.__ship = Ship(item, self)
                except ValueError:
                    self.__ship = Citadel(item, self)
                # @todo extra attributes is now useless, however it set to be
                # the same as ship attributes for ease (so we don't have to
                # change all instances in source). Remove this at some point
                self.extraAttributes = self.__ship.itemModifiedAttributes
            except ValueError:
                pyfalog.error("Item (id: {0}) is not a Ship", self.shipID)
                return

        if self.modeID and self.__ship:
            item = eos.db.getItem(self.modeID)
            # Don't need to verify if it's a proper item, as validateModeItem assures this
            self.__mode = self.ship.validateModeItem(item)
        else:
            self.__mode = self.ship.validateModeItem(None)

        self.build()

    def build(self):
        self.__extraDrains = []
        self.__ehp = None
        self.__weaponDPS = None
        self.__minerYield = None
        self.__weaponVolley = None
        self.__droneDPS = None
        self.__droneVolley = None
        self.__droneYield = None
        self.__sustainableTank = None
        self.__effectiveSustainableTank = None
        self.__effectiveTank = None
        self.__calculated = False
        self.__capStable = None
        self.__capState = None
        self.__capUsed = None
        self.__capRecharge = None
        self.__calculatedTargets = []
        self.__remoteReps = {
            "Armor"    : None,
            "Shield"   : None,
            "Hull"     : None,
            "Capacitor": None,
        }
        self.factorReload = False
        self.boostsFits = set()
        self.gangBoosts = None
        self.ecmProjectedStr = 1
        self.commandBonuses = {}

    @property
    def targetResists(self):
        return self.__targetResists

    @targetResists.setter
    def targetResists(self, targetResists):
        self.__targetResists = targetResists
        self.__weaponDPS = None
        self.__weaponVolley = None
        self.__droneDPS = None
        self.__droneVolley = None

    @property
    def damagePattern(self):
        return self.__damagePattern

    @damagePattern.setter
    def damagePattern(self, damagePattern):
        self.__damagePattern = damagePattern
        self.__ehp = None
        self.__effectiveTank = None

    @property
    def isInvalid(self):
        return self.__ship is None

    @property
    def mode(self):
        return self.__mode

    @mode.setter
    def mode(self, mode):
        self.__mode = mode
        self.modeID = mode.item.ID if mode is not None else None

    @property
    def modifiedCoalesce(self):
        """
        This is a property that should get whichever date is available for the fit. @todo: migrate old timestamp data
        and ensure created / modified are set in database to get rid of this
        """
        return self.modified or self.created or datetime.datetime.fromtimestamp(self.timestamp)

    @property
    def character(self):
        return self.__character if self.__character is not None else Character.getAll0()

    @character.setter
    def character(self, char):
        self.__character = char

    @property
    def calculated(self):
        return self.__calculated

    @calculated.setter
    def calculated(self, value):
        # todo: brief explaination hwo this works
        self.__calculated = value

    @property
    def ship(self):
        return self.__ship

    @ship.setter
    def ship(self, ship):
        self.__ship = ship
        self.shipID = ship.item.ID if ship is not None else None
        if ship is not None:
            #  set mode of new ship
            self.mode = self.ship.validateModeItem(None) if ship is not None else None
            # set fit attributes the same as ship
            self.extraAttributes = self.ship.itemModifiedAttributes

    @property
    def isStructure(self):
        return isinstance(self.ship, Citadel)

    @property
    def drones(self):
        return self.__drones

    @property
    def fighters(self):
        return self.__fighters

    @property
    def cargo(self):
        return self.__cargo

    @property
    def modules(self):
        return self.__modules

    @property
    def implants(self):
        return self.__implants

    @property
    def boosters(self):
        return self.__boosters

    @property
    def projectedModules(self):
        return self.__projectedModules

    @property
    def projectedFits(self):
        # only in extreme edge cases will the fit be invalid, but to be sure do
        # not return them.
        return [fit for fit in self.__projectedFits.values() if not fit.isInvalid]

    @property
    def commandFits(self):
        return [fit for fit in self.__commandFits.values() if not fit.isInvalid]

    def getProjectionInfo(self, fitID):
        return self.projectedOnto.get(fitID, None)

    def getCommandInfo(self, fitID):
        return self.boostedOnto.get(fitID, None)

    @property
    def projectedDrones(self):
        return self.__projectedDrones

    @property
    def projectedFighters(self):
        return self.__projectedFighters

    @property
    def weaponDPS(self):
        if self.__weaponDPS is None:
            self.calculateWeaponStats()

        return self.__weaponDPS

    @property
    def weaponVolley(self):
        if self.__weaponVolley is None:
            self.calculateWeaponStats()

        return self.__weaponVolley

    @property
    def droneDPS(self):
        if self.__droneDPS is None:
            self.calculateWeaponStats()

        return self.__droneDPS

    @property
    def droneVolley(self):
        if self.__droneVolley is None:
            self.calculateWeaponStats()

        return self.__droneVolley

    @property
    def totalDPS(self):
        return self.droneDPS + self.weaponDPS

    @property
    def totalVolley(self):
        return self.droneVolley + self.weaponVolley

    @property
    def minerYield(self):
        if self.__minerYield is None:
            self.calculateMiningStats()

        return self.__minerYield

    @property
    def droneYield(self):
        if self.__droneYield is None:
            self.calculateMiningStats()

        return self.__droneYield

    @property
    def totalYield(self):
        return self.droneYield + self.minerYield

    @property
    def maxTargets(self):
        return min(self.extraAttributes["maxTargetsLockedFromSkills"],
                   self.ship.getModifiedItemAttr("maxLockedTargets"))

    @property
    def maxTargetRange(self):
        return self.ship.getModifiedItemAttr("maxTargetRange")

    @property
    def scanStrength(self):
        return max([self.ship.getModifiedItemAttr("scan%sStrength" % scanType)
                    for scanType in ("Magnetometric", "Ladar", "Radar", "Gravimetric")])

    @property
    def scanType(self):
        maxStr = -1
        sensor_type = None
        for scanType in ("Magnetometric", "Ladar", "Radar", "Gravimetric"):
            currStr = self.ship.getModifiedItemAttr("scan%sStrength" % scanType)
            if currStr > maxStr:
                maxStr = currStr
                sensor_type = scanType
            elif currStr == maxStr:
                sensor_type = "Multispectral"

        return sensor_type

    @property
    def jamChance(self):
        return (1 - self.ecmProjectedStr) * 100

    @property
    def maxSpeed(self):
        speedLimit = self.ship.getModifiedItemAttr("speedLimit")
        if speedLimit and self.ship.getModifiedItemAttr("maxVelocity") > speedLimit:
            return speedLimit

        return self.ship.getModifiedItemAttr("maxVelocity")

    @property
    def alignTime(self):
        agility = self.ship.getModifiedItemAttr("agility") or 0
        mass = self.ship.getModifiedItemAttr("mass")

        return -log(0.25) * agility * mass / 1000000

    @property
    def implantSource(self):
        return self.implantLocation

    @implantSource.setter
    def implantSource(self, source):
        self.implantLocation = source

    @property
    def appliedImplants(self):
        if self.implantLocation == ImplantLocation.CHARACTER:
            return self.character.implants
        else:
            return self.implants

    @validates("ID", "ownerID", "shipID")
    def validator(self, key, val):
        _map = {
            "ID"     : lambda _val: isinstance(_val, int),
            "ownerID": lambda _val: isinstance(_val, int) or _val is None,
            "shipID" : lambda _val: isinstance(_val, int) or _val is None
        }

        if not _map[key](val):
            raise ValueError(str(val) + " is not a valid value for " + key)
        else:
            return val

    def clear(self, projected=False):
        self.__effectiveTank = None
        self.__weaponDPS = None
        self.__minerYield = None
        self.__weaponVolley = None
        self.__effectiveSustainableTank = None
        self.__sustainableTank = None
        self.__droneDPS = None
        self.__droneVolley = None
        self.__droneYield = None
        self.__ehp = None
        self.calculated = False
        self.__capStable = None
        self.__capState = None
        self.__capUsed = None
        self.__capRecharge = None
        self.ecmProjectedStr = 1
        self.commandBonuses = {}

        for remoterep_type in self.__remoteReps:
            self.__remoteReps[remoterep_type] = None

        del self.__calculatedTargets[:]
        del self.__extraDrains[:]

        if self.ship:
            self.ship.clear()

        c = chain(
                self.modules,
                self.drones,
                self.fighters,
                self.boosters,
                self.implants,
                self.projectedDrones,
                self.projectedModules,
                self.projectedFighters,
                (self.character, self.extraAttributes),
        )

        for stuff in c:
            if stuff is not None and stuff != self:
                stuff.clear()

        # If this is the active fit that we are clearing, not a projected fit,
        # then this will run and clear the projected ships and flag the next
        # iteration to skip this part to prevent recursion.
        if not projected:
            for stuff in self.projectedFits:
                if stuff is not None and stuff != self:
                    stuff.clear(projected=True)

    # Methods to register and get the thing currently affecting the fit,
    # so we can correctly map "Affected By"
    def register(self, currModifier, origin=None):
        self.__modifier = currModifier
        self.__origin = origin
        if hasattr(currModifier, "itemModifiedAttributes"):
            if hasattr(currModifier.itemModifiedAttributes, "fit"):
                currModifier.itemModifiedAttributes.fit = origin or self
        if hasattr(currModifier, "chargeModifiedAttributes"):
            if hasattr(currModifier.itemModifiedAttributes, "fit"):
                currModifier.chargeModifiedAttributes.fit = origin or self

    def getModifier(self):
        return self.__modifier

    def getOrigin(self):
        return self.__origin

    def addCommandBonus(self, warfareBuffID, value, _module, effect, runTime="normal"):
        # oh fuck this is so janky
        # @todo should we pass in min/max to this function, or is abs okay?
        # (abs is old method, ccp now provides the aggregate function in their data)
        if warfareBuffID not in self.commandBonuses or abs(self.commandBonuses[warfareBuffID][1]) < abs(value):
            self.commandBonuses[warfareBuffID] = (runTime, value, _module, effect)

    def __runCommandBoosts(self, runTime="normal"):
        pyfalog.debug(u"Applying gang boosts for {0}", self.name)
        for warfareBuffID in self.commandBonuses.keys():
            # Unpack all data required to run effect properly
            effect_runTime, value, thing, effect = self.commandBonuses[warfareBuffID]

            if runTime != effect_runTime:
                continue

            # This should always be a gang effect, otherwise it wouldn't be added to commandBonuses
            # @todo: Check this
            if effect.isType("gang"):
                self.register(thing)

                if warfareBuffID == 10:  # Shield Burst: Shield Harmonizing: Shield Resistance
                    for damageType in ("Em", "Explosive", "Thermal", "Kinetic"):
                        self.ship.boostItemAttr("shield%sDamageResonance" % damageType, value, stackingPenalties=True)

                if warfareBuffID == 11:  # Shield Burst: Active Shielding: Repair Duration/Capacitor
                    self.modules.filteredItemBoost(
                            lambda mod: mod.item.requiresSkill("Shield Operation") or mod.item.requiresSkill(
                                    "Shield Emission Systems"), "capacitorNeed", value)
                    self.modules.filteredItemBoost(
                            lambda mod: mod.item.requiresSkill("Shield Operation") or mod.item.requiresSkill(
                                    "Shield Emission Systems"), "duration", value)

                if warfareBuffID == 12:  # Shield Burst: Shield Extension: Shield HP
                    self.ship.boostItemAttr("shieldCapacity", value, stackingPenalties=True)

                if warfareBuffID == 13:  # Armor Burst: Armor Energizing: Armor Resistance
                    for damageType in ("Em", "Thermal", "Explosive", "Kinetic"):
                        self.ship.boostItemAttr("armor%sDamageResonance" % damageType, value, stackingPenalties=True)

                if warfareBuffID == 14:  # Armor Burst: Rapid Repair: Repair Duration/Capacitor
                    self.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Remote Armor Repair Systems") or
                                                               mod.item.requiresSkill("Repair Systems"),
                                                   "capacitorNeed", value)
                    self.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Remote Armor Repair Systems") or
                                                               mod.item.requiresSkill("Repair Systems"),
                                                   "duration", value)

                if warfareBuffID == 15:  # Armor Burst: Armor Reinforcement: Armor HP
                    self.ship.boostItemAttr("armorHP", value, stackingPenalties=True)

                if warfareBuffID == 16:  # Information Burst: Sensor Optimization: Scan Resolution
                    self.ship.boostItemAttr("scanResolution", value, stackingPenalties=True)

                if warfareBuffID == 17:  # Information Burst: Electronic Superiority: EWAR Range and Strength
                    groups = ("ECM", "Sensor Dampener", "Weapon Disruptor", "Target Painter")
                    self.modules.filteredItemBoost(lambda mod: mod.item.group.name in groups, "maxRange", value,
                                                   stackingPenalties=True)
                    self.modules.filteredItemBoost(lambda mod: mod.item.group.name in groups,
                                                   "falloffEffectiveness", value, stackingPenalties=True)

                    for scanType in ("Magnetometric", "Radar", "Ladar", "Gravimetric"):
                        self.modules.filteredItemBoost(lambda mod: mod.item.group.name == "ECM",
                                                       "scan%sStrengthBonus" % scanType, value,
                                                       stackingPenalties=True)

                    for attr in ("missileVelocityBonus", "explosionDelayBonus", "aoeVelocityBonus", "falloffBonus",
                                 "maxRangeBonus", "aoeCloudSizeBonus", "trackingSpeedBonus"):
                        self.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Weapon Disruptor",
                                                       attr, value)

                    for attr in ("maxTargetRangeBonus", "scanResolutionBonus"):
                        self.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Sensor Dampener",
                                                       attr, value)

                    self.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Target Painter",
                                                   "signatureRadiusBonus", value, stackingPenalties=True)

                if warfareBuffID == 18:  # Information Burst: Electronic Hardening: Scan Strength
                    for scanType in ("Gravimetric", "Radar", "Ladar", "Magnetometric"):
                        self.ship.boostItemAttr("scan%sStrength" % scanType, value, stackingPenalties=True)

                if warfareBuffID == 19:  # Information Burst: Electronic Hardening: RSD/RWD Resistance
                    self.ship.boostItemAttr("sensorDampenerResistance", value)
                    self.ship.boostItemAttr("weaponDisruptionResistance", value)

                if warfareBuffID == 26:  # Information Burst: Sensor Optimization: Targeting Range
                    self.ship.boostItemAttr("maxTargetRange", value)

                if warfareBuffID == 20:  # Skirmish Burst: Evasive Maneuvers: Signature Radius
                    self.ship.boostItemAttr("signatureRadius", value, stackingPenalties=True)

                if warfareBuffID == 21:  # Skirmish Burst: Interdiction Maneuvers: Tackle Range
                    groups = ("Stasis Web", "Warp Scrambler")
                    self.modules.filteredItemBoost(lambda mod: mod.item.group.name in groups, "maxRange", value,
                                                   stackingPenalties=True)

                if warfareBuffID == 22:  # Skirmish Burst: Rapid Deployment: AB/MWD Speed Increase
                    self.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Afterburner") or
                                                               mod.item.requiresSkill("High Speed Maneuvering"),
                                                   "speedFactor", value, stackingPenalties=True)

                if warfareBuffID == 23:  # Mining Burst: Mining Laser Field Enhancement: Mining/Survey Range
                    self.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Mining") or
                                                               mod.item.requiresSkill("Ice Harvesting") or
                                                               mod.item.requiresSkill("Gas Cloud Harvesting"),
                                                   "maxRange", value, stackingPenalties=True)

                    self.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("CPU Management"),
                                                   "surveyScanRange", value, stackingPenalties=True)

                if warfareBuffID == 24:  # Mining Burst: Mining Laser Optimization: Mining Capacitor/Duration
                    self.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Mining") or
                                                               mod.item.requiresSkill("Ice Harvesting") or
                                                               mod.item.requiresSkill("Gas Cloud Harvesting"),
                                                   "capacitorNeed", value, stackingPenalties=True)

                    self.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Mining") or
                                                               mod.item.requiresSkill("Ice Harvesting") or
                                                               mod.item.requiresSkill("Gas Cloud Harvesting"),
                                                   "duration", value, stackingPenalties=True)

                if warfareBuffID == 25:  # Mining Burst: Mining Equipment Preservation: Crystal Volatility
                    self.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Mining"),
                                                   "crystalVolatilityChance", value, stackingPenalties=True)

                if warfareBuffID == 60:  # Skirmish Burst: Evasive Maneuvers: Agility
                    self.ship.boostItemAttr("agility", value, stackingPenalties=True)

                # Titan effects

                if warfareBuffID == 39:  # Avatar Effect Generator : Capacitor Recharge bonus
                    self.ship.boostItemAttr("rechargeRate", value, stackingPenalties=True)

                if warfareBuffID == 40:  # Avatar Effect Generator : Kinetic resistance bonus
                    for attr in ("armorKineticDamageResonance", "shieldKineticDamageResonance", "kineticDamageResonance"):
                        self.ship.boostItemAttr(attr, value, stackingPenalties=True)

                if warfareBuffID == 41:  # Avatar Effect Generator : EM resistance penalty
                    for attr in ("armorEmDamageResonance", "shieldEmDamageResonance", "emDamageResonance"):
                        self.ship.boostItemAttr(attr, value, stackingPenalties=True)

                if warfareBuffID == 42:  # Erebus Effect Generator : Armor HP bonus
                    self.ship.boostItemAttr("armorHP", value, stackingPenalties=True)

                if warfareBuffID == 43:  # Erebus Effect Generator : Explosive resistance bonus
                    for attr in ("armorExplosiveDamageResonance", "shieldExplosiveDamageResonance", "explosiveDamageResonance"):
                        self.ship.boostItemAttr(attr, value, stackingPenalties=True)

                if warfareBuffID == 44:  # Erebus Effect Generator : Thermal resistance penalty
                    for attr in ("armorThermalDamageResonance", "shieldThermalDamageResonance", "thermalDamageResonance"):
                        self.ship.boostItemAttr(attr, value, stackingPenalties=True)

                if warfareBuffID == 45:  # Ragnarok Effect Generator : Signature Radius bonus
                    self.ship.boostItemAttr("signatureRadius", value, stackingPenalties=True)

                if warfareBuffID == 46:  # Ragnarok Effect Generator : Thermal resistance bonus
                    for attr in ("armorThermalDamageResonance", "shieldThermalDamageResonance", "thermalDamageResonance"):
                        self.ship.boostItemAttr(attr, value, stackingPenalties=True)

                if warfareBuffID == 47:  # Ragnarok Effect Generator : Explosive resistance penaly
                    for attr in ("armorExplosiveDamageResonance", "shieldExplosiveDamageResonance", "explosiveDamageResonance"):
                        self.ship.boostItemAttr(attr, value, stackingPenalties=True)

                if warfareBuffID == 48:  # Leviathan Effect Generator : Shield HP bonus
                    self.ship.boostItemAttr("shieldCapacity", value, stackingPenalties=True)

                if warfareBuffID == 49:  # Leviathan Effect Generator : EM resistance bonus
                    for attr in ("armorEmDamageResonance", "shieldEmDamageResonance", "emDamageResonance"):
                        self.ship.boostItemAttr(attr, value, stackingPenalties=True)

                if warfareBuffID == 50:  # Leviathan Effect Generator : Kinetic resistance penalty
                    for attr in ("armorKineticDamageResonance", "shieldKineticDamageResonance", "kineticDamageResonance"):
                        self.ship.boostItemAttr(attr, value, stackingPenalties=True)

                if warfareBuffID == 51:  # Avatar Effect Generator : Velocity penalty
                    self.ship.boostItemAttr("maxVelocity", value, stackingPenalties=True)

                if warfareBuffID == 52:  # Erebus Effect Generator : Shield RR penalty
                    self.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Emission Systems"), "shieldBonus", value, stackingPenalties=True)

                if warfareBuffID == 53:  # Leviathan Effect Generator : Armor RR penalty
                    self.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Remote Armor Repair Systems"),
                                                   "armorDamageAmount", value, stackingPenalties=True)

                if warfareBuffID == 54:  # Ragnarok Effect Generator : Laser and Hybrid Optimal penalty
                    groups = ("Energy Weapon", "Hybrid Weapon")
                    self.modules.filteredItemBoost(lambda mod: mod.item.group.name in groups, "maxRange", value, stackingPenalties=True)

            del self.commandBonuses[warfareBuffID]

    def calculateFitAttributes(self, targetFit=None, withBoosters=False):
        """
        This method handles recursion through the chain of fit, projected fits, and command fits.  We start from our current fit (self), then recurse up through
        the chain of projected fits.  Because this is self recursive, each level will then recurse further up the chain.  We then do the same for command fits
        (bursts or formerly gang links).

        In practice if we have Fit B projected onto Fit A, and Fit C projected onto Fit B, it will end up looking like:
        - Find Fit A, process projected fits
        - Find Fit B, process projected fits
        - Find Fit C, no projected fits.
        - Calculate Fit C
        - Project Fit C onto Fit B
        - Calculate Fit B
        - Project Fit B onto Fit A
        - Calculate Fit A

        :param targetFit:

        :param withBoosters:
        :return:
        """

        pyfalog.debug("Starting fit calculation.")

        if withBoosters:
            # Recalc ships projecting onto this fit
            for projected_fit in self.projectedFits:
                if projected_fit.getProjectionInfo(self.ID).active:
                    if projected_fit is self:
                        # If fit is self, don't recurse
                        self.calculateModifiedFitAttributes(targetFit=self)
                    else:
                        for projected_command_fit in projected_fit.commandFits:
                            projected_onto = projected_command_fit.getCommandInfo(projected_fit)
                            if getattr(projected_onto, 'active', None):
                                if projected_command_fit.calculated is not True:
                                    # The command fit isn't calced, so force the fit below it in the chain to recalc
                                    projected_fit.calculated = False
                                projected_command_fit.calculateModifiedFitAttributes()
                                projected_command_fit.calculateModifiedFitAttributes(targetFit=projected_fit)

                        projected_fit.calculateModifiedFitAttributes()
                        projected_fit.calculateModifiedFitAttributes(targetFit=self)

            for command_fit in self.commandFits:
                projected_onto = command_fit.getCommandInfo(self.ID)
                if getattr(projected_onto, 'active', None):
                    if command_fit is self:
                        # If fit is self, don't recurse
                        self.calculateModifiedFitAttributes(targetFit=self)
                    else:
                        command_fit.calculateModifiedFitAttributes()
                        command_fit.calculateModifiedFitAttributes(targetFit=self)

        self.calculateModifiedFitAttributes()

    def calculateModifiedFitAttributes(self, targetFit=None):
        """
        Calculates a fits atttributes.

        :param targetFit:
        If a target fit is specified, will project onto the target fit.
        If targetFit is the same as self, then we make a copy in order to properly project it without running into recursion issues.
        """

        shadow = None
        projectionInfo = None
        if targetFit:
            pyfalog.info(u"Calculating projections from {0} to target {1}", self.name, targetFit.name)
            projectionInfo = self.getProjectionInfo(targetFit.ID)
            pyfalog.debug("ProjectionInfo: {0}", projectionInfo)
            if self is targetFit:
                # Make a copy of our fit.  targetFit stays as the original, self becomes the copy.
                # noinspection PyNoneFunctionAssignment
                shadow = deepcopy(targetFit)
                # noinspection PyMethodFirstArgAssignment
                self = shadow
                pyfalog.debug("Handling self projection - making shadow copy of fit.")
        else:
            pyfalog.info("Calculating fit {0}", self.name)

        # If fit is calculated and we have nothing to do here, get out

        # A note on why projected fits don't get to return here. If we return
        # here, the projection afflictions will not be run as they are
        # intertwined into the regular fit calculations. So, even if the fit has
        # been calculated, we need to recalculate it again just to apply the
        # projections. This is in contract to gang boosts, which are only
        # calculated once, and their items are then looped and accessed with
        #     self.gangBoosts.iteritems()
        # We might be able to exit early in the fit calculations if we separate
        # projections from the normal fit calculations. But we must ensure that
        # projection have modifying stuff applied, such as gang boosts and other
        # local modules that may help
        if self.calculated and not targetFit:
            pyfalog.debug("Fit has already been calculated and is not projected, returning: {0}", self)
            return

        # Loop through our run times here. These determine which effects are run in which order.
        for runTime in ("early", "normal", "late"):
            pyfalog.debug("Run time: {0}", runTime)
            u = [
                # Items that are unrestricted. These items are run on the local fit
                # first and then projected onto the target fit it one is designated
                (self.character, self.ship),
                self.drones,
                self.fighters,
                self.boosters,
                self.appliedImplants,
                self.modules
            ] if not self.isStructure else [
                # Ensure a restricted set for citadels
                (self.character, self.ship),
                self.fighters,
                self.modules
            ]

            # Items that are restricted. These items are only run on the local
            # fit. They are NOT projected onto the target fit. # See issue 354
            r = [(self.mode,), self.projectedDrones, self.projectedFighters, self.projectedModules]

            # chain unrestricted and restricted into one iterable
            c = chain.from_iterable(u + r)

            for item in c:
                # Registering the item about to affect the fit allows us to
                # track "Affected By" relations correctly
                if item is not None:
                    if hasattr(item, 'item'):
                        item_name = getattr(item.item, 'name', getattr(item.item, 'ID', "Unknown"))
                    else:
                        item_name = getattr(item, 'name', getattr(item, 'ID', "Unknown"))

                    pyfalog.debug(u"Processing item: {0}", item_name)

                    if targetFit:
                        # Apply to projected fit
                        if item not in chain.from_iterable(r) and projectionInfo:
                            for _ in xrange(projectionInfo.amount):
                                targetFit.register(item, origin=self)
                                item.calculateModifiedAttributes(targetFit, runTime, True)
                        if item in self.modules:
                            item.calculateModifiedAttributes(targetFit, runTime, False, True)
                    else:
                        # Apply to local fit
                        self.register(item)
                        item.calculateModifiedAttributes(self, runTime, False)

            if self.commandBonuses and not targetFit:
                if len(self.commandBonuses) > 0:
                    # Apply command bursts
                    pyfalog.info("Command bonuses applied.")
                    self.__runCommandBoosts(runTime)

            pyfalog.debug('Done with runtime: {0}', runTime)

        if not targetFit:
            # Mark fit as calculated
            self.calculated = True

        if shadow:
            # Put our original fit back into self
            # noinspection PyMethodFirstArgAssignment,PyUnusedLocal
            self = targetFit
            # Cleanup after ourselves
            try:
                # we delete the fit because when we copy a fit, flush() is
                # called to properly handle projection updates. However, we do
                # not want to save this fit to the database, so simply remove it
                eos.db.saveddata_session.delete(shadow)
            except InvalidRequestError:
                # Older versions of SQLAlchemy are not forgiving of the delete command. Newer versions seem to use it more as a delete or expunge.
                # Test a pass here to see if we can just skip it, may need a refresh or other cleanup.
                pyfalog.warning("Caught InvalidRequestError when deleting the shadow fit out of the database.")
            del shadow

        pyfalog.debug('Done with fit calculation')

    def __runProjectionEffects(self, runTime, targetFit, projectionInfo):
        """
        To support a simpler way of doing self projections (so that we don't have to make a copy of the fit and
        recalculate), this function was developed to be a common source of projected effect application.
        """
        c = chain(self.drones, self.fighters, self.modules)
        for item in c:
            if item is not None:
                # apply effects onto target fit x amount of times
                for _ in xrange(projectionInfo.amount):
                    targetFit.register(item, origin=self)
                    item.calculateModifiedAttributes(targetFit, runTime, True)

    def fill(self):
        """
        Fill this fit's module slots with enough dummy slots so that all slots are used.
        This is mostly for making the life of gui's easier.
        GUI's can call fill() and then stop caring about empty slots completely.
        """
        if self.ship is None:
            return

        for slotType in (Slot.LOW, Slot.MED, Slot.HIGH, Slot.RIG, Slot.SUBSYSTEM, Slot.SERVICE):
            amount = self.getSlotsFree(slotType, True)
            if amount > 0:
                for _ in xrange(int(amount)):
                    self.modules.append(Module.buildEmpty(slotType))

            if amount < 0:
                # Look for any dummies of that type to remove
                toRemove = []
                for mod in self.modules:
                    if mod.isEmpty and mod.slot == slotType:
                        toRemove.append(mod)
                        amount += 1
                        if amount == 0:
                            break
                for mod in toRemove:
                    self.modules.remove(mod)

    def unfill(self):
        for i in xrange(len(self.modules) - 1, -1, -1):
            mod = self.modules[i]
            if mod.isEmpty:
                del self.modules[i]

    @property
    def modCount(self):
        x = 0
        for i in xrange(len(self.modules) - 1, -1, -1):
            mod = self.modules[i]
            if not mod.isEmpty:
                x += 1
        return x

    @staticmethod
    def getItemAttrSum(_dict, attr):
        amount = 0
        for mod in _dict:
            add = mod.getModifiedItemAttr(attr)
            if add is not None:
                amount += add

        return amount

    @staticmethod
    def getItemAttrOnlineSum(_dict, attr):
        amount = 0
        for mod in _dict:
            add = mod.getModifiedItemAttr(attr) if mod.state >= State.ONLINE else None
            if add is not None:
                amount += add

        return amount

    def getHardpointsUsed(self, hardpoint_type):
        amount = 0
        for mod in self.modules:
            if mod.hardpoint is hardpoint_type and not mod.isEmpty:
                amount += 1

        return amount

    def getSlotsUsed(self, slot_type, countDummies=False):
        amount = 0

        for mod in chain(self.modules, self.fighters):
            if mod.slot is slot_type and (not getattr(mod, "isEmpty", False) or countDummies):
                if slot_type in (Slot.F_HEAVY, Slot.F_SUPPORT, Slot.F_LIGHT) and not mod.active:
                    continue
                amount += 1

        return amount

    slots = {
        Slot.LOW      : "lowSlots",
        Slot.MED      : "medSlots",
        Slot.HIGH     : "hiSlots",
        Slot.RIG      : "rigSlots",
        Slot.SUBSYSTEM: "maxSubSystems",
        Slot.SERVICE  : "serviceSlots",
        Slot.F_LIGHT  : "fighterLightSlots",
        Slot.F_SUPPORT: "fighterSupportSlots",
        Slot.F_HEAVY  : "fighterHeavySlots"
    }

    def getSlotsFree(self, slot_type, countDummies=False):
        if slot_type in (Slot.MODE, Slot.SYSTEM):
            # These slots don't really exist, return default 0
            return 0

        slotsUsed = self.getSlotsUsed(slot_type, countDummies)
        totalSlots = self.ship.getModifiedItemAttr(self.slots[slot_type]) or 0
        return int(totalSlots - slotsUsed)

    def getNumSlots(self, slot_type):
        return self.ship.getModifiedItemAttr(self.slots[slot_type]) or 0

    @property
    def calibrationUsed(self):
        return self.getItemAttrOnlineSum(self.modules, 'upgradeCost')

    @property
    def pgUsed(self):
        return self.getItemAttrOnlineSum(self.modules, "power")

    @property
    def cpuUsed(self):
        return self.getItemAttrOnlineSum(self.modules, "cpu")

    @property
    def droneBandwidthUsed(self):
        amount = 0
        for d in self.drones:
            amount += d.getModifiedItemAttr("droneBandwidthUsed") * d.amountActive

        return amount

    @property
    def droneBayUsed(self):
        amount = 0
        for d in self.drones:
            amount += d.item.volume * d.amount

        return amount

    @property
    def fighterBayUsed(self):
        amount = 0
        for f in self.fighters:
            amount += f.item.volume * f.amountActive

        return amount

    @property
    def fighterTubesUsed(self):
        amount = 0
        for f in self.fighters:
            if f.active:
                amount += 1

        return amount

    @property
    def cargoBayUsed(self):
        amount = 0
        for c in self.cargo:
            amount += c.getModifiedItemAttr("volume") * c.amount

        return amount

    @property
    def activeDrones(self):
        amount = 0
        for d in self.drones:
            amount += d.amountActive

        return amount

    @property
    def probeSize(self):
        """
        Expresses how difficult a target is to probe down with scan probes
        """

        sigRad = self.ship.getModifiedItemAttr("signatureRadius")
        sensorStr = float(self.scanStrength)
        probeSize = sigRad / sensorStr if sensorStr != 0 else None
        # http://www.eveonline.com/ingameboard.asp?a=topic&threadID=1532170&page=2#42
        if probeSize is not None:
            # Probe size is capped at 1.08
            probeSize = max(probeSize, 1.08)
        return probeSize

    @property
    def warpSpeed(self):
        base = self.ship.getModifiedItemAttr("baseWarpSpeed") or 1
        multiplier = self.ship.getModifiedItemAttr("warpSpeedMultiplier") or 1
        return base * multiplier

    @property
    def maxWarpDistance(self):
        capacity = self.ship.getModifiedItemAttr("capacitorCapacity")
        mass = self.ship.getModifiedItemAttr("mass")
        warpCapNeed = self.ship.getModifiedItemAttr("warpCapacitorNeed")

        if not warpCapNeed:
            return 0

        return capacity / (mass * warpCapNeed)

    @property
    def capStable(self):
        if self.__capStable is None:
            self.simulateCap()

        return self.__capStable

    @property
    def capState(self):
        """
        If the cap is stable, the capacitor state is the % at which it is stable.
        If the cap is unstable, this is the amount of time before it runs out
        """
        if self.__capState is None:
            self.simulateCap()

        return self.__capState

    @property
    def capUsed(self):
        if self.__capUsed is None:
            self.simulateCap()

        return self.__capUsed

    @property
    def capRecharge(self):
        if self.__capRecharge is None:
            self.simulateCap()

        return self.__capRecharge

    @property
    def sustainableTank(self):
        if self.__sustainableTank is None:
            self.calculateSustainableTank()

        return self.__sustainableTank

    def calculateSustainableTank(self):
        total_shield_reps = 0
        total_armor_reps = 0
        total_hull_reps = 0

        simulation_matrix = GnosisSimulation.capacitor_simulation(self,
                                                                  self.__extraDrains,
                                                                  self.ship.getModifiedItemAttr("capacitorCapacity"),
                                                                  self.ship.getModifiedItemAttr("rechargeRate")
                                                                  )

        if simulation_matrix['Matrix']['Stability']['FailedToRunModules']:
            # Modules failed to run, so lets get the effective HP/s only after they failed
            start_recording_time = simulation_matrix['Matrix']['Stability']['FailedToRunModulesTime']
        else:
            start_recording_time = 0

        total_time = (simulation_matrix['Matrix']['Stability']['RunTime'] - start_recording_time) / 1000
        if total_time < 60:
            # This is an uncommon scenario, where we run out of cap *RIGHT* as the simulation ends.
            # In this case lets grab the last minute of stats.
            start_recording_time -= 60000
            total_time = 60

        for _ in simulation_matrix['Matrix']['Cached Runs']:
            if _['Current Time'] > start_recording_time:
                total_shield_reps += _['Shield Reps']
                total_armor_reps += _['Armor Reps']
                total_hull_reps += _['Hull Reps']

        sustainable = {
            "shieldRepair" : total_shield_reps / total_time,
            "armorRepair"  : total_armor_reps / total_time,
            "hullRepair"   : total_hull_reps / total_time,
            "passiveShield": self.calculateShieldRecharge()
        }

        # Check to make sure we're not over the maximum reps
        # This can occur if we cut off in the middle of a cycle
        # For example, AAR if we cut off right before a reload
        if sustainable["shieldRepair"] > self.extraAttributes.get("shieldRepair"):
            sustainable["shieldRepair"] = self.extraAttributes.get("shieldRepair")

        if sustainable["armorRepair"] > self.extraAttributes.get("armorRepair"):
            sustainable["armorRepair"] = self.extraAttributes.get("armorRepair")

        if sustainable["hullRepair"] > self.extraAttributes.get("hullRepair"):
            sustainable["hullRepair"] = self.extraAttributes.get("hullRepair")

        self.__sustainableTank = sustainable

        return self.__sustainableTank

    def calculateCapRecharge(self):
        peak_return = GnosisFormulas.get_peak_regen(self.ship.getModifiedItemAttr("capacitorCapacity"), self.ship.getModifiedItemAttr("rechargeRate"))
        return peak_return['DeltaAmount']

    def calculateShieldRecharge(self):
        peak_return = GnosisFormulas.get_peak_regen(self.ship.getModifiedItemAttr("shieldCapacity"),
                                                    self.ship.getModifiedItemAttr("shieldRechargeRate"))
        return peak_return['DeltaAmount']

    def addDrain(self, src, cycleTime, capNeed, clipSize=0):
        """ Used for both cap drains and cap fills (fills have negative capNeed) """

        energyNeutralizerSignatureResolution = src.getModifiedItemAttr("energyNeutralizerSignatureResolution")
        signatureRadius = self.ship.getModifiedItemAttr("signatureRadius")

        # Signature reduction, uses the bomb formula as per CCP Larrikin
        if energyNeutralizerSignatureResolution:
            capNeed *= min(1, signatureRadius / energyNeutralizerSignatureResolution)

        if self.ship.getModifiedItemAttr("energyWarfareResistance"):
            capNeed *= min(1, self.ship.getModifiedItemAttr("energyWarfareResistance"))

        self.__extraDrains.append((src, cycleTime, capNeed, clipSize))

    def simulateCap(self):
        simulation_matrix = GnosisSimulation.capacitor_simulation(self,
                                                                  self.__extraDrains,
                                                                  self.ship.getModifiedItemAttr("capacitorCapacity"),
                                                                  self.ship.getModifiedItemAttr("rechargeRate"))

        self.__capRecharge = GnosisFormulas.get_peak_regen(self.ship.getModifiedItemAttr("capacitorCapacity"),
                                                           self.ship.getModifiedItemAttr("rechargeRate"))

        cap_per_second = 0
        for module_list in simulation_matrix['ModuleDict']:
            if module_list['Charges']:
                total_run_time = module_list['CycleTime'] * module_list['Charges']
                total_amount = module_list['Amount'] * module_list['Charges']
            else:
                total_run_time = module_list['CycleTime']
                total_amount = module_list['Amount']

            if module_list['ReloadTime'] and module_list['Charges']:
                total_run_time += module_list['ReloadTime']

            if module_list['ReactivationDelay']:
                total_run_time += module_list['ReactivationDelay']

            if total_run_time > 0 and total_amount > 0:
                cap_per_second += total_amount / (total_run_time / 1000)

        self.__capUsed = cap_per_second

        if simulation_matrix['Matrix']['Stability']['FailedToRunModules']:
            # We ran our of cap to run modules.
            self.__capStable = 0
            self.__capState = simulation_matrix['Matrix']['Stability']['FailedToRunModulesTime']
        else:
            low_water_mark = simulation_matrix['Matrix']['Stability']['LowWaterMark']
            self.__capStable = round(low_water_mark / self.ship.getModifiedItemAttr("capacitorCapacity"), 2)
            self.__capState = simulation_matrix['Matrix']['Stability']['LowWaterMarkTime']

    @property
    def remoteReps(self):
        force_recalc = False
        for remote_type in self.__remoteReps:
            if self.__remoteReps[remote_type] is None:
                force_recalc = True
                break

        if force_recalc is False:
            return self.__remoteReps

        # We are rerunning the recalcs. Explicitly set to 0 to make sure we don't duplicate anything and correctly set
        # all values to 0.
        for remote_type in self.__remoteReps:
            self.__remoteReps[remote_type] = 0

        for stuff in chain(self.modules, self.drones):
            remote_type = None

            # Only apply the charged multiplier if we have a charge in our ancil reppers (#1135)
            if stuff.charge:
                fueledMultiplier = stuff.getModifiedItemAttr("chargedArmorDamageMultiplier", 1)
            else:
                fueledMultiplier = 1

            if isinstance(stuff, Module) and (stuff.isEmpty or stuff.state < State.ACTIVE):
                continue
            elif isinstance(stuff, Drone):
                # We only get one drone object, but may have multiple drones.  Add a multiplier so we get the correct total value.
                count = stuff.amountActive
            else:
                count = 1

            # Covert cycleTime to seconds
            duration = stuff.cycleTime / 1000

            # Skip modules with no duration.
            if not duration:
                continue

            remote_module_groups = {
                "Remote Armor Repairer"          : "Armor",
                "Ancillary Remote Armor Repairer": "Armor",
                "Remote Hull Repairer"           : "Hull",
                "Remote Shield Booster"          : "Shield",
                "Ancillary Remote Shield Booster": "Shield",
                "Remote Capacitor Transmitter"   : "Capacitor",
            }

            module_group = stuff.item.group.name

            if module_group in remote_module_groups:
                remote_type = remote_module_groups[module_group]
            elif not isinstance(stuff, Drone):
                # Module isn't in our list of remote rep modules, bail
                continue

            if remote_type == "Hull":
                hp = stuff.getModifiedItemAttr("structureDamageAmount", 0)
            elif remote_type == "Armor":
                hp = stuff.getModifiedItemAttr("armorDamageAmount", 0)
            elif remote_type == "Shield":
                hp = stuff.getModifiedItemAttr("shieldBonus", 0)
            elif remote_type == "Capacitor":
                hp = stuff.getModifiedItemAttr("powerTransferAmount", 0)
            else:
                droneShield = stuff.getModifiedItemAttr("shieldBonus", 0)
                droneArmor = stuff.getModifiedItemAttr("armorDamageAmount", 0)
                droneHull = stuff.getModifiedItemAttr("structureDamageAmount", 0)
                if droneShield:
                    remote_type = "Shield"
                    hp = droneShield
                elif droneArmor:
                    remote_type = "Armor"
                    hp = droneArmor
                elif droneHull:
                    remote_type = "Hull"
                    hp = droneHull
                else:
                    # Doesn't project anything remotely, skip
                    continue

            if hp > 0 and duration >= 0:
                # Occsaionally we get modules with no duration. Catch these so we don't stack trace with div by 0.
                self.__remoteReps[remote_type] += (hp * fueledMultiplier * count) / duration

        return self.__remoteReps

    @property
    def hp(self):
        hp = {}
        for (resist_type, attr) in (('shield', 'shieldCapacity'), ('armor', 'armorHP'), ('hull', 'hp')):
            hp[resist_type] = self.ship.getModifiedItemAttr(attr)

        return hp

    @property
    def ehp(self):
        if self.__ehp is None:
            if self.damagePattern is None:
                ehp = self.hp
            else:
                ehp = self.damagePattern.calculateEhp(self)
            self.__ehp = ehp

        return self.__ehp

    @property
    def tank(self):
        hps = {"passiveShield": self.calculateShieldRecharge()}
        for resist_type in ("shield", "armor", "hull"):
            hps["%sRepair" % resist_type] = self.extraAttributes["%sRepair" % resist_type]

        return hps

    @property
    def effectiveTank(self):
        if self.__effectiveTank is None:
            if self.damagePattern is None:
                ehps = self.tank
            else:
                ehps = self.damagePattern.calculateEffectiveTank(self, self.extraAttributes)

            self.__effectiveTank = ehps

        return self.__effectiveTank

    @property
    def effectiveSustainableTank(self):
        if self.__effectiveSustainableTank is None:
            if self.damagePattern is None:
                eshps = self.sustainableTank
            else:
                eshps = self.damagePattern.calculateEffectiveTank(self, self.sustainableTank)

            self.__effectiveSustainableTank = eshps

        return self.__effectiveSustainableTank

    def calculateLockTime(self, radius):
        scanRes = self.ship.getModifiedItemAttr("scanResolution")
        if scanRes is not None and scanRes > 0:
            # Yes, this function returns time in seconds, not miliseconds.
            # 40,000 is indeed the correct constant here.
            return min(40000 / scanRes / asinh(radius) ** 2, 30 * 60)
        else:
            return self.ship.getModifiedItemAttr("scanSpeed") / 1000.0

    def calculateMiningStats(self):
        minerYield = 0
        droneYield = 0

        for mod in self.modules:
            minerYield += mod.miningStats

        for drone in self.drones:
            droneYield += drone.miningStats

        self.__minerYield = minerYield
        self.__droneYield = droneYield

    def calculateWeaponStats(self):
        weaponDPS = 0
        droneDPS = 0
        weaponVolley = 0
        droneVolley = 0

        for mod in self.modules:
            dps, volley = mod.damageStats(self.targetResists)
            weaponDPS += dps
            weaponVolley += volley

        for drone in self.drones:
            dps, volley = drone.damageStats(self.targetResists)
            droneDPS += dps
            droneVolley += volley

        for fighter in self.fighters:
            dps, volley = fighter.damageStats(self.targetResists)
            droneDPS += dps
            droneVolley += volley

        self.__weaponDPS = weaponDPS
        self.__weaponVolley = weaponVolley
        self.__droneDPS = droneDPS
        self.__droneVolley = droneVolley

    @property
    def fits(self):
        for mod in self.modules:
            if not mod.isEmpty and not mod.fits(self):
                return False

        return True

    def __deepcopy__(self, memo=None):
        copy_ship = Fit()
        # Character and owner are not copied
        copy_ship.character = self.__character
        copy_ship.owner = self.owner
        copy_ship.ship = deepcopy(self.ship)
        copy_ship.name = "%s copy" % self.name
        copy_ship.damagePattern = self.damagePattern
        copy_ship.targetResists = self.targetResists
        copy_ship.notes = self.notes

        toCopy = (
            "modules",
            "drones",
            "fighters",
            "cargo",
            "implants",
            "boosters",
            "projectedModules",
            "projectedDrones",
            "projectedFighters")
        for name in toCopy:
            orig = getattr(self, name)
            c = getattr(copy_ship, name)
            for i in orig:
                c.append(deepcopy(i))

        for fit in self.projectedFits:
            copy_ship.__projectedFits[fit.ID] = fit
            # this bit is required -- see GH issue # 83
            eos.db.saveddata_session.flush()
            eos.db.saveddata_session.refresh(fit)

        return copy_ship

    def __repr__(self):
        return u"Fit(ID={}, ship={}, name={}) at {}".format(
                self.ID, self.ship.item.name, self.name, hex(id(self))
        ).encode('utf8')

    def __str__(self):
        return u"{} ({})".format(
                self.name, self.ship.item.name
        ).encode('utf8')
