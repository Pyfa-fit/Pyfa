# shipBonusHeavyAssaultMissileKineticDamageCBC1
#
# Used by:
# Ship: Drake
# Ship: Nighthawk
effectType = "passive"


def handler(fit, ship, context):
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Heavy Assault Missiles"),
                                    "kineticDamage", ship.getModifiedItemAttr("shipBonusCBC1"),
                                    skill="Caldari Battlecruiser")
