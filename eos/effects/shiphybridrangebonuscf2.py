# shipHybridRangeBonusCF2
#
# Used by:
# Ship: Harpy
# Ship: Raptor
effectType = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Hybrid Turret"),
                                  "maxRange", ship.getModifiedItemAttr("shipBonusCF2"), skill="Caldari Frigate")
