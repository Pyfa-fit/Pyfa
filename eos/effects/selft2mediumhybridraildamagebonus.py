# selfT2MediumHybridRailDamageBonus
#
# Used by:
# Skill: Medium Railgun Specialization
effectType = "passive"


def handler(fit, skill, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Railgun Specialization"),
                                  "damageMultiplier", skill.getModifiedItemAttr("damageMultiplierBonus") * skill.level)
