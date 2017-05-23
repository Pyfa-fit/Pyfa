# roleBonusWDRange
#
# Used by:
# Ship: Crucifier Navy Issue
effectType = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Weapon Disruption"), "falloff",
                                  src.getModifiedItemAttr("roleBonus"))
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Weapon Disruption"), "maxRange",
                                  src.getModifiedItemAttr("roleBonus"))
