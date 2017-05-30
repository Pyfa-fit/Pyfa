# shipSETDmgBonusRookie
#
# Used by:
# Ship: Hematos
# Ship: Immolator
# Ship: Impairor
effectType = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Energy Turret"),
                                  "damageMultiplier", ship.getModifiedItemAttr("rookieSETDamageBonus"))
