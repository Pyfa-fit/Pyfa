# shipSPTOptimalBonusMF
#
# Used by:
# Ship: Chremoas
effectType = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Projectile Turret"),
                                  "maxRange", ship.getModifiedItemAttr("shipBonusMF"), skill="Minmatar Frigate")
