# missileThermalDmgBonusTorpedo
#
# Used by:
# Implants named like: Zainou 'Snapshot' Torpedoes TD (6 of 6)
effectType = "passive"


def handler(fit, container, context):
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Torpedoes"),
                                    "thermalDamage", container.getModifiedItemAttr("damageMultiplierBonus"))
