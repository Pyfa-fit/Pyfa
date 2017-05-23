# shipBonusStasisMF2
#
# Used by:
# Ship: Caedes
# Ship: Cruor
# Ship: Freki
effectType = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Stasis Web",
                                  "maxRange", ship.getModifiedItemAttr("shipBonusMF2"), skill="Minmatar Frigate")
