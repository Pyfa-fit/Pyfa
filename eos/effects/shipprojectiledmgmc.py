# shipProjectileDmgMC
#
# Used by:
# Ship: Mimir
effectType = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Projectile Turret"),
                                  "damageMultiplier", ship.getModifiedItemAttr("shipBonusMC"), skill="Minmatar Cruiser")
