# shipEnergyTCapNeedBonusRookie
#
# Used by:
# Ship: Hematos
# Ship: Impairor
effectType = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Energy Turret"),
                                  "capacitorNeed", ship.getModifiedItemAttr("rookieSETCapBonus"))
