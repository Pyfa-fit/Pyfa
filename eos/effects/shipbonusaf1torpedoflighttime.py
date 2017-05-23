# shipBonusAF1TorpedoFlightTime
#
# Used by:
# Ship: Purifier
effectType = "passive"


def handler(fit, ship, context):
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Torpedoes"),
                                    "explosionDelay", ship.getModifiedItemAttr("shipBonusAF"), skill="Amarr Frigate")
