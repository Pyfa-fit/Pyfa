# shipBonusThermalMissileDamageGC2
#
# Used by:
# Ship: Chameleon
# Ship: Gila

effectType = "passive"


def handler(fit, ship, context):
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Missile Launcher Operation"),
                                    "thermalDamage", ship.getModifiedItemAttr("shipBonusGC2"), skill="Gallente Cruiser")
