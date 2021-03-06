# shipMissileExpDamageCC
#
# Used by:
# Ship: Orthrus
# Ship: Osprey Navy Issue
effectType = "passive"


def handler(fit, ship, context):
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Missile Launcher Operation"),
                                    "explosiveDamage", ship.getModifiedItemAttr("shipBonusCC"), skill="Caldari Cruiser")
