# selfT2SmallLaserBeamDamageBonus
#
# Used by:
# Skill: Small Beam Laser Specialization
effectType = "passive"


def handler(fit, skill, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Beam Laser Specialization"),
                                  "damageMultiplier", skill.getModifiedItemAttr("damageMultiplierBonus") * skill.level)
