# shipBonusHeavyMissileKineticDmgMB
#
# Used by:
# Ship: Typhoon Fleet Issue
effectType = "passive"


def handler(fit, ship, context):
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Heavy Missiles"),
                                    "kineticDamage", ship.getModifiedItemAttr("shipBonusMB"),
                                    skill="Minmatar Battleship")
