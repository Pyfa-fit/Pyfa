# eliteBonusCommandShipHybridOptimalCS1
#
# Used by:
# Ship: Vulture
effectType = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Hybrid Turret"),
                                  "maxRange", ship.getModifiedItemAttr("eliteBonusCommandShips1"),
                                  skill="Command Ships")
