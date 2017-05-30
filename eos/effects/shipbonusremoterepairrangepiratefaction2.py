# shipBonusRemoteRepairRangePirateFaction2
#
# Used by:
# Ship: Nestor
effectType = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Remote Armor Repair Systems"),
                                  "maxRange", ship.getModifiedItemAttr("shipBonusPirateFaction2"))
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Remote Armor Repair Systems"),
                                  "falloffEffectiveness", ship.getModifiedItemAttr("shipBonusPirateFaction2"))
