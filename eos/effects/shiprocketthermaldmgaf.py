# shipRocketThermalDmgAF
#
# Used by:
# Ship: Anathema
# Ship: Vengeance
effectType = "passive"


def handler(fit, ship, context):
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Rockets"),
                                    "thermalDamage", ship.getModifiedItemAttr("shipBonusAF"), skill="Amarr Frigate")
