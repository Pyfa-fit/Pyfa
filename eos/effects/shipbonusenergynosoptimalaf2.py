# shipBonusEnergyNosOptimalAF2
#
# Used by:
# Ship: Malice
effectType = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Energy Nosferatu", "maxRange",
                                  src.getModifiedItemAttr("shipBonus2AF"), skill="Amarr Frigate")
