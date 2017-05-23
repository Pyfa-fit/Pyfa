# shipHybridRangeBonusRookie
#
# Used by:
# Ship: Ibis
effectType = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Hybrid Turret"),
                                  "maxRange", ship.getModifiedItemAttr("rookieSHTOptimalBonus"))
