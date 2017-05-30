# shipBonusGF1TorpedoFlightTime
#
# Used by:
# Ship: Nemesis
effectType = "passive"


def handler(fit, ship, context):
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Torpedoes"),
                                    "explosionDelay", ship.getModifiedItemAttr("shipBonusGF"), skill="Gallente Frigate")
