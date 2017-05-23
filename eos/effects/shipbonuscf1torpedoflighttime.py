# shipBonusCF1TorpedoFlightTime
#
# Used by:
# Ship: Manticore
effectType = "passive"


def handler(fit, ship, context):
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Torpedoes"),
                                    "explosionDelay", ship.getModifiedItemAttr("shipBonusCF"), skill="Caldari Frigate")
