# shipHTDamageBonusCC
#
# Used by:
# Ship: Moa
effectType = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Hybrid Turret"),
                                  "damageMultiplier", ship.getModifiedItemAttr("shipBonusCC"), skill="Caldari Cruiser")
