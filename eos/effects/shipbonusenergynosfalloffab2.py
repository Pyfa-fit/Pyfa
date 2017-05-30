# shipBonusEnergyNosFalloffAB2
#
# Used by:
# Ship: Armageddon
effectType = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Energy Nosferatu", "falloffEffectiveness",
                                  src.getModifiedItemAttr("shipBonusAB2"), skill="Amarr Battleship")
