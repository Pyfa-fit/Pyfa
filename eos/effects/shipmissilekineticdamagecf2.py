# shipMissileKineticDamageCF2
#
# Used by:
# Ship: Garmur
effectType = "passive"


def handler(fit, ship, context):
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Missile Launcher Operation"),
                                    "kineticDamage", ship.getModifiedItemAttr("shipBonusCF2"), skill="Caldari Frigate")
