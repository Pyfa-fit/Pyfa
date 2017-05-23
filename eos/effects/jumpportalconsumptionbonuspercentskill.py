# jumpPortalConsumptionBonusPercentSkill
#
# Used by:
# Skill: Jump Portal Generation
effectType = "passive"


def handler(fit, skill, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill(skill), "consumptionQuantity",
                                  skill.getModifiedItemAttr("consumptionQuantityBonusPercent") * skill.level)
