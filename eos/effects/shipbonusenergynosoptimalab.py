# shipBonusEnergyNosOptimalAB
#
# Used by:
# Ship: Armageddon
effectType = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Energy Nosferatu", "maxRange",
                                  src.getModifiedItemAttr("shipBonusAB"), skill="Amarr Battleship")
