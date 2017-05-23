# shipBonusEnergyNeutFalloffEAF3
#
# Used by:
# Ship: Sentinel
effectType = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Energy Neutralizer", "falloffEffectiveness",
                                  src.getModifiedItemAttr("eliteBonusElectronicAttackShip3"),
                                  skill="Electronic Attack Ships")
