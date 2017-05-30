# shipBonusMissileAoeVelocityMB2
#
# Used by:
# Ship: Typhoon
effectType = "passive"


def handler(fit, ship, context):
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Torpedoes"),
                                    "aoeVelocity", ship.getModifiedItemAttr("shipBonusMB2"),
                                    skill="Minmatar Battleship")
