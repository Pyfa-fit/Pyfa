# shipEnergyDrainAmountAF1
#
# Used by:
# Ship: Caedes
# Ship: Cruor
# Ship: Sentinel
effectType = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Energy Nosferatu",
                                  "powerTransferAmount", ship.getModifiedItemAttr("shipBonusAF"), skill="Amarr Frigate")
