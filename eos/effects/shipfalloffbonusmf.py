# shipFalloffBonusMF
#
# Used by:
# Ship: Chremoas
# Ship: Dramiel
effectType = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Projectile Turret"),
                                  "falloff", ship.getModifiedItemAttr("shipBonusMF"), skill="Minmatar Frigate")
