# shipBonusEnergyNeutOptimalAC1
#
# Used by:
# Ship: Vangel
effectType = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Energy Neutralizer", "maxRange",
                                  src.getModifiedItemAttr("shipBonusAC"), skill="Amarr Cruiser")
