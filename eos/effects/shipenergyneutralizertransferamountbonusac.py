# shipEnergyNeutralizerTransferAmountBonusAC
#
# Used by:
# Ship: Ashimmu
# Ship: Vangel
effectType = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Energy Neutralizer",
                                  "energyNeutralizerAmount", ship.getModifiedItemAttr("shipBonusAC"),
                                  skill="Amarr Cruiser")
