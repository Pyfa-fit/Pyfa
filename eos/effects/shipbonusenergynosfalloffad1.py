# shipBonusEnergyNosFalloffAD1
#
# Used by:
# Ship: Dragoon
effectType = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Energy Nosferatu", "falloffEffectiveness",
                                  src.getModifiedItemAttr("shipBonusAD1"), skill="Amarr Destroyer")
