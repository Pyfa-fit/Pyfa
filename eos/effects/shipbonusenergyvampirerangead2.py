# Not used by any item
effectType = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Energy Nosferatu",
                                  "maxRange", ship.getModifiedItemAttr("shipBonusAD2"), skill="Amarr Destroyer")
