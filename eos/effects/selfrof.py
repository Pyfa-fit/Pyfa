# selfRof
#
# Used by:
# Skills named like: Missile Specialization (4 of 5)
# Skill: Rocket Specialization
# Skill: Torpedo Specialization
effectType = "passive"


def handler(fit, skill, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill(skill),
                                  "speed", skill.getModifiedItemAttr("rofBonus") * skill.level)
