# shipRemoteArmorFalloffGC1
#
# Used by:
# Ship: Oneiros
effectType = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Remote Armor Repair Systems"),
                                  "falloffEffectiveness", src.getModifiedItemAttr("shipBonusGC"),
                                  skill="Gallente Cruiser")
