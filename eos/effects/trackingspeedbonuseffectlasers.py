# trackingSpeedBonusEffectLasers
#
# Used by:
# Modules named like: Energy Metastasis Adjuster (8 of 8)
effectType = "passive"


def handler(fit, module, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Energy Weapon",
                                  "trackingSpeed", module.getModifiedItemAttr("trackingSpeedBonus"),
                                  stackingPenalties=True)
