# shipSETOptimalBonusRookie
#
# Used by:
# Ship: Immolator
effectType = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Energy Turret"),
                                  "maxRange", ship.getModifiedItemAttr("rookieSETOptimal"))
