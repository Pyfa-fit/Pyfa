# eliteIndustrialMWDHeatBonus
#
# Used by:
# Ships from group: Deep Space Transport (4 of 4)
effectType = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("High Speed Maneuvering"),
                                  "overloadSpeedFactorBonus", ship.getModifiedItemAttr("roleBonusOverheatDST"))
