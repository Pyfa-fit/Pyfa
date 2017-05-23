# shipEnergyVampireTransferAmountBonusAc
#
# Used by:
# Ship: Ashimmu
# Ship: Rabisu
# Ship: Vangel
effectType = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Energy Nosferatu",
                                  "powerTransferAmount", ship.getModifiedItemAttr("shipBonusAC"), skill="Amarr Cruiser")
