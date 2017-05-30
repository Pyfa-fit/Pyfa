# shipBonusMediumHybridDmgCC2
#
# Used by:
# Ship: Falcon
effectType = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Hybrid Turret"),
                                  "damageMultiplier", ship.getModifiedItemAttr("shipBonusCC2"), skill="Caldari Cruiser")
