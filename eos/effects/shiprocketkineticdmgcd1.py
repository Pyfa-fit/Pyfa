# shipRocketKineticDmgCD1
#
# Used by:
# Ship: Corax
effectType = "passive"


def handler(fit, ship, context):
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Rockets"),
                                    "kineticDamage", ship.getModifiedItemAttr("shipBonusCD1"),
                                    skill="Caldari Destroyer")
