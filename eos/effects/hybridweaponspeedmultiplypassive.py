# hybridWeaponSpeedMultiplyPassive
#
# Used by:
# Modules named like: Hybrid Burst Aerator (8 of 8)
effectType = "passive"


def handler(fit, module, context):
    fit.modules.filteredItemMultiply(lambda mod: mod.item.group.name == "Hybrid Weapon",
                                     "speed", module.getModifiedItemAttr("speedMultiplier"),
                                     stackingPenalties=True)
