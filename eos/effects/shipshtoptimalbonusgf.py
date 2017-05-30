# shipSHTOptimalBonusGF
#
# Used by:
# Ship: Ares
effectType = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Hybrid Turret"),
                                  "maxRange", ship.getModifiedItemAttr("shipBonusGF"), skill="Gallente Frigate")
