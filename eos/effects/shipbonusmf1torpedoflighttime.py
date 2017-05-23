# shipBonusMF1TorpedoFlightTime
#
# Used by:
# Ship: Hound
effectType = "passive"


def handler(fit, ship, context):
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Torpedoes"),
                                    "explosionDelay", ship.getModifiedItemAttr("shipBonusMF"), skill="Minmatar Frigate")
