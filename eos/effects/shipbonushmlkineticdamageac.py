# shipBonusHMLKineticDamageAC
#
# Used by:
# Ship: Sacrilege
effectType = "passive"


def handler(fit, ship, context):
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Heavy Missiles"),
                                    "kineticDamage", ship.getModifiedItemAttr("shipBonusAC"), skill="Amarr Cruiser")
