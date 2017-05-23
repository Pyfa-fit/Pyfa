# falloffBonusEffectHybrids
#
# Used by:
# Modules named like: Hybrid Ambit Extension (8 of 8)
effectType = "passive"


def handler(fit, module, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Hybrid Weapon",
                                  "falloff", module.getModifiedItemAttr("falloffBonus"),
                                  stackingPenalties=True)
