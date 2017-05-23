# skillBonusXLCruiseMissileSpecialization
#
# Used by:
# Skill: XL Cruise Missile Specialization
effectType = "passive"


def handler(fit, src, context):
    lvl = src.level
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("XL Cruise Missile Specialization"), "speed",
                                  src.getModifiedItemAttr("rofBonus") * lvl)
